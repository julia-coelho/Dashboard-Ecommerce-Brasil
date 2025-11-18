# Modelo de Dados - Pilar B (Macro/Estratégico)

## Diagrama de Relacionamento

```
┌─────────────────────────────────────┐
│         dimmonth                    │
│  (Tabela de Calendário/Dimensão)    │
├─────────────────────────────────────┤
│ PK: yearmonthkey (VARCHAR) ⚠️       │
│     monthdate (DATE)                │
│     year (INT)                      │
│     monthnumber (INT)               │
│     monthnamept (VARCHAR)           │
│     yearmonth (VARCHAR)             │
│     daysinmonth (INT)               │
│     startofmonth (DATE)             │
│     endofmonth (DATE)               │
└─────────────────────────────────────┘
           │
           │ Relacionamento: dimmonth[yearmonthkey] (VARCHAR)
           │                     ↓
           │            factXXX[yearmonthkey] (INTEGER)
           │
           │ ⚠️ PROBLEMA: Tipos incompatíveis!
           │    dimmonth.yearmonthkey = VARCHAR ('199201')
           │    fact tables.yearmonthkey = INTEGER (199201)
           │
    ┌──────┴───────┐
    │              │
    ▼              ▼
┌─────────────────────────────┐  ┌─────────────────────────────────┐
│   factretailirsa            │  │   factisrseasonalgap            │
│   (Tabela Fato - ISR SA)    │  │   (Tabela Fato - SA + NSA)      │
├─────────────────────────────┤  ├─────────────────────────────────┤
│ PK: yearmonthkey (INTEGER)  │  │ PK: yearmonthkey (INTEGER)      │
│     monthdate (DATE)        │  │     monthdate (DATE)            │
│     isr_sa (NUMERIC)        │  │     isr_sa (NUMERIC)            │
│                             │  │     isr_nsa (NUMERIC)           │
│                             │  │     gap_abs (NUMERIC)           │
│                             │  │     gap_pct (NUMERIC)           │
└─────────────────────────────┘  └─────────────────────────────────┘
  403 registros                    403 registros
  Jan/1992 - Jul/2025              Jan/1992 - Jul/2025
```

---

## Tabelas e Relacionamentos

### 1. dimmonth (Dimensão Calendário)
**Tipo:** Tabela de dimensão temporal
**Registros:** 444 meses (Jan/1992 - Dez/2028)
**Chave Primária:** `yearmonthkey` (VARCHAR) - formato "YYYYMM" (ex: "199201")

**Colunas:**
- `yearmonthkey` (VARCHAR): Chave no formato texto "YYYYMM"
- `monthdate` (DATE): Primeiro dia do mês
- `year` (INTEGER): Ano
- `monthnumber` (INTEGER): Número do mês (1-12)
- `monthnamept` (VARCHAR): Nome do mês em português
- `yearmonth` (VARCHAR): "Ano-Mês" (ex: "1992-01")
- `daysinmonth` (INTEGER): Dias no mês (28-31)
- `startofmonth` (DATE): Início do mês (sempre dia 01)
- `endofmonth` (DATE): Último dia do mês

**Uso:** Filtros de tempo, slicers, contexto temporal

---

### 2. factretailirsa (Fato - ISR SA)
**Tipo:** Tabela fato (série temporal macro)
**Registros:** 403 meses (Jan/1992 - Jul/2025)
**Chave Primária:** `yearmonthkey` (INTEGER) - formato numérico YYYYMM (ex: 199201)

**Colunas:**
- `monthdate` (DATE): Data do mês (sempre dia 01)
- `yearmonthkey` (INTEGER): Chave numérica YYYYMM
- `isr_sa` (NUMERIC): ISR Seasonally Adjusted

**KPIs Derivados:**
- ISR (SA) - KPI #1
- ISR MoM % (SA) - KPI #1.1
- ISR YoY % (SA) - KPI #1.2

**Fonte:** FRED Series `RETAILIRSA`

---

### 3. factisrseasonalgap (Fato - SA + NSA + Gap)
**Tipo:** Tabela fato (série temporal macro + análise sazonal)
**Registros:** 403 meses (Jan/1992 - Jul/2025)
**Chave Primária:** `yearmonthkey` (INTEGER) - formato numérico YYYYMM (ex: 199201)

**Colunas:**
- `monthdate` (DATE): Data do mês (sempre dia 01)
- `yearmonthkey` (INTEGER): Chave numérica YYYYMM
- `isr_sa` (NUMERIC): ISR Seasonally Adjusted
- `isr_nsa` (NUMERIC): ISR Not Seasonally Adjusted
- `gap_abs` (NUMERIC): Gap absoluto (SA - NSA)
- `gap_pct` (NUMERIC): Gap percentual ((SA - NSA) / NSA × 100)

**KPIs Derivados:**
- ISR (SA) - Componente Seasonal Gap - KPI #2
- ISR (NSA) - KPI #3 / #1.6 (Overlay/Toggle)
- ISR Seasonal Gap (Absoluto) - KPI #4
- ISR Seasonal Gap (Percentual) - KPI #5
- ISR Percentil 10 anos - KPI #1.5

**Fontes:** FRED Series `RETAILIRSA` + `RETAILIRNSA`

---

## ⚠️ PROBLEMA: Incompatibilidade de Tipos

### Situação Atual:
- **dimmonth.yearmonthkey** = VARCHAR ("199201")
- **factretailirsa.yearmonthkey** = INTEGER (199201)
- **factisrseasonalgap.yearmonthkey** = INTEGER (199201)

### Impacto no Power BI:
❌ **Relacionamento NÃO funcionará automaticamente**
- Power BI não cria relacionamento entre VARCHAR e INTEGER
- Tipos devem ser idênticos

### Soluções:

#### **Opção 1: Converter em Power Query (Recomendado para início rápido)**
No Power BI, ao importar `dimmonth`:
```m
// Power Query - Converter yearmonthkey para INT
= Table.TransformColumnTypes(
    dimmonth,
    {{"yearmonthkey", Int64.Type}}
)
```

#### **Opção 2: Corrigir no Neon (Recomendado para produção)**
```sql
-- Converter dimmonth.yearmonthkey de VARCHAR para INTEGER
ALTER TABLE dimmonth
ALTER COLUMN yearmonthkey TYPE INTEGER
USING yearmonthkey::INTEGER;
```

#### **Opção 3: Usar MonthDate como chave (Alternativa)**
- Relacionamento via `dimmonth[monthdate]` ↔ `factXXX[monthdate]`
- Ambos são DATE (tipos compatíveis)
- **Desvantagem:** YearMonthKey é mais eficiente como chave

---

## Cardinalidade dos Relacionamentos

### Se Relacionamentos forem criados:

```
dimmonth (1) ───< (*) factretailirsa
   │
   └───< (*) factisrseasonalgap
```

**Tipo:** One-to-Many (1:*)
- 1 mês em `dimmonth` → Muitos registros em fact tables (na prática, 1:1 neste caso)
- **Direção do filtro:** Bidirecional NÃO necessária (single direction: dimmonth → facts)

---

## Estratégia Recomendada para Power BI - Pilar B

### **Opção A: Modelo com dimmonth (Mais completo)**
```
Relacionamentos:
- dimmonth[yearmonthkey] (INT) → factretailirsa[yearmonthkey] (INT)
- dimmonth[yearmonthkey] (INT) → factisrseasonalgap[yearmonthkey] (INT)

Filtros de tempo:
- Usar dimmonth para slicers (ano, mês, trimestre)
- Medidas DAX usam contexto de dimmonth

Ações necessárias:
1. Converter dimmonth.yearmonthkey para INT (Power Query ou Neon)
2. Criar relacionamentos ativos
```

### **Opção B: Modelo sem dimmonth (Mais simples - RECOMENDADO PARA INÍCIO)**
```
Sem relacionamentos entre tabelas
- Usar factisrseasonalgap[monthdate] diretamente nos eixos
- Não importar dimmonth no modelo
- Medidas DAX funcionam independentemente

Vantagens:
✅ Sem incompatibilidade de tipos
✅ Modelo mais simples (2 tabelas em vez de 3)
✅ Performance melhor (menos relacionamentos)
✅ Todas as 6 KPIs funcionam sem dimmonth

Quando usar:
- Dashboard focado apenas em Pilar B (não combina com Pilar A)
- Análise de série temporal macro (não precisa de hierarquia de tempo complexa)
```

---

## Medidas DAX - Independentes de Relacionamentos

Todas as 6 KPIs funcionam **COM ou SEM dimmonth**:

### KPI #1: ISR (SA)
```dax
ISR (SA) = SUM(FactRETAILIRSA[ISR_SA])
```

### KPI #1.1: ISR MoM % (SA)
```dax
ISR MoM % (SA) =
VAR CurrentMonth_ISR = [ISR (SA)]
VAR PreviousMonth_ISR =
    CALCULATE(
        [ISR (SA)],
        DATEADD(FactRETAILIRSA[MonthDate], -1, MONTH)
    )
RETURN
    IF(
        ISBLANK(CurrentMonth_ISR) || ISBLANK(PreviousMonth_ISR),
        BLANK(),
        DIVIDE(CurrentMonth_ISR - PreviousMonth_ISR, PreviousMonth_ISR)
    )
```

### KPI #1.2: ISR YoY % (SA)
```dax
ISR YoY % (SA) =
VAR CurrentMonth_ISR = [ISR (SA)]
VAR PreviousYear_ISR =
    CALCULATE(
        [ISR (SA)],
        DATEADD(FactRETAILIRSA[MonthDate], -12, MONTH)
    )
RETURN
    IF(
        ISBLANK(CurrentMonth_ISR) || ISBLANK(PreviousYear_ISR),
        BLANK(),
        DIVIDE(CurrentMonth_ISR - PreviousYear_ISR, PreviousYear_ISR)
    )
```

### KPI #1.5: ISR Percentil 10 anos
```dax
ISR Percentil 10Y (SA) =
VAR CurrentMonth = MAX(FactISRSeasonalGap[MonthDate])
VAR CurrentISR = [ISR (SA)]
VAR StartWindow = EDATE(CurrentMonth, -119)

VAR WindowISR =
    CALCULATETABLE(
        VALUES(FactISRSeasonalGap[ISR_SA]),
        FILTER(
            ALL(FactISRSeasonalGap[MonthDate]),
            FactISRSeasonalGap[MonthDate] >= StartWindow &&
            FactISRSeasonalGap[MonthDate] <= CurrentMonth
        )
    )

VAR CountBelow =
    COUNTROWS(
        FILTER(WindowISR, FactISRSeasonalGap[ISR_SA] < CurrentISR)
    )

VAR TotalWindow = COUNTROWS(WindowISR)

RETURN
    IF(
        TotalWindow < 120 || ISBLANK(CurrentISR),
        BLANK(),
        DIVIDE(CountBelow, TotalWindow - 1)
    )
```

### KPI #1.6: ISR (NSA)
```dax
ISR (NSA) =
VAR CurrentISR_NSA = SUM(FactISRSeasonalGap[ISR_NSA])
RETURN
    IF(
        ISBLANK(CurrentISR_NSA),
        BLANK(),
        CurrentISR_NSA
    )
```

### KPI #4: ISR Seasonal Gap (Absoluto)
```dax
ISR Seasonal Gap (abs) = SUM(FactISRSeasonalGap[Gap_abs])
```

### KPI #5: ISR Seasonal Gap (%)
```dax
ISR Seasonal Gap (%) = SUM(FactISRSeasonalGap[Gap_pct])
```

---

## Recomendação Final

### 🎯 **Para Começar Rápido: Opção B (SEM dimmonth)**

**Importar no Power BI:**
- ✅ factisrseasonalgap (contém TODAS as colunas necessárias)
- ✅ factretailirsa (opcional, pode usar ISR_SA de factisrseasonalgap)
- ❌ dimmonth (NÃO importar - evita problema de tipos)

**Vantagens:**
- Sem erros de relacionamento
- Modelo mais simples
- Todas as 6 KPIs funcionam perfeitamente
- Usar `factisrseasonalgap[monthdate]` diretamente em gráficos

**Quando adicionar dimmonth:**
- Se precisar de hierarquia Ano → Trimestre → Mês
- Se for combinar Pilar A + Pilar B (calendário compartilhado)
- Nesse caso: **corrigir tipos primeiro** (VARCHAR → INTEGER)

---

**Última atualização:** 2025-11-18
**Projeto:** Dashboard E-Commerce Brasil - CEUB - Pilar B
