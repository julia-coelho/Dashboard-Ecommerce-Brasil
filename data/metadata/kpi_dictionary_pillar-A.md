# Dicionário de KPIs - Pilar A (Micro/Operacional)

## Resumo
Este documento descreve as KPIs (Key Performance Indicators) operacionais do **Pilar A** - indicadores calculados a partir dos dados internos de vendas, estoque e transferências no varejo.

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

## 4. Days in Month (M)

**Nome Técnico:** `Days_in_Month_M`

**Descrição:** Número de dias no mês atual (usado para normalização de vendas)

**Fórmula Matemática:**
```
Valor único de DaysInMonth para o mês selecionado
```

**Fórmula DAX:**
```dax
Days in Month (M) = SELECTEDVALUE(dimmonth[daysinmonth])
```

**Características:**
- **Unidade:** Dias (inteiro)
- **Tipo:** Valor de dimensão
- **Grão:** Mês

**Fontes de Dados:**
- **Colunas:** dimmonth[daysinmonth]
- **Tabelas:** dimmonth

**Regras BLANK:** Retorna BLANK se múltiplos meses selecionados (contexto ambíguo)

**Caso de Uso:** Normalizar vendas mensais por número de dias (criar métricas diárias)

---

## 5. Vendas_dia_$

**Nome Técnico:** `Vendas_dia_USD`

**Descrição:** Vendas médias por dia (normalizadas pelo número de dias do mês)

**Fórmula Matemática:**
```
Retail Sales_m / Days in Month_m
```

**Fórmula DAX:**
```dax
Vendas_dia_$ =
VAR RetailSalesM = [Retail Sales (M)]
VAR DaysInMonthM = [Days in Month (M)]
RETURN
    IF(
        ISBLANK(RetailSalesM) || ISBLANK(DaysInMonthM) || DaysInMonthM = 0,
        BLANK(),
        DIVIDE(RetailSalesM, DaysInMonthM)
    )
```

**Características:**
- **Unidade:** $ (vendas por dia)
- **Tipo:** Métrica normalizada
- **Grão:** Mês × Item (ou agregações)

**Fontes de Dados:**
- **Colunas:** FactRetailMonthly[RetailSales], dimmonth[daysinmonth]
- **Tabelas:** FactRetailMonthly, dimmonth

**Regras BLANK:** Retorna BLANK se vendas BLANK, dias do mês BLANK, ou dias = 0

**Dependências:**
- [Retail Sales (M)]
- [Days in Month (M)]

**Caso de Uso:** Comparar vendas entre meses de diferentes durações (fevereiro vs julho), base para cálculo de DoS

---

## 6. Stock Value (Snapshot)

**Nome Técnico:** `Stock_Value_Snapshot`

**Descrição:** Valor total do estoque em $ (snapshot único de 18/09/2025)

**Fórmula Matemática:**
```
Σ(Total Inventory × Price)
```

**Fórmula DAX:**
```dax
Stock Value (Snapshot) = SUM(factinventorysnapshotmonthly[stockvalue])
```

**Características:**
- **Unidade:** $
- **Tipo:** Valor absoluto (snapshot)
- **Grão:** Item × Snapshot Date (18/09/2025)

**Fontes de Dados:**
- **Colunas:** factinventorysnapshotmonthly[stockvalue]
- **Tabelas:** factinventorysnapshotmonthly, dimmonth

**Regras BLANK:** N/A

**Limitações:**
- **Snapshot único:** Dados de 18/09/2025 apenas - não reflete estoque médio real ao longo do tempo
- **Proxy em valor ($):** Usa valor monetário, não unidades físicas
- **Cobertura:** 56.2% de match entre inventário e vendas (3,811 de 6,785 itens)

**Caso de Uso:** Base para cálculo de DoS, análise de valor imobilizado em estoque

---

## 7. DoS (Dias, Proxy)

**Nome Técnico:** `DoS_Days_Proxy`

**Descrição:** Days of Supply - Estimativa de quantos dias o estoque atual duraria mantendo o ritmo de vendas atual

**Fórmula Matemática:**
```
Stock Value / (Retail Sales_m / Days in Month_m)
```
Simplificado:
```
Stock Value / Vendas_dia_$
```

**Fórmula DAX:**
```dax
DoS (Dias, Proxy) =
VAR StockVal = [Stock Value (Snapshot)]
VAR SalesPerDay = [Vendas_dia_$]
RETURN
    IF(
        ISBLANK(StockVal) || ISBLANK(SalesPerDay) || SalesPerDay <= 0,
        BLANK(),
        DIVIDE(StockVal, SalesPerDay)
    )
```

**Características:**
- **Unidade:** Dias
- **Tipo:** Métrica de cobertura
- **Grão:** Mês × Item (ou agregações)

**Fontes de Dados:**
- **Colunas:** factinventorysnapshotmonthly[stockvalue], factretailmonthly[retailsales], dimmonth[daysinmonth]
- **Tabelas:** factinventorysnapshotmonthly, factretailmonthly, dimmonth

**Regras BLANK:** Retorna BLANK se:
1. Stock Value BLANK (item sem inventário)
2. Vendas_dia_$ BLANK (item sem vendas no mês)
3. Vendas_dia_$ ≤ 0 (divisão inválida)

**Dependências:**
- [Stock Value (Snapshot)]
- [Vendas_dia_$]
  - [Retail Sales (M)]
  - [Days in Month (M)]

**Limitações:**
- **Match rate:** Apenas 56.2% dos itens têm match inventário↔vendas
- **Snapshot único:** Usa estoque de 18/09/2025, não estoque médio
- **Proxy em valor ($):** Usa valor monetário, não unidades físicas
- **Premissa:** Assume ritmo de vendas constante (pode não ser válido para sazonalidade)

**Interpretação:**
- **DoS < 30 dias:** Risco de ruptura - considerar reposição urgente
- **DoS 30-60 dias:** Cobertura adequada
- **DoS > 90 dias:** Estoque parado - considerar ações de liquidação
- **BLANK:** Item sem match inventário↔vendas (esperado para 43.8% dos itens)

**Caso de Uso:** KPI principal - Monitorar risco de ruptura, identificar estoque obsoleto, base para cálculo de Giro

---

## 8. Giro (voltas/mês)

**Nome Técnico:** `Giro_Turnover_per_Month`

**Descrição:** Velocidade de renovação do estoque - quantas vezes o estoque "gira" (se renova) por mês

**Fórmula Matemática:**
```
MIN(30 / DoS, Giro_Max_Param)
```
Onde:
- 30 = número padrão de dias para comparabilidade entre meses
- Giro_Max_Param = limite superior configurável (default: 30 voltas/mês)

**Fórmula DAX:**
```dax
Giro (voltas/mês) =
VAR DoSDias = [DoS (Dias, Proxy)]
VAR GiroCalculado = DIVIDE(30, DoSDias)
VAR GiroMax = [Giro Max (mpm)]
RETURN
    IF(
        ISBLANK(DoSDias) || DoSDias <= 0,
        BLANK(),
        MIN(GiroCalculado, GiroMax)
    )
```

**Parâmetro Relacionado:**
```dax
Giro Max (mpm) = 'Giro Max per Month Param'[Giro Max per Month Param Value]
```
- **Range:** 5-60 voltas/mês
- **Default:** 30 voltas/mês
- **Incremento:** 1

**Características:**
- **Unidade:** voltas/mês (número de renovações)
- **Tipo:** Métrica de velocidade
- **Grão:** Mês × Item (ou agregações)

**Fontes de Dados:**
- **Colunas:** factinventorysnapshotmonthly[stockvalue], factretailmonthly[retailsales], dimmonth[daysinmonth]
- **Tabelas:** factinventorysnapshotmonthly, factretailmonthly, dimmonth
- **Parâmetros:** Giro Max per Month Param

**Regras BLANK:** Retorna BLANK se:
1. DoS BLANK (herda condições BLANK do DoS)
2. DoS ≤ 0 (divisão inválida)

**Censura:** Valores calculados > Giro_Max_Param são limitados ao parâmetro (prevenir outliers extremos)

**Dependências:**
- [DoS (Dias, Proxy)]
  - [Stock Value (Snapshot)]
  - [Vendas_dia_$]
    - [Retail Sales (M)]
    - [Days in Month (M)]
- [Giro Max (mpm)]

**Limitações:**
- **Herda limitações do DoS:** 56.2% match, snapshot único, proxy em valor ($)
- **Premissa de 30 dias:** Usa mês padrão de 30 dias para comparabilidade (não dias reais do mês)
- **Proxy em valor ($):** Giro calculado em $ vendidos / $ em estoque, não unidades físicas

**Interpretação:**
- **Giro < 1:** Estoque parado - leva mais de 1 mês para renovar (considerar liquidação)
- **Giro 1-2:** Rotação lenta - adequado para produtos de baixo giro
- **Giro 2-4:** Rotação moderada - padrão para maioria dos produtos
- **Giro > 4:** Rotação rápida - risco de ruptura (considerar aumentar estoque de segurança)
- **Giro = Giro_Max_Param:** Valor censurado - giro real pode ser maior
- **BLANK:** Herda BLANK do DoS (item sem match inventário↔vendas)

**Caso de Uso:** KPI principal - Identificar produtos de baixo giro para liquidação, produtos de alto giro para reforço de estoque, otimizar capital de giro

---

## Modelo de Dados - Relacionamentos

### Relacionamentos Ativos
1. **dimmonth[yearmonthkey] (1) → factretailmonthly[yearmonthkey] (*)**
   - Cardinalidade: One-to-Many
   - Direção do filtro: Single (dim → fact)
   - Status: Ativo

2. **dimcategoria[itemtype] (1) → factretailmonthly[itemtype] (*)**
   - Cardinalidade: One-to-Many
   - Direção do filtro: Single (dim → fact)
   - Status: Ativo

3. **dimmonth[yearmonthkey] (1) → factinventorysnapshotmonthly[yearmonthkey] (*)**
   - Cardinalidade: One-to-Many
   - Direção do filtro: Single (dim → fact)
   - Status: Ativo

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
- `data/processed/pillar_a/FactRetailMonthly.csv` - Vendas mensais agregadas por item (307,644 registros)
- `data/processed/pillar_a/FactInventorySnapshotMonthly.csv` - Snapshot de inventário de 18/09/2025 (6,785 registros)

### Tabelas Dimensão
- `data/dims/dim_month_1992_2028.csv` - Dimensão temporal 1992-2028 (444 registros)
- `data/dims/DimCategoria.csv` - Mapeamento ItemType → Categoria (8 categorias)

### Metadados e QA
- `data/metadata/kpi_dictionary.md` - Este dicionário (documentação completa de KPIs)
- `data/metadata/kpi_dictionary.csv` - Versão CSV do dicionário
- `data/metadata/qa_kpi_delta_vendas_3m.csv` - Casos de teste para validação de Δ Vendas 3M%
- `data/metadata/KeyMap_Inventory_Sales.csv` - Mapeamento de códigos entre inventário e vendas (3,811 matches, 56.2%)

---

**Última atualização:** 2025-11-11
**Versão:** 2.0

---

## 10. Retail Sales (M) - Transfer Rate

**Nome Técnico:** `Retail_Sales_Transfer_M`

**Descrição:** Total de vendas no varejo para o mês (usado para cálculo de Taxa de Transferência)

**Fórmula Matemática:**
```
Σ(Retail Sales)
```

**Fórmula DAX:**
```dax
Retail Sales (M) = SUM(factretailmonthly[retailsales])
```

**Características:**
- **Unidade:** $ (USD)
- **Tipo:** Valor absoluto
- **Grão:** Mês × Item Code × Item Type

**Fontes de Dados:**
- **Colunas:** factretailmonthly[retailsales]
- **Tabelas:** factretailmonthly, dimmonth

**Regras BLANK:** N/A

**Caso de Uso:** Componente para cálculo de Taxa de Transferência

---

## 11. Retail Transfers (M)

**Nome Técnico:** `Retail_Transfers_M`

**Descrição:** Total de transferências entre lojas no varejo para o mês

**Fórmula Matemática:**
```
Σ(Retail Transfers)
```

**Fórmula DAX:**
```dax
Retail Transfers (M) = SUM(factretailmonthly[retailtransfers])
```

**Características:**
- **Unidade:** $ (USD)
- **Tipo:** Valor absoluto
- **Grão:** Mês × Item Code × Item Type

**Fontes de Dados:**
- **Colunas:** factretailmonthly[retailtransfers]
- **Tabelas:** factretailmonthly, dimmonth

**Regras BLANK:** N/A

**Caso de Uso:** Componente para cálculo de Taxa de Transferência

---

## 12. Outflow (M)

**Nome Técnico:** `Outflow_M`

**Descrição:** Saída total do varejo (vendas diretas + transferências entre lojas)

**Fórmula Matemática:**
```
Outflow = Retail Sales + Retail Transfers
```

**Fórmula DAX:**
```dax
Outflow (M) = [Retail Sales (M)] + [Retail Transfers (M)]
```

**Características:**
- **Unidade:** $ (USD)
- **Tipo:** Valor calculado
- **Grão:** Mês × Item Code × Item Type

**Fontes de Dados:**
- **Medidas:** [Retail Sales (M)], [Retail Transfers (M)]

**Regras BLANK:** N/A

**Dependências:**
- [Retail Sales (M)]
- [Retail Transfers (M)]

**Caso de Uso:** Denominador para cálculo de Taxa de Transferência

---

## 13. Taxa de Transferência (%)

**Nome Técnico:** `Transfer_Rate_Pct`

**Descrição:** Percentual da saída do varejo que ocorre por transferências entre lojas (vs vendas diretas ao consumidor)

**Fórmula Matemática:**
```
Taxa = (Retail Transfers / (Retail Sales + Retail Transfers)) × 100
```

**Fórmula DAX:**
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

**Características:**
- **Unidade:** % (percentual)
- **Tipo:** Taxa/razão
- **Grão:** Mês × Item Code × Item Type

**Fontes de Dados:**
- **Colunas:** factretailmonthly[RetailSales, RetailTransfers]
- **Tabelas:** factretailmonthly, dimmonth

**Regras BLANK:**
- Retorna BLANK se `Outflow = 0`
- Retorna BLANK se `Outflow = NULL`
- Retorna BLANK se `Retail Sales = NULL` ou `Retail Transfers = NULL`

**Dependências:**
- [Retail Sales (M)]
- [Retail Transfers (M)]
- [Outflow (M)]

**Interpretação:**
- **0-20%**: Vendas diretas predominam (padrão saudável para varejo)
- **20-40%**: Rebalanceamento moderado entre lojas
- **40-100%**: Alta movimentação entre lojas - investigar causas:
  - Desbalanceamento de estoque
  - Promoções localizadas
  - Otimização de logística

**Limitações:**
- **Valores negativos**: 113 registros com Sales negativo, 1,016 com Transfers negativo (possíveis devoluções/ajustes) → podem gerar taxas fora de 0-100%
- **Muitos BLANKs**: 38% dos registros têm Outflow = 0 (sem movimento)
- **Período**: Jun/2017 a Set/2020 (3.3 anos)

**Caso de Uso:** KPI principal - exibida em badge no card de vendas e ranking por Item Type

---

## Changelog

### v3.1 (2025-11-17)
- 🔄 Dicionário separado por pilar (Pilar A - Micro/Operacional)
- 📝 KPIs do Pilar B movidas para `kpi_dictionary_pillar-B.md`

### v3.0 (2025-11-14)
- ✅ Adicionado KPI #10-13: Taxa de Transferência
  - Retail Sales (M) - Transfer Rate
  - Retail Transfers (M)
  - Outflow (M)
  - Taxa de Transferência (%)
- ✅ Adicionado modelo de dados com factretailmonthly
- ✅ Adicionado relacionamento dimmonth → factretailmonthly
- ✅ Documentadas limitações: 38% BLANKs (Outflow=0), valores negativos
- ✅ QA validado: 3 itens × 3 meses, erro 0.0 p.p.

### v2.0 (2025-11-11)
- ✅ Adicionado KPI #4: Days in Month (M)
- ✅ Adicionado KPI #5: Vendas_dia_$ (vendas diárias normalizadas)
- ✅ Adicionado KPI #6: Stock Value (Snapshot)
- ✅ Adicionado KPI #7: DoS (Dias, Proxy) - Days of Supply
- ✅ Adicionado KPI #8: Giro (voltas/mês) - Inventory Turnover
- ✅ Atualizado modelo de dados com FactInventorySnapshotMonthly
- ✅ Adicionado relacionamento dimmonth → factinventorysnapshotmonthly
- ✅ Documentadas limitações: 56.2% match inventário↔vendas, snapshot único 18/09/2025
- ✅ Documentadas dependências entre KPIs
- ✅ Adicionados guias de interpretação para DoS e Giro

### v1.0 (2025-11-07)
- Versão inicial com KPIs #1-3 (Retail Sales, Avg 3M, Δ Vendas 3M%)
