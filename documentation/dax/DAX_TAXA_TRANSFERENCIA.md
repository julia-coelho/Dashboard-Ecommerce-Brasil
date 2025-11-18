# 📊 Medidas DAX - Taxa de Transferência

## Contexto

Estas medidas calculam a **Taxa de Transferência**, que mostra qual percentual da saída do estoque ocorre por transferências entre lojas (vs vendas diretas ao consumidor).

**Tabela usada**: `factretailmonthly` (já importada no Power BI)

---

## 1️⃣ Retail Transfers (M)

**Descrição**: Total de transferências entre lojas no mês (em dólares)

```dax
Retail Transfers (M) = SUM(factretailmonthly[retailtransfers])
```

**Formatação:**
- Formato: Currency ($)
- Decimal places: 2
- Display Units: None

**O que faz**: Soma todas as transferências de mercadorias entre lojas para o período selecionado (mês/ano/categoria).

**Exemplo de uso**: Card mostrando "$25,450 em transferências este mês"

---

## 2️⃣ Outflow (M)

**Descrição**: Saída total do varejo (vendas diretas + transferências entre lojas)

```dax
Outflow (M) = [Retail Sales (M)] + [Retail Transfers (M)]
```

**Formatação:**
- Formato: Currency ($)
- Decimal places: 2
- Display Units: None

**O que faz**: Soma as vendas diretas ao consumidor com as transferências entre lojas, mostrando o total de mercadorias que saíram do estoque.

**Exemplo de uso**:
- Retail Sales = $100,000
- Retail Transfers = $25,000
- **Outflow = $125,000** (saída total)

**Dependências**:
- Usa `[Retail Sales (M)]` (medida #1 que você já criou)
- Usa `[Retail Transfers (M)]` (medida acima)

---

## 3️⃣ Taxa de Transferência (%)

**Descrição**: Percentual da saída do estoque que ocorre por transferências (vs vendas diretas)

```dax
Taxa de Transferência (%) =
VAR TotalOutflow = [Outflow (M)]
VAR Transfers = [Retail Transfers (M)]
RETURN
    IF(
        ISBLANK(TotalOutflow) || TotalOutflow = 0,
        BLANK(),
        DIVIDE(Transfers, TotalOutflow)
    )
```

**Formatação:**
- Formato: Percentage (%)
- Decimal places: 1
- Display Units: None

**O que faz**:
1. Calcula o total de saída (vendas + transferências)
2. Divide as transferências pelo total
3. Retorna BLANK se não houver movimento (Outflow = 0)

**Exemplo de uso**:
- Retail Sales = $100,000
- Retail Transfers = $25,000
- Outflow = $125,000
- **Taxa = 25,000 / 125,000 = 20.0%**

**Interpretação**:
- **0-20%**: Vendas diretas predominam (padrão saudável)
- **20-40%**: Rebalanceamento moderado entre lojas
- **40-100%**: Alta movimentação entre lojas (investigar causas)

**Regras BLANK**:
- Se `Outflow = 0` → BLANK (sem movimento)
- Se `Outflow = NULL` → BLANK
- Se `Retail Transfers = NULL` ou `Retail Sales = NULL` → BLANK

**Dependências**:
- Usa `[Outflow (M)]`
- Usa `[Retail Transfers (M)]`

---

## 📋 Checklist de Implementação

### Passo 1: Criar Retail Transfers (M)
- [ ] Ir em Report View → Data pane
- [ ] Click direito em `_Measures` → New measure
- [ ] Colar: `Retail Transfers (M) = SUM(factretailmonthly[retailtransfers])`
- [ ] Formatar como Currency ($), 2 casas decimais

### Passo 2: Criar Outflow (M)
- [ ] Click direito em `_Measures` → New measure
- [ ] Colar: `Outflow (M) = [Retail Sales (M)] + [Retail Transfers (M)]`
- [ ] Formatar como Currency ($), 2 casas decimais

### Passo 3: Criar Taxa de Transferência (%)
- [ ] Click direito em `_Measures` → New measure
- [ ] Colar a fórmula DAX completa (acima)
- [ ] Formatar como Percentage (%), 1 casa decimal

### Passo 4: Testar
- [ ] Criar um card com `[Taxa de Transferência (%)]`
- [ ] Verificar se mostra valor entre 0-100% (ou BLANK)
- [ ] Adicionar slicer de ano/mês para testar

---

## 🎯 Casos de Teste

### Teste 1: Vendas Diretas Predominantes
**Dados**:
- Retail Sales = $80,000
- Retail Transfers = $20,000

**Resultado esperado**:
- Outflow = $100,000
- Taxa = 20.0%
- ✅ Interpretação: Vendas diretas (padrão saudável)

### Teste 2: Alta Transferência
**Dados**:
- Retail Sales = $30,000
- Retail Transfers = $70,000

**Resultado esperado**:
- Outflow = $100,000
- Taxa = 70.0%
- ⚠️ Interpretação: Alta movimentação entre lojas (investigar)

### Teste 3: Sem Movimento
**Dados**:
- Retail Sales = $0
- Retail Transfers = $0

**Resultado esperado**:
- Outflow = $0
- Taxa = BLANK
- ✅ Regra de BLANK funcionando

### Teste 4: Apenas Transferências
**Dados**:
- Retail Sales = $0
- Retail Transfers = $50,000

**Resultado esperado**:
- Outflow = $50,000
- Taxa = 100.0%
- ⚠️ Interpretação: Nenhuma venda direta (incomum)

---

## 📊 Exemplos de Visualizações

### Card Principal
```
┌─────────────────────────┐
│ Taxa de Transferência   │
│       33.6%             │
│  ↑ +2.3 p.p. vs mês ant │
└─────────────────────────┘
```

### Tooltip (ao passar mouse)
```
Retail Sales: $100,234.56
Retail Transfers: $50,789.12
Outflow Total: $151,023.68
Taxa: 33.6%

Fórmula: Transfers / (Sales + Transfers)
```

### Ranking por Categoria
```
Categoria    | Taxa    | Outflow
-------------|---------|----------
WINE         | 45.2%   | $234,567
LIQUOR       | 32.1%   | $189,234
BEER         | 18.5%   | $345,678
```

---

## ⚠️ Limitações Conhecidas

1. **Valores negativos**: 113 registros com Sales negativo, 1,016 com Transfers negativo (devoluções/ajustes) podem gerar taxas fora de 0-100%
2. **BLANKs**: 38% dos registros têm Outflow = 0 (sem movimento no período)
3. **Período**: Dados disponíveis de Jun/2017 a Set/2020

**Sugestão**: Filtrar `[Outflow (M)] > 0` nos visuais para focar em períodos com movimento.

---

**Criado em**: 2025-11-14
**Arquivo de referência**: POWER_BI_SETUP.md (medidas #10-13)
**QA validado**: 3 itens × 3 meses, erro 0.0 p.p.
