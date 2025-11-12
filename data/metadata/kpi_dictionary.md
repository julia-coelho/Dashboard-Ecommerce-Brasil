# Dicionário de KPIs - Retail Sales Analytics

## Resumo
Este documento descreve todas as KPIs (Key Performance Indicators) utilizadas no projeto de análise de vendas no varejo.

---

## 1. Retail Sales (M)

**Nome Técnico:** `Retail_Sales_M`

**Descrição:** Total de vendas no varejo para o mês

**Fórmula Matemática:**
```
Σ(Retail Sales)
```

**Fórmula DAX:**
```dax
SUM(FactRetailMonthly[RetailSales])
```

**Características:**
- **Unidade:** $
- **Tipo:** Valor absoluto
- **Grão:** Mês × Item (ou agregações)

**Fontes de Dados:**
- **Colunas:** FactRetailMonthly[RetailSales]
- **Tabelas:** FactRetailMonthly, dim_month_1992_2028

**Regras BLANK:** N/A

**Caso de Uso:** Medida base para análise de vendas mensais

---

## 2. Avg Retail Sales Prev 3M

**Nome Técnico:** `Avg_Retail_Sales_Prev_3M`

**Descrição:** Média de vendas dos 3 meses anteriores ao mês atual

**Fórmula Matemática:**
```
média(Retail Sales_{m-1}, Retail Sales_{m-2}, Retail Sales_{m-3})
```

**Fórmula DAX:**
```dax
VAR MaxMes = MAX(dim_month_1992_2028[MonthDate]) RETURN IF(CALCULATE(DISTINCTCOUNT(dim_month_1992_2028[YearMonthKey]), DATESINPERIOD(dim_month_1992_2028[MonthDate], EOMONTH(MaxMes,-1), -3, MONTH)) < 3, BLANK(), AVERAGEX(DATESINPERIOD(dim_month_1992_2028[MonthDate], EOMONTH(MaxMes,-1), -3, MONTH), [Retail Sales (M)]))
```

**Características:**
- **Unidade:** $
- **Tipo:** Média móvel
- **Grão:** Mês × Item (ou agregações)

**Fontes de Dados:**
- **Colunas:** FactRetailMonthly[RetailSales], dim_month_1992_2028[MonthDate, YearMonthKey]
- **Tabelas:** FactRetailMonthly, dim_month_1992_2028

**Regras BLANK:** Retorna BLANK se menos de 3 meses anteriores disponíveis

**Caso de Uso:** Base de comparação para cálculo de tendência

---

## 3. Δ Vendas vs Média 3M %

**Nome Técnico:** `Delta_Vendas_vs_Media_3M_Pct`

**Descrição:** Variação percentual das vendas do mês atual em relação à média dos 3 meses anteriores

**Fórmula Matemática:**
```
(Retail Sales_m - média_3m) / média_3m × 100
```

**Fórmula DAX:**
```dax
VAR Base3M = [Avg Retail Sales Prev 3M] RETURN IF(ISBLANK(Base3M) || Base3M = 0, BLANK(), DIVIDE([Retail Sales (M)] - Base3M, Base3M))
```

**Características:**
- **Unidade:** %
- **Tipo:** Variação percentual
- **Grão:** Mês × Item (ou agregações: Mês × ItemType, Mês × Categoria, Mês Total)

**Fontes de Dados:**
- **Colunas:** FactRetailMonthly[RetailSales], dim_month_1992_2028[MonthDate, YearMonthKey]
- **Tabelas:** FactRetailMonthly, dim_month_1992_2028, DimCategoria (opcional)

**Regras BLANK:** Retorna BLANK se: (1) menos de 3 meses anteriores, (2) média_3m = 0

**Caso de Uso:** KPI principal - Tendência 3M (%) exibida em card e tooltips de gráficos de vendas mensais

---

## Modelo de Dados - Relacionamentos

### Relacionamentos Ativos
1. **dim_month_1992_2028[YearMonthKey] (1) → FactRetailMonthly[YearMonthKey] (*)**
   - Cardinalidade: One-to-Many
   - Direção do filtro: Single (dim → fact)
   - Status: Ativo

2. **DimCategoria[ItemType] (1) → FactRetailMonthly[ItemType] (*)**
   - Cardinalidade: One-to-Many
   - Direção do filtro: Single (dim → fact)
   - Status: Ativo (opcional)

### Hierarquia de Categorias
```
Categoria (DimCategoria)
  └─ ItemType (DimCategoria/FactRetailMonthly)
      └─ ItemCode (FactRetailMonthly)
          └─ ItemDescription (FactRetailMonthly)
```

---

## Arquivos de Dados

### Tabelas Fato
- `data/processed/FactRetailMonthly.csv` - Vendas mensais agregadas por item

### Tabelas Dimensão
- `data/dims/dim_month_1992_2028.csv` - Dimensão temporal (1992-2028)
- `data/dims/DimCategoria.csv` - Mapeamento ItemType → Categoria

### Metadados e QA
- `data/metadata/kpi_dictionary.csv` - Este dicionário em formato CSV
- `data/metadata/qa_kpi_delta_vendas_3m.csv` - Casos de teste para validação

---

**Última atualização:** 2025-11-07
**Versão:** 1.0
