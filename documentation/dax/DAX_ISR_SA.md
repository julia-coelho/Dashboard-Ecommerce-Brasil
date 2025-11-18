# 📊 Medida DAX - ISR (SA) - Seasonally Adjusted

## Contexto

Esta medida expõe o valor mensal do **ISR (Inventories-to-Sales Ratio)** ajustado sazonalmente.

**Tabela usada**: `FactRETAILIRSA` (403 meses: Jan/1992 - Jul/2025)

---

## 📐 ISR (SA) - Seasonally Adjusted

**Descrição**: Razão entre estoques e vendas no varejo dos EUA (ajustado sazonalmente)

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
- Formato: Number
- Decimal places: 2
- Display Units: None
- Display name: "ISR (razão) — SA"

**O que faz**:
1. Extrai o valor de ISR_SA para o mês no contexto atual (filtro de data)
2. Retorna BLANK se não houver valor para aquele mês
3. Caso contrário, retorna o valor ISR_SA

**Exemplo de uso**:
- Card mostrando "ISR: 1.29" para Julho/2025
- Gráfico de linha mostrando série histórica Jan/1992 - Jul/2025

**Unidade**: Razão (número decimal)

**Interpretação**:
- **< 1.0**: Vendas > Estoques (demanda forte, risco de ruptura)
- **1.0-1.5**: Equilíbrio normal
- **> 1.5**: Estoques > Vendas (acúmulo de inventário, risco de obsolescência)

---

## 📋 Regras de Negócio

### Regras BLANK

A medida retorna BLANK quando:
- Não há dados para o mês selecionado no filtro
- O contexto de filtro não resolve para um mês específico
- A coluna `ISR_SA` está NULL para aquele mês

**Observação**: Na série atual (Jan/1992 - Jul/2025) não há valores NULL.

### Limitações

⚠️ **IMPORTANTE - Não agregar entre meses**:
- ISR é um valor **pontual do mês**
- **NÃO somar** ISR de vários meses
- **NÃO fazer média** simples de ISR entre meses
- Use filtros de data para selecionar 1 mês específico

⚠️ **Série macroeconômica**:
- Representa mercado nacional (EUA)
- Não é comparável a nível SKU/loja individual
- Não aplicar deflatores

⚠️ **Unidade é razão, não percentual**:
- Valor típico: 1.29 (razão)
- **Não converter para %** (12.9% seria incorreto)
- Formatar como número decimal com 2 casas

---

## 🎯 Casos de Teste

### Teste 1: Mês com Dados Válidos (Julho/2025)
**Filtro**: MonthDate = 2025-07-01

**Dados**:
- ISR_SA no CSV: 1.29

**Resultado esperado**:
- ISR (SA) = 1.29
- ✅ Valor numérico válido

### Teste 2: Mês com Dados Válidos (Junho/2021 - Mínimo histórico)
**Filtro**: MonthDate = 2021-06-01

**Dados**:
- ISR_SA no CSV: 1.09

**Resultado esperado**:
- ISR (SA) = 1.09
- ✅ Menor ISR da série (demanda forte pós-pandemia)

### Teste 3: Mês com Dados Válidos (Abril/1995 - Máximo histórico)
**Filtro**: MonthDate = 1995-04-01

**Dados**:
- ISR_SA no CSV: 1.75

**Resultado esperado**:
- ISR (SA) = 1.75
- ✅ Maior ISR da série (acúmulo de estoque)

### Teste 4: Mês Sem Dados (Agosto/2025 - futuro)
**Filtro**: MonthDate = 2025-08-01

**Dados**:
- Não existe no CSV

**Resultado esperado**:
- ISR (SA) = BLANK
- ✅ Regra de BLANK funcionando

### Teste 5: Múltiplos Meses Selecionados (ERRO ESPERADO)
**Filtro**: MonthDate entre Jan/2025 e Jul/2025 (7 meses)

**Resultado esperado**:
- SUM() irá somar os 7 valores → resultado incorreto
- ⚠️ **Não fazer isso!** ISR é valor pontual, não cumulativo
- **Solução**: Usar filtro para 1 mês específico ou criar medida diferente com LASTNONBLANK()

---

## 📊 Exemplos de Visualizações

### Card Principal
```
┌─────────────────────────┐
│ ISR (razão) — SA        │
│       1.29              │
│  Jul/2025               │
└─────────────────────────┘
```

### Tooltip (ao passar mouse no gráfico)
```
Mês: Julho/2025
ISR (SA): 1.29

Definição: Razão estoque/vendas ajustada sazonalmente (SA)
Unidade: Razão (1.29 = estoques 29% maiores que vendas)
Nota: Série nacional; não agregar entre meses
```

### Tabela (últimos 12 meses)
```
Mês       | ISR (SA) | Status
----------|----------|------------------
Jul/2025  | 1.29     | Equilíbrio
Jun/2025  | 1.29     | Equilíbrio
Mai/2025  | 1.30     | Equilíbrio
Abr/2025  | 1.29     | Equilíbrio
Mar/2025  | 1.29     | Equilíbrio
Fev/2025  | 1.31     | Equilíbrio
Jan/2025  | 1.31     | Equilíbrio
Dez/2024  | 1.29     | Equilíbrio
Nov/2024  | 1.31     | Equilíbrio
Out/2024  | 1.32     | Equilíbrio
Set/2024  | 1.33     | Equilíbrio
Ago/2024  | 1.33     | Equilíbrio
```

---

## 📋 Checklist de Implementação

### Passo 1: Criar Medida
- [ ] Ir em Report View → Data pane
- [ ] Click direito em `_Measures` → New measure
- [ ] Colar a fórmula DAX completa
- [ ] Nomear como "ISR (SA)"

### Passo 2: Formatar Medida
- [ ] Formato: Number
- [ ] Decimal places: 2
- [ ] Display Units: None
- [ ] Display name: "ISR (razão) — SA"

### Passo 3: Testar
- [ ] Criar um card com `[ISR (SA)]`
- [ ] Adicionar slicer de mês/ano
- [ ] Verificar valor para Jul/2025 = 1.29
- [ ] Verificar BLANK para mês futuro (Ago/2025)

### Passo 4: Criar Tooltip Personalizado
- [ ] Adicionar texto: "Razão estoque/vendas ajustada sazonalmente"
- [ ] Adicionar nota: "Não agregar entre meses"

---

## ⚠️ Erros Comuns e Soluções

### Erro 1: "Valor muito alto (ex: 12.9 em vez de 1.29)"
**Causa**: Formatou como Percentage em vez de Number
**Solução**: Mudar formato para Number (não Percentage)

### Erro 2: "Soma incorreta ao selecionar múltiplos meses"
**Causa**: SUM() agregou valores de vários meses
**Solução**: Usar filtro para 1 mês específico. ISR não é cumulativo.

### Erro 3: "Medida retorna BLANK sempre"
**Causa**: Relacionamento inativo ou filtro errado
**Solução**:
1. Verificar relacionamento dimmonth ↔ FactRETAILIRSA ativo
2. Verificar filtro de data no range Jan/1992 - Jul/2025

### Erro 4: "Valor diferente do CSV"
**Causa**: Filtros adicionais ativos (categoria, loja, etc.)
**Solução**: ISR é série nacional única. Remover filtros que não sejam data.

---

## 📚 Dependências

**Nenhuma medida dependente** - ISR (SA) é calculada diretamente da tabela.

**Tabelas necessárias**:
- `FactRETAILIRSA` (obrigatório)
- `dimmonth` (opcional, para relacionamento temporal)

**Colunas usadas**:
- `FactRETAILIRSA[ISR_SA]` (decimal)

---

## 📈 Estatísticas de Referência

### Série Completa (Jan/1992 - Jul/2025)
- **Total de meses**: 403
- **Média**: 1.49
- **Mediana**: 1.49
- **Mínimo**: 1.09 (Jun/2021)
- **Máximo**: 1.75 (Abr/1995)
- **Desvio padrão**: ~0.15
- **NULL/BLANK**: 0

### Faixas Históricas
- **Anos 1990s**: 1.50 - 1.75 (estoques mais altos)
- **Anos 2000s**: 1.30 - 1.60 (normalização)
- **Anos 2010s**: 1.30 - 1.50 (eficiência supply chain)
- **2020-2021**: 1.09 - 1.35 (pandemia - demanda volátil)
- **2022-2025**: 1.29 - 1.35 (equilíbrio atual)

---

**Criado em**: 2025-11-17
**Arquivo de referência**: PILLAR_B_ISR_SA_SETUP.md
**QA validado**: 3 meses, erro 0.00
**Fonte**: FRED Series RETAILIRSA
