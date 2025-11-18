# 📊 Pilar B - ISR (Inventories-to-Sales Ratio) - Setup Guide

**Projeto:** Dashboard E-Commerce Brasil - CEUB
**Data:** Novembro 2025
**Pilar:** Macro/Estratégico (Indicadores Econômicos)

---

## 📖 Contexto

Este pilar trabalha com **indicadores macroeconômicos** dos EUA relacionados ao varejo:

- **ISR (Inventories-to-Sales Ratio)**: Razão entre estoques e vendas no varejo
- **SA (Seasonally Adjusted)**: Série ajustada sazonalmente
- **NSA (Not Seasonally Adjusted)**: Série não ajustada (bruta)

**Fonte dos dados**: Federal Reserve Economic Data (FRED)
**Período**: Jan/1992 a Jul/2025 (403 meses)

---

## 📁 Arquivos de Dados

### Localização
```
csv's_Pillar_B/
├── RETAILIRSA.csv      (ISR ajustado sazonalmente)
├── RETAILIRNSA.csv     (ISR não ajustado)
└── process_isr_seasonal_gap.py (script ETL)
```

### Estrutura dos CSVs

**RETAILIRSA.csv** (403 linhas)
```
observation_date,RETAILIRSA
1992-01-01,1.65
1992-02-01,1.66
...
```

**RETAILIRNSA.csv** (403 linhas)
```
observation_date,RETAILIRNSA
1992-01-01,1.81
1992-02-01,1.83
...
```

---

## 🔄 Processamento ETL

### Script: `process_isr_seasonal_gap.py`

**O que faz:**
1. Carrega RETAILIRSA.csv e RETAILIRNSA.csv
2. Converte datas e cria YearMonthKey (YYYYMM)
3. Faz inner join temporal (apenas meses presentes em ambas)
4. Calcula Seasonal Gap (absoluto e percentual)
5. Salva `FactISRSeasonalGap.csv` processado

**Como executar:**
```bash
cd "/Volumes/Crucial X6/Projeto_integrador"
./venv/bin/python csv's_Pillar_B/process_isr_seasonal_gap.py
```

### Arquivo de Saída

**data/processed/pillar_b/FactISRSeasonalGap.csv** (403 linhas)

Colunas:
- `MonthDate` (YYYY-MM-DD)
- `YearMonthKey` (YYYYMM)
- `ISR_SA` (razão - ajustado)
- `ISR_NSA` (razão - não ajustado)
- `Gap_abs` (razão - diferença absoluta)
- `Gap_pct` (% - diferença percentual)

---

## 📊 KPIs Implementadas

### 1. ISR (SA) - Seasonally Adjusted

**Descrição**: Razão entre estoques e vendas no varejo (ajustado sazonalmente)

**Valor**: Direto da coluna `ISR_SA`

**Interpretação**:
- **< 1.0**: Vendas > Estoques (demanda forte)
- **1.0-1.5**: Equilíbrio normal
- **> 1.5**: Estoques > Vendas (acúmulo de inventário)

---

### 2. ISR (NSA) - Not Seasonally Adjusted

**Descrição**: Razão entre estoques e vendas no varejo (série bruta, com sazonalidade)

**Valor**: Direto da coluna `ISR_NSA`

**Uso**: Comparação com a série ajustada para evidenciar efeitos sazonais

---

### 3. ISR Seasonal Gap (Absoluto)

**Nome técnico**: `kpi_isr_seasonal_gap_abs`

**Fórmula:**
```
Gap_abs = ISR_SA - ISR_NSA
```

**Unidade**: Razão (número decimal)

**Medida DAX:**
```dax
ISR Seasonal Gap (Abs) =
VAR ISR_SA_Val = [ISR (SA)]
VAR ISR_NSA_Val = [ISR (NSA)]
RETURN
    IF(
        ISBLANK(ISR_SA_Val) || ISBLANK(ISR_NSA_Val),
        BLANK(),
        ISR_SA_Val - ISR_NSA_Val
    )
```

**Formatação**: Number, 4 casas decimais

**Regras BLANK**:
- Se ISR_SA = NULL → BLANK
- Se ISR_NSA = NULL → BLANK

---

### 4. ISR Seasonal Gap (Percentual)

**Nome técnico**: `kpi_isr_seasonal_gap_pct`

**Fórmula:**
```
Gap_pct = (ISR_SA - ISR_NSA) / ISR_NSA × 100
```

**Unidade**: Percentual (%)

**Medida DAX:**
```dax
ISR Seasonal Gap (%) =
VAR ISR_SA_Val = [ISR (SA)]
VAR ISR_NSA_Val = [ISR (NSA)]
RETURN
    IF(
        ISBLANK(ISR_SA_Val) || ISBLANK(ISR_NSA_Val) || ISR_NSA_Val = 0,
        BLANK(),
        DIVIDE(ISR_SA_Val - ISR_NSA_Val, ISR_NSA_Val)
    )
```

**Formatação**: Percentage, 1 casa decimal

**Regras BLANK**:
- Se ISR_SA = NULL → BLANK
- Se ISR_NSA = NULL → BLANK
- Se ISR_NSA = 0 → BLANK

**Interpretação**:
- **Gap > 0**: Ajuste sazonal aumentou o ISR (sazonalidade negativa removida)
- **Gap < 0**: Ajuste sazonal diminuiu o ISR (sazonalidade positiva removida)
- **Gap ≈ 0**: Pouca sazonalidade no mês

---

## 🎯 Estatísticas dos Dados

### Gap Absoluto (razão)
- **Média**: -0.0069
- **Mediana**: -0.0100
- **Min**: -0.2500 (maior ajuste negativo)
- **Max**: 0.3500 (maior ajuste positivo)

### Gap Percentual (%)
- **Média**: 0.09%
- **Mediana**: -0.65%
- **Min**: -12.63%
- **Max**: 26.32%
- **BLANKs**: 0 (nenhum NSA = 0)

---

## 📋 Passos para Implementar no Power BI

### Passo 1: Importar Dados

1. Abra Power BI Desktop
2. **Get Data** → **Text/CSV**
3. Navegue até: `data/processed/pillar_b/FactISRSeasonalGap.csv`
4. Clique **Load**

### Passo 2: Verificar Tipos de Dados

No **Data View**, verifique:
- `MonthDate`: Date
- `YearMonthKey`: Whole Number
- `ISR_SA`: Decimal Number
- `ISR_NSA`: Decimal Number
- `Gap_abs`: Decimal Number
- `Gap_pct`: Decimal Number

### Passo 3: (Opcional) Relacionamento com Calendário

Se você tiver uma tabela `dimmonth`:
- Relacione `dimmonth[yearmonthkey]` (1) → `FactISRSeasonalGap[YearMonthKey]` (*)
- Cardinalidade: One-to-Many
- Cross-filter: Single

### Passo 4: Criar Medidas DAX

Crie uma tabela `_Measures_ISR` (ou use `_Measures` existente):

**Medida 1: ISR (SA)**
```dax
ISR (SA) = SUM(FactISRSeasonalGap[ISR_SA])
```
Formato: Number, 2 casas decimais

**Medida 2: ISR (NSA)**
```dax
ISR (NSA) = SUM(FactISRSeasonalGap[ISR_NSA])
```
Formato: Number, 2 casas decimais

**Medida 3: ISR Seasonal Gap (Abs)**
```dax
ISR Seasonal Gap (Abs) =
VAR ISR_SA_Val = [ISR (SA)]
VAR ISR_NSA_Val = [ISR (NSA)]
RETURN
    IF(
        ISBLANK(ISR_SA_Val) || ISBLANK(ISR_NSA_Val),
        BLANK(),
        ISR_SA_Val - ISR_NSA_Val
    )
```
Formato: Number, 4 casas decimais

**Medida 4: ISR Seasonal Gap (%)**
```dax
ISR Seasonal Gap (%) =
VAR ISR_SA_Val = [ISR (SA)]
VAR ISR_NSA_Val = [ISR (NSA)]
RETURN
    IF(
        ISBLANK(ISR_SA_Val) || ISBLANK(ISR_NSA_Val) || ISR_NSA_Val = 0,
        BLANK(),
        DIVIDE(ISR_SA_Val - ISR_NSA_Val, ISR_NSA_Val)
    )
```
Formato: Percentage, 1 casa decimal

### Passo 5: Criar Visualizações

#### Visual 1: Gráfico de Linha - ISR ao Longo do Tempo
- **X-Axis**: MonthDate (ou dimmonth[MonthDate])
- **Y-Axis**: `[ISR (SA)]` (série principal)
- **Secondary Y-Axis**: `[ISR (NSA)]` (série comparativa)
- **Tipo**: Line Chart

#### Visual 2: Badge/Card - Seasonal Gap do Mês Atual
- **Card 1**: `[ISR Seasonal Gap (Abs)]`
- **Card 2**: `[ISR Seasonal Gap (%)]`
- **Posição**: Ao lado do gráfico de linha

#### Visual 3: Tooltip Detalhado
Adicione ao gráfico de linha:
```
Mês: [MonthDate]
ISR (SA): [ISR (SA)]
ISR (NSA): [ISR (NSA)]
Gap Abs: [ISR Seasonal Gap (Abs)]
Gap %: [ISR Seasonal Gap (%)]

Fórmula: (SA - NSA) / NSA
```

---

## ✅ QA - Validação Manual

### Amostra de Teste (últimos 3 meses)

**Maio/2025**
- ISR_SA: 1.30
- ISR_NSA: 1.23
- Gap_abs: 0.0700 ✅
- Gap_pct: 5.69% ✅

**Junho/2025**
- ISR_SA: 1.29
- ISR_NSA: 1.30
- Gap_abs: -0.0100 ✅
- Gap_pct: -0.77% ✅

**Julho/2025**
- ISR_SA: 1.29
- ISR_NSA: 1.24
- Gap_abs: 0.0500 ✅
- Gap_pct: 4.03% ✅

**Erro**: 0.000000 (perfeito!)

---

## 🎨 Exemplo de Dashboard

```
┌────────────────────────────────────────────────┐
│  ISR - Inventories-to-Sales Ratio             │
├────────────────────────────────────────────────┤
│                                                │
│  [Gráfico de Linha: ISR ao longo do tempo]   │
│  - Linha azul: ISR (SA)                       │
│  - Linha cinza tracejada: ISR (NSA)           │
│                                                │
├────────────────────────────────────────────────┤
│  Seasonal Gap (Jul/2025):                     │
│  ┌──────────┐  ┌──────────┐                  │
│  │  0.0500  │  │  4.03%   │                  │
│  │ (razão)  │  │  (pct)   │                  │
│  └──────────┘  └──────────┘                  │
└────────────────────────────────────────────────┘
```

---

## 📚 Referências

- **Fonte de dados**: [FRED - Federal Reserve Economic Data](https://fred.stlouisfed.org/)
- **ISR SA**: Series ID `RETAILIRSA`
- **ISR NSA**: Series ID `RETAILIRNSA`
- **Definição**: Razão entre estoques totais e vendas mensais no varejo dos EUA

---

## 🔧 Troubleshooting

### Problema: "Medidas retornam BLANK"
**Solução**: Verifique se importou `FactISRSeasonalGap.csv` e se há filtros de data ativos

### Problema: "Gap_pct mostra valores estranhos"
**Solução**: Verifique se formatou como Percentage (não Decimal)

### Problema: "Não vejo dados"
**Solução**: Verifique range de datas - dados vão de Jan/1992 a Jul/2025

---

**Última atualização**: 2025-11-17
**Versão**: 1.0
**Autor**: Claude Code + Equipe CEUB
