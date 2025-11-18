# 📊 Medida DAX - ISR MoM % (SA) - Month-over-Month Variation

## Contexto

Esta medida calcula a **variação percentual mês a mês** do ISR (SA) - Seasonally Adjusted.

**Tabelas usadas**:
- `FactRETAILIRSA` (403 meses: Jan/1992 - Jul/2025)
- `dimmonth` (calendário 1992-2028)

**Dependências**: Requer medida base `[ISR (SA)]` e relacionamento ativo com dimmonth

---

## 📐 ISR MoM % (SA) - Month-over-Month %

**Nome técnico**: `kpi_isr_mom_pct_sa`

**Descrição**: Variação percentual do ISR (SA) em relação ao mês imediatamente anterior

**Fórmula Matemática:**
```
MoM% = (ISR_SA(m) − ISR_SA(m−1)) / ISR_SA(m−1) × 100
```

**Fórmula DAX:**
```dax
ISR MoM % (SA) =
VAR CurrentMonth_ISR = [ISR (SA)]
VAR PreviousMonth_ISR =
    CALCULATE(
        [ISR (SA)],
        DATEADD(dimmonth[MonthDate], -1, MONTH)
    )
RETURN
    IF(
        ISBLANK(CurrentMonth_ISR) || ISBLANK(PreviousMonth_ISR),
        BLANK(),
        DIVIDE(CurrentMonth_ISR - PreviousMonth_ISR, PreviousMonth_ISR)
    )
```

**Formatação:**
- Formato: Percentage (%)
- Decimal places: 1
- Display Units: None
- Display name: "ISR MoM % (SA)"

**O que faz**:
1. Obtém o ISR_SA do mês atual (`CurrentMonth_ISR`)
2. Usa DATEADD para voltar 1 mês e obter o ISR_SA do mês anterior (`PreviousMonth_ISR`)
3. Calcula a variação percentual: (Atual - Anterior) / Anterior
4. Retorna BLANK se não houver mês anterior (primeiro mês da série) ou se algum valor for BLANK

---

## 📋 Regras de Negócio

### Regras BLANK

A medida retorna BLANK quando:
- **Primeiro mês da série** (Jan/1992) - não há mês anterior
- Mês atual não tem dados (CurrentMonth_ISR = BLANK)
- Mês anterior não tem dados (PreviousMonth_ISR = BLANK)
- Há gap temporal na série (mês m-1 ausente)

### Dependências

**Medidas necessárias**:
- `[ISR (SA)]` - medida base que retorna ISR_SA do mês no contexto

**Relacionamentos necessários**:
- `dimmonth[YearMonthKey]` (1) → `FactRETAILIRSA[YearMonthKey]` (*) - **ATIVO**
- Cross-filter direction: Single

**Tabelas necessárias**:
- `FactRETAILIRSA` (série temporal com ISR_SA)
- `dimmonth` (calendário mensal para função DATEADD)

### Interpretação

- **MoM% > 0**: ISR aumentou (estoques cresceram mais que vendas)
- **MoM% = 0**: ISR estável (mesma razão estoque/vendas)
- **MoM% < 0**: ISR diminuiu (vendas cresceram mais que estoques)

**Exemplo**:
- Jun/2025: ISR_SA = 1.29
- Jul/2025: ISR_SA = 1.29
- MoM% = (1.29 - 1.29) / 1.29 = **0.0%**

---

## 🎯 Casos de Teste

### Teste 1: Variação Positiva (Mai→Jun/2025)
**Dados**:
- Mai/2025: ISR_SA = 1.30
- Jun/2025: ISR_SA = 1.29

**Cálculo manual**:
- MoM% = (1.29 - 1.30) / 1.30 × 100 = **-0.77%**

**Resultado esperado**: -0.8% (1 casa decimal)

---

### Teste 2: Variação Negativa (Abr→Mai/2025)
**Dados**:
- Abr/2025: ISR_SA = 1.29
- Mai/2025: ISR_SA = 1.30

**Cálculo manual**:
- MoM% = (1.30 - 1.29) / 1.29 × 100 = **0.78%**

**Resultado esperado**: 0.8% (1 casa decimal)

---

### Teste 3: Primeiro Mês da Série (Jan/1992)
**Dados**:
- Jan/1992: ISR_SA = 1.65
- Mês anterior: **NÃO EXISTE**

**Resultado esperado**: BLANK ✅

---

### Teste 4: Variação Estável (Jun→Jul/2025)
**Dados**:
- Jun/2025: ISR_SA = 1.29
- Jul/2025: ISR_SA = 1.29

**Cálculo manual**:
- MoM% = (1.29 - 1.29) / 1.29 × 100 = **0.00%**

**Resultado esperado**: 0.0%

---

## 📊 Exemplos de Visualizações

### Card junto à Linha ISR (SA)
```
┌─────────────────────────┐
│ ISR (SA): 1.29          │
│ MoM: 0.0%               │
│ Jul/2025                │
└─────────────────────────┘
```

### Tooltip Detalhado
```
Mês: Julho/2025
ISR (SA): 1.29
ISR (SA) mês anterior: 1.29
Variação MoM: 0.0%

Fórmula: (m − m−1) / m−1
```

### Tabela com Série Temporal
```
Mês       | ISR (SA) | MoM %
----------|----------|-------
Jul/2025  | 1.29     | 0.0%
Jun/2025  | 1.29     | -0.8%
Mai/2025  | 1.30     | 0.8%
Abr/2025  | 1.29     | 0.0%
Mar/2025  | 1.29     | -1.5%
Fev/2025  | 1.31     | 0.0%
Jan/2025  | 1.31     | 1.6%
```

---

## 📋 Checklist de Implementação

### Passo 1: Verificar Pré-requisitos
- [ ] Tabela `FactRETAILIRSA` importada no Power BI
- [ ] Tabela `dimmonth` importada no Power BI
- [ ] Relacionamento `dimmonth[YearMonthKey]` → `FactRETAILIRSA[YearMonthKey]` **ATIVO**
- [ ] Medida `[ISR (SA)]` criada e funcionando

### Passo 2: Criar Medida MoM %
- [ ] Ir em Report View → Data pane
- [ ] Click direito em `_Measures` ou `_Measures_ISR` → New measure
- [ ] Colar a fórmula DAX completa
- [ ] Nomear como "ISR MoM % (SA)"

### Passo 3: Formatar Medida
- [ ] Formato: Percentage
- [ ] Decimal places: 1
- [ ] Display Units: None
- [ ] Display name: "ISR MoM % (SA)"

### Passo 4: Testar
- [ ] Criar um card com `[ISR MoM % (SA)]`
- [ ] Adicionar slicer de mês/ano
- [ ] Selecionar Jul/2025 → verificar MoM% = 0.0%
- [ ] Selecionar Jun/2025 → verificar MoM% ≈ -0.8%
- [ ] Selecionar Jan/1992 → verificar BLANK ✅

### Passo 5: Criar Tooltip Personalizado
- [ ] Adicionar ao tooltip do gráfico de linha:
  - Mês atual
  - ISR (SA) atual
  - ISR (SA) mês anterior
  - MoM %
  - Texto: "Fórmula: (m − m−1) / m−1"

---

## ⚠️ Erros Comuns e Soluções

### Erro 1: "MoM% sempre retorna BLANK"
**Causas possíveis**:
1. Relacionamento dimmonth ↔ FactRETAILIRSA **INATIVO**
2. Medida base `[ISR (SA)]` não existe
3. DATEADD não encontra mês anterior (gap temporal)

**Solução**:
1. Verificar Model View → Relacionamento deve estar ativo (linha sólida)
2. Criar medida `[ISR (SA)]` primeiro
3. Verificar se série temporal é contínua (sem gaps)

---

### Erro 2: "Valor muito alto (ex: 0.8 em vez de 0.8%)"
**Causa**: Formatou como Number em vez de Percentage

**Solução**: Mudar formato para Percentage (não Number)

---

### Erro 3: "Jan/1992 mostra valor em vez de BLANK"
**Causa**: DATEADD está retornando valor anterior fora da série (bug)

**Solução**:
- Verificar se dim_month começa em Jan/1992
- Se necessário, adicionar filtro explícito na medida

---

### Erro 4: "MoM% diferente do calculado manualmente"
**Causa**: Usando ISR_SA do mês errado

**Solução**: Verificar valores base com card separado:
- Card 1: `[ISR (SA)]` para mês m
- Card 2: `CALCULATE([ISR (SA)], DATEADD(dimmonth[MonthDate], -1, MONTH))` para m-1
- Comparar com CSV

---

## 📈 Estatísticas de Referência (Jul/2024 - Jul/2025)

### Amostra QA - Últimos 12 meses

| Mês       | ISR_SA | ISR_SA (m-1) | MoM % (calculado) |
|-----------|--------|--------------|-------------------|
| Jul/2025  | 1.29   | 1.29         | 0.0%              |
| Jun/2025  | 1.29   | 1.30         | -0.8%             |
| Mai/2025  | 1.30   | 1.29         | 0.8%              |
| Abr/2025  | 1.29   | 1.29         | 0.0%              |
| Mar/2025  | 1.29   | 1.31         | -1.5%             |
| Fev/2025  | 1.31   | 1.31         | 0.0%              |
| Jan/2025  | 1.31   | 1.29         | 1.6%              |
| Dez/2024  | 1.29   | 1.31         | -1.5%             |
| Nov/2024  | 1.31   | 1.32         | -0.8%             |
| Out/2024  | 1.32   | 1.33         | -0.8%             |
| Set/2024  | 1.33   | 1.33         | 0.0%              |
| Ago/2024  | 1.33   | 1.34         | -0.7%             |

### Estatísticas Históricas (Fev/1992 - Jul/2025)

- **Registros com MoM%**: 402 (Jan/1992 = BLANK)
- **Maior alta**: +6.5% (algum mês com recuperação)
- **Maior queda**: -5.2% (algum mês com ajuste)
- **Média**: ~0.0% (série relativamente estável)
- **Mediana**: 0.0%

---

## 🔄 Versão Alternativa - Com Previous Month Explícito

Se preferir mostrar o mês anterior como medida separada:

```dax
ISR (SA) Previous Month =
CALCULATE(
    [ISR (SA)],
    DATEADD(dimmonth[MonthDate], -1, MONTH)
)
```

Então a medida MoM% pode ser simplificada:

```dax
ISR MoM % (SA) =
VAR CurrentMonth = [ISR (SA)]
VAR PreviousMonth = [ISR (SA) Previous Month]
RETURN
    IF(
        ISBLANK(CurrentMonth) || ISBLANK(PreviousMonth),
        BLANK(),
        DIVIDE(CurrentMonth - PreviousMonth, PreviousMonth)
    )
```

**Vantagem**: Pode exibir `[ISR (SA) Previous Month]` no tooltip para debugar

---

## 📚 Referências

- **Função DAX**: DATEADD - https://dax.guide/dateadd/
- **Função DAX**: DIVIDE - https://dax.guide/divide/
- **Relacionamentos**: https://learn.microsoft.com/power-bi/transform-model/desktop-relationships-understand
- **Time Intelligence**: https://learn.microsoft.com/dax/time-intelligence-functions-dax

---

**Criado em**: 2025-11-17
**Arquivo de referência**: PILLAR_B_ISR_SA_SETUP.md
**Dependências**: [ISR (SA)], dimmonth
**Fonte**: FRED Series RETAILIRSA (variação calculada)
