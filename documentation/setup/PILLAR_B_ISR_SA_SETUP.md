# 📊 Pilar B - ISR (SA) - Seasonally Adjusted - Setup Guide

**Projeto:** Dashboard E-Commerce Brasil - CEUB
**Data:** Novembro 2025
**Pilar:** Macro/Estratégico (Indicadores Econômicos)

---

## 📖 Contexto

Esta KPI expõe o valor mensal do **ISR (Inventories-to-Sales Ratio)** ajustado sazonalmente:

- **ISR (SA)**: Razão entre estoques e vendas no varejo dos EUA (série ajustada sazonalmente)
- **Fonte**: Federal Reserve Economic Data (FRED) - Series `RETAILIRSA`
- **Período**: Jan/1992 a Jul/2025 (403 meses)
- **Grão**: Mês (série nacional)
- **Unidade**: Razão (número decimal, ex: 1.37)

---

## 📁 Arquivos de Dados

### Localização
```
csv's_Pillar_B/
├── RETAILIRSA.csv           (ISR ajustado sazonalmente - 403 meses)
└── process_retailirsa.py    (script ETL)
```

### Estrutura do CSV de Entrada

**RETAILIRSA.csv** (403 linhas + header)
```
observation_date,RETAILIRSA
1992-01-01,1.65
1992-02-01,1.66
...
2025-07-01,1.29
```

---

## 🔄 Processamento ETL

### Script: `process_retailirsa.py`

**O que faz:**
1. Carrega RETAILIRSA.csv
2. Converte observation_date para datetime
3. Cria YearMonthKey (YYYYMM)
4. Renomeia RETAILIRSA → ISR_SA
5. Salva `FactRETAILIRSA.csv` processado

**Como executar:**
```bash
cd "/Volumes/Crucial X6/Projeto_integrador"
./venv/bin/python csv's_Pillar_B/process_retailirsa.py
```

### Arquivo de Saída

**data/processed/pillar_b/FactRETAILIRSA.csv** (403 linhas)

Colunas:
- `MonthDate` (YYYY-MM-DD) - Data do mês (sempre dia 01)
- `YearMonthKey` (YYYYMM) - Chave temporal inteira
- `ISR_SA` (decimal) - Razão estoque/vendas ajustada sazonalmente

---

## 📊 KPI Implementada

### ISR (SA) - Seasonally Adjusted

**Nome técnico**: `kpi_isr_sa`

**Descrição**: Razão entre estoques e vendas no varejo dos EUA (ajustado sazonalmente)

**Fórmula:**
```
ISR (SA) = RETAILIRSA
```

**Valor**: Direto da coluna `ISR_SA` (sem transformação)

**Unidade**: Razão (número decimal)

**Interpretação**:
- **< 1.0**: Vendas > Estoques (demanda forte, risco de ruptura)
- **1.0-1.5**: Equilíbrio normal
- **> 1.5**: Estoques > Vendas (acúmulo de inventário)

**Regras BLANK**:
- Retorna BLANK quando não houver valor para o mês no CSV
- **Observação**: Na série atual (Jan/1992 - Jul/2025) não há valores NULL

**Limites**:
- Série macro (não comparável a nível SKU/loja)
- Não aplicar deflatores
- **NÃO somar ou fazer média entre meses** - usar o valor do próprio mês
- Não converter para % (já é uma razão)

---

## 📋 Passos para Implementar no Power BI

### Passo 1: Importar Dados

1. Abra Power BI Desktop
2. **Get Data** → **Text/CSV**
3. Navegue até: `data/processed/pillar_b/FactRETAILIRSA.csv`
4. Clique **Load**

### Passo 2: Verificar Tipos de Dados

No **Data View**, verifique:
- `MonthDate`: Date
- `YearMonthKey`: Whole Number
- `ISR_SA`: Decimal Number

### Passo 3: (Opcional) Relacionamento com Calendário

Se você tiver uma tabela `dimmonth`:
- Relacione `dimmonth[yearmonthkey]` (1) → `FactRETAILIRSA[YearMonthKey]` (*)
- Cardinalidade: One-to-Many
- Cross-filter: Single
- Active: Yes

### Passo 4: Criar Medida DAX

Crie uma tabela `_Measures_ISR` (ou use `_Measures` existente):

**Medida: ISR (SA)**
```dax
ISR (SA) =
VAR CurrentISR = SUM(FactRETAILIRSA[ISR_SA])
RETURN
    IF(
        ISBLANK(CurrentISR),
        BLANK(),
        CurrentISR
    )
```

**Formatação:**
- Format: Number
- Decimal places: 2
- Display name: "ISR (razão) — SA"

**Tooltip personalizado:**
```
Definição: Razão estoque/vendas ajustada sazonalmente (SA)
Unidade: Razão (ex.: 1,37)
Regra: Mês sem valor no CSV → BLANK
Nota: Série nacional; não converter em %; não agregar/somar entre meses
```

### Passo 5: Criar Visualizações

#### Visual 1: Card Principal - ISR do Mês Atual
- **Value**: `[ISR (SA)]`
- **Tipo**: Card
- **Formatação**: 2 casas decimais

#### Visual 2: Gráfico de Linha - Série Histórica
- **X-Axis**: MonthDate (ou dimmonth[MonthDate])
- **Y-Axis**: `[ISR (SA)]`
- **Tipo**: Line Chart
- **Data range**: Jan/1992 - Jul/2025

#### Visual 3: Tooltip Detalhado
Adicione ao gráfico de linha:
```
Mês: [MonthDate]
ISR (SA): [ISR (SA)]
Unidade: Razão

Fórmula: Inventories / Sales (ajustado sazonalmente)
```

---

## 🎯 Estatísticas dos Dados

### ISR (SA) - Jan/1992 a Jul/2025
- **Registros**: 403 meses
- **Média**: 1.49
- **Mediana**: 1.49
- **Mínimo**: 1.09 (Jun/2021) - período pós-pandemia com demanda forte
- **Máximo**: 1.75 (Abr/1995)
- **NULL/BLANK**: 0 (nenhum mês ausente)

### Tendência Recente (últimos 12 meses)
```
2024-08: 1.33
2024-09: 1.33
2024-10: 1.32
2024-11: 1.31
2024-12: 1.29
2025-01: 1.31
2025-02: 1.31
2025-03: 1.29
2025-04: 1.29
2025-05: 1.30
2025-06: 1.29
2025-07: 1.29 ← Último valor disponível
```

---

## ✅ QA - Validação Manual

### Amostra de Teste (3 meses)

**Agosto/2024**
- ISR_SA (CSV): 1.33
- ISR_SA (BI): 1.33 ✅
- Tipo: float64 ✅
- NULL?: False ✅

**Setembro/2024**
- ISR_SA (CSV): 1.33
- ISR_SA (BI): 1.33 ✅
- Tipo: float64 ✅
- NULL?: False ✅

**Outubro/2024**
- ISR_SA (CSV): 1.32
- ISR_SA (BI): 1.32 ✅
- Tipo: float64 ✅
- NULL?: False ✅

**Status**: ✅ Todas as validações passaram (erro = 0.00)

---

## 🎨 Exemplo de Dashboard

```
┌────────────────────────────────────────────────┐
│  ISR (razão) — SA                              │
├────────────────────────────────────────────────┤
│  [Card Principal]                              │
│  ┌──────────┐                                  │
│  │   1.29   │  ← Julho/2025                    │
│  │ (razão)  │                                  │
│  └──────────┘                                  │
│                                                │
│  [Gráfico de Linha: ISR ao longo do tempo]   │
│  - Eixo X: Meses (Jan/1992 - Jul/2025)       │
│  - Eixo Y: ISR (SA)                          │
│  - Linha azul contínua                        │
│                                                │
│  Tooltip ao passar mouse:                     │
│  ┌─────────────────────────────┐             │
│  │ Mês: Jul/2025               │             │
│  │ ISR (SA): 1.29              │             │
│  │ Unidade: Razão              │             │
│  │                             │             │
│  │ Ajustado sazonalmente (SA)  │             │
│  └─────────────────────────────┘             │
└────────────────────────────────────────────────┘
```

---

## 📚 Referências

- **Fonte de dados**: [FRED - Federal Reserve Economic Data](https://fred.stlouisfed.org/)
- **ISR SA**: Series ID `RETAILIRSA`
- **Definição completa**: Ratio of Total Business Inventories to Sales for Retail Trade (Seasonally Adjusted)
- **Documentação FRED**: https://fred.stlouisfed.org/series/RETAILIRSA

---

## 🔧 Troubleshooting

### Problema: "Medida retorna BLANK"
**Solução**: Verifique se importou `FactRETAILIRSA.csv` e se há filtros de data ativos. A série vai de Jan/1992 a Jul/2025.

### Problema: "Valores muito altos ou baixos"
**Solução**: ISR é uma razão (inventories/sales). Valores normais: 1.0-1.8. Se aparecer > 10, verificar se não converteu para %.

### Problema: "Soma de ISR entre meses"
**Solução**: ISR é valor pontual do mês, não deve ser somado. Use SUM() apenas para extrair o valor do mês vigente no contexto.

### Problema: "Relacionamento com dimmonth não funciona"
**Solução**: Verifique se YearMonthKey está formatado como Whole Number em ambas as tabelas. Active relationship e Single cross-filter direction.

---

**Última atualização**: 2025-11-17
**Versão**: 1.0
**Autor**: Claude Code + Equipe CEUB
