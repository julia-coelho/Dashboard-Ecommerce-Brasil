# 📊 Medida DAX - ISR YoY % (SA) - Year-over-Year Variation

## Contexto

Esta medida calcula a **variação percentual ano a ano** do ISR (SA) - comparando com o mesmo mês do ano anterior.

**Tabelas usadas**:
- `FactRETAILIRSA` (403 meses: Jan/1992 - Jul/2025)
- `dimmonth` (calendário 1992-2028)

**Dependências**: Requer medida base `[ISR (SA)]` e relacionamento ativo com dimmonth

---

## 📐 ISR YoY % (SA) - Year-over-Year %

**Nome técnico**: `kpi_isr_yoy_pct_sa`

**Descrição**: Variação percentual do ISR (SA) em relação ao mesmo mês do ano anterior (12 meses atrás)

**Fórmula Matemática:**
```
YoY% = (ISR_SA(m) − ISR_SA(m−12)) / ISR_SA(m−12) × 100
```

**Fórmula DAX:**
```dax
ISR YoY % (SA) =
VAR CurrentMonth_ISR = [ISR (SA)]
VAR SameMonthLastYear_ISR =
    CALCULATE(
        [ISR (SA)],
        DATEADD(dimmonth[MonthDate], -12, MONTH)
    )
RETURN
    IF(
        ISBLANK(CurrentMonth_ISR) || ISBLANK(SameMonthLastYear_ISR),
        BLANK(),
        DIVIDE(CurrentMonth_ISR - SameMonthLastYear_ISR, SameMonthLastYear_ISR)
    )
```

**Formatação:**
- Formato: Percentage (%)
- Decimal places: 1
- Display Units: None
- Display name: "ISR YoY % (SA)"

**O que faz**:
1. Obtém o ISR_SA do mês atual (`CurrentMonth_ISR`)
2. Usa DATEADD com -12 meses para obter o ISR_SA do mesmo mês do ano anterior (`SameMonthLastYear_ISR`)
3. Calcula a variação percentual: (Atual - Ano Anterior) / Ano Anterior
4. Retorna BLANK se não houver 12 meses de histórico ou se algum valor for BLANK

---

## 📋 Regras de Negócio

### Regras BLANK

A medida retorna BLANK quando:
- **Primeiros 12 meses da série** (Jan/1992 - Dez/1992) - não há 12 meses de histórico
- Mês atual não tem dados (CurrentMonth_ISR = BLANK)
- Mês m-12 não tem dados (SameMonthLastYear_ISR = BLANK)
- Há gap temporal na série (mês m-12 ausente)

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

- **YoY% > 0**: ISR aumentou em relação ao ano anterior (estoques cresceram mais que vendas)
- **YoY% = 0**: ISR estável ano a ano
- **YoY% < 0**: ISR diminuiu em relação ao ano anterior (vendas cresceram mais que estoques)

**Vantagem da comparação YoY**:
- Elimina efeitos sazonais (compara meses equivalentes)
- Mostra tendências de longo prazo
- Útil para séries com forte sazonalidade

**Exemplo**:
- Jul/2024: ISR_SA = 1.34
- Jul/2025: ISR_SA = 1.29
- YoY% = (1.29 - 1.34) / 1.34 = **-3.73%**

---

## 🎯 Casos de Teste

### Teste 1: Variação Negativa (Jul/2024 → Jul/2025)
**Dados**:
- Jul/2024: ISR_SA = 1.34
- Jul/2025: ISR_SA = 1.29

**Cálculo manual**:
- YoY% = (1.29 - 1.34) / 1.34 × 100 = **-3.73%**

**Resultado esperado**: -3.7% (1 casa decimal)

---

### Teste 2: Variação Positiva (Jun/2024 → Jun/2025)
**Dados**:
- Jun/2024: ISR_SA = 1.32
- Jun/2025: ISR_SA = 1.29

**Cálculo manual**:
- YoY% = (1.29 - 1.32) / 1.32 × 100 = **-2.27%**

**Resultado esperado**: -2.3% (1 casa decimal)

---

### Teste 3: Primeiros 12 Meses (Jan-Dez/1992)
**Dados**:
- Jan/1992: ISR_SA = 1.65
- Mês m-12: **NÃO EXISTE**

**Resultado esperado**: BLANK ✅

**Observação**: Todos os meses de 1992 devem retornar BLANK (não há ano anterior)

---

### Teste 4: Primeiro mês com YoY (Jan/1993)
**Dados**:
- Jan/1992: ISR_SA = 1.65
- Jan/1993: ISR_SA = 1.69

**Cálculo manual**:
- YoY% = (1.69 - 1.65) / 1.65 × 100 = **+2.42%**

**Resultado esperado**: 2.4% (1 casa decimal)

---

## 📊 Exemplos de Visualizações

### Card junto à Linha ISR (SA)
```
┌─────────────────────────┐
│ ISR (SA): 1.29          │
│ YoY: -3.7%              │
│ Jul/2025                │
└─────────────────────────┘
```

### Tooltip Detalhado
```
Mês: Julho/2025
ISR (SA): 1.29
ISR (SA) ano anterior: 1.34 (Jul/2024)
Variação YoY: -3.7%

Fórmula: (m − m−12) / m−12
Nota: Compara meses equivalentes (controle de sazonalidade)
```

### Tabela com Comparação Anual
```
Mês       | ISR (SA) | ISR (SA) Ano Ant. | YoY %
----------|----------|-------------------|--------
Jul/2025  | 1.29     | 1.34              | -3.7%
Jun/2025  | 1.29     | 1.32              | -2.3%
Mai/2025  | 1.30     | 1.33              | -2.3%
Abr/2025  | 1.29     | 1.32              | -2.3%
Mar/2025  | 1.29     | 1.32              | -2.3%
```

---

## 📋 Checklist de Implementação

### Passo 1: Verificar Pré-requisitos
- [ ] Tabela `FactRETAILIRSA` importada no Power BI
- [ ] Tabela `dimmonth` importada no Power BI
- [ ] Relacionamento `dimmonth[YearMonthKey]` → `FactRETAILIRSA[YearMonthKey]` **ATIVO**
- [ ] Medida `[ISR (SA)]` criada e funcionando

### Passo 2: Criar Medida YoY %
- [ ] Ir em Report View → Data pane
- [ ] Click direito em `_Measures` ou `_Measures_ISR` → New measure
- [ ] Colar a fórmula DAX completa
- [ ] Nomear como "ISR YoY % (SA)"

### Passo 3: Formatar Medida
- [ ] Formato: Percentage
- [ ] Decimal places: 1
- [ ] Display Units: None
- [ ] Display name: "ISR YoY % (SA)"

### Passo 4: Testar
- [ ] Criar um card com `[ISR YoY % (SA)]`
- [ ] Adicionar slicer de mês/ano
- [ ] Selecionar Jul/2025 → verificar YoY% ≈ -3.7%
- [ ] Selecionar Jan/1992 → verificar BLANK ✅
- [ ] Selecionar Jan/1993 → verificar YoY% ≈ +2.4%

### Passo 5: Criar Tooltip Personalizado
- [ ] Adicionar ao tooltip do gráfico de linha:
  - Mês atual
  - ISR (SA) atual
  - ISR (SA) ano anterior (m-12)
  - YoY %
  - Texto: "Fórmula: (m − m−12) / m−12"
  - Nota: "Compara meses equivalentes"

---

## ⚠️ Erros Comuns e Soluções

### Erro 1: "YoY% sempre retorna BLANK"
**Causas possíveis**:
1. Relacionamento dimmonth ↔ FactRETAILIRSA **INATIVO**
2. Medida base `[ISR (SA)]` não existe
3. DATEADD não encontra mês m-12 (gap temporal ou série muito curta)

**Solução**:
1. Verificar Model View → Relacionamento deve estar ativo (linha sólida)
2. Criar medida `[ISR (SA)]` primeiro
3. Verificar se série tem pelo menos 13 meses de dados

---

### Erro 2: "Primeiros 12 meses não retornam BLANK"
**Causa**: Série temporal inclui dados anteriores a Jan/1992

**Solução**: Verificar que FactRETAILIRSA começa em Jan/1992. Se houver dados anteriores, eles serão usados para YoY.

---

### Erro 3: "YoY% diferente do calculado manualmente"
**Causa**: Usando ISR_SA do mês errado

**Solução**: Verificar valores base com cards separados:
- Card 1: `[ISR (SA)]` para mês m
- Card 2: `CALCULATE([ISR (SA)], DATEADD(dimmonth[MonthDate], -12, MONTH))` para m-12
- Comparar com CSV

---

### Erro 4: "Valor muito alto (ex: 3.7 em vez de 3.7%)"
**Causa**: Formatou como Number em vez de Percentage

**Solução**: Mudar formato para Percentage (não Number)

---

## 📈 Estatísticas de Referência (Jul/2024 - Jul/2025)

### Amostra QA - Últimos 12 meses

| Mês       | ISR_SA (m) | ISR_SA (m-12) | YoY % (calculado) |
|-----------|------------|---------------|-------------------|
| Jul/2025  | 1.29       | 1.34          | -3.73%            |
| Jun/2025  | 1.29       | 1.32          | -2.27%            |
| Mai/2025  | 1.30       | 1.33          | -2.26%            |
| Abr/2025  | 1.29       | 1.32          | -2.27%            |
| Mar/2025  | 1.29       | 1.32          | -2.27%            |
| Fev/2025  | 1.31       | 1.31          | 0.00%             |
| Jan/2025  | 1.31       | 1.30          | +0.77%            |
| Dez/2024  | 1.29       | 1.29          | 0.00%             |
| Nov/2024  | 1.31       | 1.29          | +1.55%            |
| Out/2024  | 1.32       | 1.28          | +3.13%            |
| Set/2024  | 1.33       | 1.29          | +3.10%            |
| Ago/2024  | 1.33       | 1.27          | +4.72%            |

### Estatísticas Históricas (Jan/1993 - Jul/2025)

- **Registros com YoY%**: 391 (12 meses de 1992 = BLANK)
- **Maior alta YoY**: Depende da volatilidade histórica
- **Maior queda YoY**: Depende da volatilidade histórica
- **Média**: ~0.0% (série tende ao equilíbrio)

---

## 🔄 Versão Alternativa - Com Same Month Last Year Explícito

Se preferir mostrar o valor do ano anterior como medida separada:

```dax
ISR (SA) Same Month Last Year =
CALCULATE(
    [ISR (SA)],
    DATEADD(dimmonth[MonthDate], -12, MONTH)
)
```

Então a medida YoY% pode ser simplificada:

```dax
ISR YoY % (SA) =
VAR CurrentMonth = [ISR (SA)]
VAR LastYear = [ISR (SA) Same Month Last Year]
RETURN
    IF(
        ISBLANK(CurrentMonth) || ISBLANK(LastYear),
        BLANK(),
        DIVIDE(CurrentMonth - LastYear, LastYear)
    )
```

**Vantagem**: Pode exibir `[ISR (SA) Same Month Last Year]` no tooltip para comparação direta

---

## 🆚 Comparação: YoY % vs MoM %

| Aspecto | MoM % | YoY % |
|---------|-------|-------|
| **Offset** | 1 mês | 12 meses |
| **Compara** | Mês anterior | Mesmo mês ano anterior |
| **Elimina sazonalidade** | ❌ Não | ✅ Sim |
| **Detecta tendência curto prazo** | ✅ Sim | ❌ Não |
| **Detecta tendência longo prazo** | ❌ Não | ✅ Sim |
| **Primeiro valor BLANK** | Jan/1992 | Jan-Dez/1992 (12 meses) |
| **Uso típico** | Volatilidade mensal | Crescimento anual |

**Recomendação**: Usar **ambas** para análise completa:
- **MoM %**: Tendência de curto prazo, volatilidade mensal
- **YoY %**: Tendência de longo prazo, crescimento anual sem sazonalidade

---

## 📚 Referências

- **Função DAX**: DATEADD - https://dax.guide/dateadd/
- **Função DAX**: DIVIDE - https://dax.guide/divide/
- **Time Intelligence**: https://learn.microsoft.com/dax/time-intelligence-functions-dax
- **Year-over-Year Analysis**: Best practices para análise temporal

---

**Criado em**: 2025-11-17
**Arquivo de referência**: PILLAR_B_ISR_SA_SETUP.md
**Dependências**: [ISR (SA)], dimmonth
**Fonte**: FRED Series RETAILIRSA (variação calculada)
**Complementar a**: DAX_ISR_MOM.md (MoM %)
