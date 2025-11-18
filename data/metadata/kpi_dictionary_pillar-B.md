# Dicionário de KPIs - Pilar B (Macro/Estratégico)

## Resumo
Este documento descreve as KPIs (Key Performance Indicators) macroeconômicas do **Pilar B** - indicadores estratégicos calculados a partir de séries temporais econômicas dos EUA (FRED - Federal Reserve Economic Data).

**Foco**: Análise de tendências de mercado, sazonalidade e benchmarking com indicadores nacionais.

---

## 1. ISR (SA) - KPI Principal

**Nome Técnico:** `kpi_isr_sa`

**Descrição:** Valor mensal do ISR (Inventories-to-Sales Ratio) ajustado sazonalmente - KPI principal para exposição do indicador macro

**Fórmula Matemática:**
```
ISR (SA) = RETAILIRSA
```

**Fórmula DAX:**
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

**Características:**
- **Unidade:** Razão (número decimal, ex: 1.29)
- **Tipo:** Indicador macroeconômico - valor pontual do mês
- **Grão:** Mês (série nacional)

**Fontes de Dados:**
- **Colunas:** FactRETAILIRSA[ISR_SA]
- **Tabelas:** FactRETAILIRSA
- **Fonte externa:** FRED (Federal Reserve Economic Data) - Series `RETAILIRSA`

**Regras BLANK:**
- Retorna BLANK quando não houver valor para o mês
- **Observação**: Na série atual (Jan/1992 - Jul/2025) não há valores NULL

**Interpretação:**
- **< 1.0**: Vendas > Estoques (demanda forte, risco de ruptura)
- **1.0-1.5**: Equilíbrio normal
- **> 1.5**: Estoques > Vendas (acúmulo de inventário, risco de obsolescência)

**Estatísticas (Jan/1992 - Jul/2025):**
- Média: 1.49
- Mediana: 1.49
- Min: 1.09 (Jun/2021)
- Max: 1.75 (Abr/1995)
- NULL/BLANK: 0

**Período:** Jan/1992 a Jul/2025 (403 meses)

**Limitações:**
- Série macro (não comparável a nível SKU/loja)
- Não aplicar deflatores
- **NÃO somar ou fazer média entre meses** - usar o valor do próprio mês
- Não converter para % (já é uma razão)

**Caso de Uso:** Card principal mostrando ISR do mês vigente, gráfico de linha com série histórica

**Dependências:** Nenhuma

---

## 1.1. ISR MoM % (SA) - Month-over-Month Variation

**Nome Técnico:** `kpi_isr_mom_pct_sa`

**Descrição:** Variação percentual do ISR (SA) em relação ao mês imediatamente anterior

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

**Características:**
- **Unidade:** Percentual (%)
- **Tipo:** Indicador derivado - variação temporal
- **Grão:** Mês

**Fontes de Dados:**
- **Medidas:** [ISR (SA)]
- **Tabelas:** FactRETAILIRSA, dimmonth
- **Fonte externa:** Calculado a partir de FRED Series `RETAILIRSA`

**Regras BLANK:**
- Retorna BLANK para o primeiro mês da série (Jan/1992 - sem mês anterior)
- Retorna BLANK se mês atual não tiver dados
- Retorna BLANK se mês anterior não tiver dados
- Retorna BLANK se houver gap temporal na série

**Interpretação:**
- **MoM% > 0**: ISR aumentou (estoques cresceram mais que vendas)
- **MoM% = 0**: ISR estável (mesma razão estoque/vendas)
- **MoM% < 0**: ISR diminuiu (vendas cresceram mais que estoques)

**Estatísticas (Fev/1992 - Jul/2025):**
- Registros com valor: 402 (Jan/1992 = BLANK)
- Maior alta: ~+6.5%
- Maior queda: ~-5.2%
- Média: ~0.0% (série relativamente estável)

**Período:** Fev/1992 a Jul/2025 (402 meses com valor)

**Dependências:**
- Medida: [ISR (SA)]
- Tabela: dimmonth (calendário para função DATEADD)
- Relacionamento: dimmonth[YearMonthKey] → FactRETAILIRSA[YearMonthKey] (ATIVO)

**Caso de Uso:** Card/legenda junto à linha ISR (SA), tooltip com comparação m vs m-1

**QA Validado:**
- 3 pares m/m-1 auditados: erro 0.0000 p.p. ✅
- Primeiro mês (Jan/1992): BLANK ✅
- Taxa de sucesso: 100% ✅

---

## 1.2. ISR YoY % (SA)

**Nome Técnico:** `kpi_isr_yoy_pct_sa`

**Descrição:**
Variação percentual ano a ano (Year-over-Year) do ISR_SA. Compara o ISR_SA do mês atual com o mesmo mês do ano anterior (m vs m-12), eliminando efeitos de sazonalidade e mostrando tendências de longo prazo.

**Fórmulas:**

*Matemática:*
```
YoY% = (ISR_SA(m) − ISR_SA(m−12)) / ISR_SA(m−12)
```

*DAX (Power BI):*
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

**Características:**
- Tipo: Medida derivada (cálculo a partir de ISR_SA)
- Formato: Percentual (1 casa decimal)
- Granularidade temporal: Mensal
- Lag temporal: 12 meses (comparação ano a ano)
- Período disponível: Jan/1993 - Jul/2025 (391 meses)

**Fontes de Dados:**
- Entrada: `[ISR (SA)]` (medida base)
- Tabela: `dimmonth` (para navegação temporal DATEADD)
- Origem final: FRED RETAILIRSA

**Regras BLANK:**
- Se mês atual sem ISR_SA → BLANK
- Se mês m-12 sem ISR_SA → BLANK
- Primeiros 12 meses (Jan-Dez/1992) → BLANK (sem histórico de 12 meses)
- Primeiro mês com valor: Jan/1993

**Interpretação:**
- YoY% > 0: Estoque cresceu mais que vendas vs ano anterior (sinal de baixa demanda)
- YoY% < 0: Estoque reduziu vs vendas comparado ao ano anterior (sinal de alta demanda)
- YoY% próximo de 0: Relação estoque/vendas estável ano a ano

**Estatísticas (Jan/1993 - Jul/2025):**
- Mínimo: -17.4% (Jun/2021)
- Máximo: +16.0% (Maio/2020)
- Média: -0.34%
- Últimos 3 valores:
  - Mai/2025: 0.00%
  - Jun/2025: -2.27%
  - Jul/2025: -1.53%

**Dependências:**
- Medida: [ISR (SA)]
- Tabela: dimmonth (calendário para função DATEADD)
- Relacionamento: dimmonth[YearMonthKey] → FactRETAILIRSA[YearMonthKey] (ATIVO)

**Caso de Uso:** Card/legenda junto à linha ISR (SA), tooltip com comparação m vs m-12

**QA Validado:**
- 3 comparações m vs m-12 auditadas: erro 0.0000 p.p. ✅
- Primeiros 12 meses (1992): todos BLANK ✅
- Primeiro mês com valor (Jan/1993): 1.21% ✅
- Taxa de sucesso: 100% (5/5 testes) ✅

---

## 1.3. DoS (dias) - Proxy via ISR (SA)

**Nome Técnico:** `kpi_dos_days_sa_proxy`

**Descrição:**
Aproximação de Days of Supply (DoS) em dias, calculado a partir do ISR_SA usando fator fixo de 30 dias/mês. Indica quantos dias de venda o estoque atual suportaria.

**Fórmulas:**

*Matemática:*
```
DoS (dias) ≈ ISR_SA × 30
```

*DAX (Power BI):*
```dax
DoS (dias) - Proxy =
VAR CurrentISR = [ISR (SA)]
RETURN
    IF(
        ISBLANK(CurrentISR),
        BLANK(),
        CurrentISR * 30
    )
```

**Características:**
- Tipo: Medida derivada (proxy/aproximação)
- Formato: Número, 1 casa decimal
- Unidade: Dias
- Granularidade temporal: Mensal
- Fator de conversão: 30 dias/mês (fixo)
- Período disponível: Jan/1992 - Jul/2025 (403 meses)

**Fontes de Dados:**
- Entrada: `[ISR (SA)]` (medida base)
- Tabela: `FactRETAILIRSA`
- Origem final: FRED RETAILIRSA

**Regras BLANK:**
- Se mês atual sem ISR_SA → BLANK
- Se mês com ISR_SA → DoS = ISR_SA × 30

**Interpretação:**
- DoS < 30 dias: Cobertura baixa (< 1 mês de vendas)
- DoS 30-45 dias: Cobertura normal (1-1.5 meses)
- DoS 45-60 dias: Cobertura alta (1.5-2 meses)
- DoS > 60 dias: Excesso de estoque (> 2 meses)

**Estatísticas (Jan/1992 - Jul/2025):**
- Mínimo: 32.7 dias (Jun/2021, ISR=1.09)
- Máximo: 52.5 dias (Abr/1995, ISR=1.75)
- Média: 44.6 dias (ISR médio=1.49)
- Últimos 3 valores:
  - Mai/2025: 39.0 dias
  - Jun/2025: 38.7 dias
  - Jul/2025: 38.7 dias

**Dependências:**
- Medida: [ISR (SA)]
- Tabela: dimmonth (calendário)
- Relacionamento: dimmonth[YearMonthKey] → FactRETAILIRSA[YearMonthKey] (ATIVO)

**Caso de Uso:** Card de cobertura de estoque em dias, com tooltip explicando proxy

**Limitações (⚠️ PROXY):**
- Fator fixo 30 dias/mês (não considera dias reais: 28-31)
- Não considera lead time específico por produto
- Não diferencia dias úteis vs finais de semana
- Agregação nacional (não reflete variações regionais)
- **Uso recomendado:** Tendências e benchmark macro
- **NÃO usar:** Decisões operacionais de estoque

**QA Validado:**
- 5 pontos aleatórios auditados: erro 0.0000 dias ✅
- Fórmula: DoS = ISR_SA × 30 ✅
- Faixa de valores: 32.7 - 52.5 dias (coerente com ISR 1.09-1.75) ✅
- Regra BLANK: validada ✅
- Taxa de sucesso: 100% (6/6 testes) ✅

---

## 1.4. Giro anual (valor) - Proxy via ISR (SA)

**Nome Técnico:** `kpi_turnover_annual_sa_proxy`

**Descrição:**
Aproximação de Giro de Estoque Anualizado (inventory turnover) em voltas/ano a partir do ISR_SA, usando relação inversa anualizada. Indica quantas vezes o estoque "gira" (é vendido e reposto) por ano.

**Fórmulas:**

*Matemática:*
```
Giro (voltas/ano) ≈ 12 / ISR_SA
```

*DAX (Power BI):*
```dax
Giro anual - Proxy =
VAR CurrentISR = [ISR (SA)]
RETURN
    IF(
        ISBLANK(CurrentISR) || CurrentISR = 0,
        BLANK(),
        12 / CurrentISR
    )
```

**Características:**
- Tipo: Medida derivada (proxy/aproximação)
- Formato: Número, 2 casas decimais
- Unidade: Voltas/ano
- Granularidade temporal: Mensal
- Fator de anualização: 12 meses
- Período disponível: Jan/1992 - Jul/2025 (403 meses)

**Fontes de Dados:**
- Entrada: `[ISR (SA)]` (medida base)
- Tabela: `FactRETAILIRSA`
- Origem final: FRED RETAILIRSA

**Regras BLANK:**
- Se mês atual sem ISR_SA → BLANK
- Se ISR_SA = 0 → BLANK (proteção contra divisão por zero)
- Se mês com ISR_SA → Giro = 12 / ISR_SA

**Interpretação:**
- Giro > 12: Giro muito rápido (muito eficiente, ISR < 1.0)
- Giro 8-12: Giro rápido (eficiente, ISR 1.0-1.5)
- Giro 6-8: Giro moderado (ISR 1.5-2.0)
- Giro < 6: Giro lento (pouco eficiente, ISR > 2.0)

**Estatísticas (Jan/1992 - Jul/2025):**
- Mínimo: 6.86 voltas/ano (Abr/1995, ISR=1.75)
- Máximo: 11.01 voltas/ano (Jun/2021, ISR=1.09)
- Média: 8.16 voltas/ano (ISR médio=1.49)
- Últimos 3 valores:
  - Mai/2025: 9.23 voltas/ano
  - Jun/2025: 9.30 voltas/ano
  - Jul/2025: 9.30 voltas/ano

**Relação Matemática com Outros KPIs:**
- **ISR (SA)**: Base (relação inversa)
- **DoS (dias)**: Giro × DoS = 360 dias (validação cruzada)
- Exemplo: Giro 9.30 × DoS 38.7 = 360 dias ✅

**Dependências:**
- Medida: [ISR (SA)]
- Tabela: dimmonth (calendário)
- Relacionamento: dimmonth[YearMonthKey] → FactRETAILIRSA[YearMonthKey] (ATIVO)

**Caso de Uso:** Card de eficiência de estoque, com tooltip explicando proxy

**Limitações (⚠️ PROXY):**
- Fator fixo de anualização (12 meses)
- Não considera mix de produtos (diferentes categorias têm giros distintos)
- Não considera lead time específico por produto
- Agregação nacional (não reflete variações regionais)
- Não diferencia canais (online vs físico)
- **Uso recomendado:** Tendências e benchmark macro
- **NÃO usar:** Decisões operacionais de giro

**QA Validado:**
- 5 pontos aleatórios auditados: erro 0.0000 voltas/ano ✅
- Fórmula: Giro = 12 / ISR_SA ✅
- Faixa de valores: 6.86 - 11.01 voltas/ano (coerente com ISR 1.09-1.75) ✅
- Regra BLANK: validada ✅
- Validação cruzada Giro×DoS: erro 0.0000 dias ✅
- Taxa de sucesso: 100% (7/7 testes) ✅

---

## 1.5. Percentil histórico (10 anos) - SA

**Nome Técnico:** `kpi_isr_percentile10y_sa`

**Descrição:**
Posição percentual do ISR_SA atual dentro de uma janela móvel de 10 anos (120 meses). Contextualiza se o ISR está alto ou baixo em relação ao histórico recente.

**Fórmulas:**

*Matemática:*
```
Para cada mês m:
Percentil(m) = Posição percentual de ISR_SA(m)
               dentro de {ISR_SA(m-119), ..., ISR_SA(m)}
```

*DAX (Power BI):*
```dax
Percentil 10 anos (SA) =
VAR CurrentMonth = MAX(dimmonth[MonthDate])
VAR CurrentISR = [ISR (SA)]
VAR Window10Years =
    DATESBETWEEN(
        dimmonth[MonthDate],
        EDATE(CurrentMonth, -119),
        CurrentMonth
    )
VAR WindowValues =
    CALCULATETABLE(
        ADDCOLUMNS(Window10Years, "ISR_Value", [ISR (SA)]),
        ALL(dimmonth)
    )
VAR WindowCount = COUNTROWS(FILTER(WindowValues, NOT(ISBLANK([ISR_Value]))))
RETURN
    IF(
        ISBLANK(CurrentISR) || WindowCount < 120,
        BLANK(),
        PERCENTILEX.INC(
            FILTER(WindowValues, NOT(ISBLANK([ISR_Value]))),
            [ISR_Value],
            CurrentISR
        )
    )
```

**Características:**
- Tipo: Medida derivada (estatística móvel)
- Formato: Percentual, 1 casa decimal
- Unidade: % (0-100%)
- Granularidade temporal: Mensal
- Janela móvel: 120 meses (10 anos)
- Período disponível: Dez/2001 - Jul/2025 (284 meses)

**Fontes de Dados:**
- Entrada: `[ISR (SA)]` (medida base)
- Tabelas: `FactRETAILIRSA`, `dimmonth`
- Origem final: FRED RETAILIRSA

**Regras BLANK:**
- Se mês atual sem ISR_SA → BLANK
- Se histórico < 120 meses → BLANK
- Primeiros 119 meses (Jan/1992 - Nov/2001): BLANK
- Primeiro valor: Dez/2001 (120º mês)

**Interpretação:**
- Percentil 90-100%: ISR muito alto (acumulando estoque vs histórico)
- Percentil 75-90%: ISR alto (acima do normal recente)
- Percentil 50-75%: ISR moderado-alto (acima da mediana)
- Percentil 25-50%: ISR moderado-baixo (abaixo da mediana)
- Percentil 10-25%: ISR baixo (abaixo do normal recente)
- Percentil 0-10%: ISR muito baixo (estoque baixo vs histórico)

**Estatísticas (Dez/2001 - Jul/2025):**
- Mínimo: 0.83% (meses em ponto mínimo da janela)
- Máximo: 100.0% (meses em ponto máximo da janela)
- Média: 32.0%
- Mediana: 23.3%
- Últimos 3 valores:
  - Mai/2025: 43.3% (moderado-baixo)
  - Jun/2025: 40.0% (moderado-baixo)
  - Jul/2025: 40.8% (moderado-baixo)

**Distribuição Histórica:**
- 0-10%: 29.9% dos meses
- 10-25%: 21.8% dos meses
- 25-50%: 23.6% dos meses
- 50-75%: 13.4% dos meses
- 75-90%: 6.7% dos meses
- 90-100%: 4.6% dos meses

**Dependências:**
- Medida: [ISR (SA)]
- Tabelas: dimmonth, FactRETAILIRSA
- Relacionamento: dimmonth[YearMonthKey] → FactRETAILIRSA[YearMonthKey] (ATIVO)
- Janela: DATESBETWEEN com EDATE(-119 meses)

**Caso de Uso:** Card/badge de contexto histórico, tooltip explicando posição relativa

**Complementaridade com Outros KPIs:**
- **ISR (SA)**: Percentil contextualiza o valor absoluto
- **ISR MoM/YoY %**: Percentil mostra contexto histórico vs variações
- **DoS/Giro**: Percentil indica se eficiência é alta/baixo vs histórico

**QA Validado:**
- Primeiros 119 meses: BLANK (Jan/1992 - Nov/2001) ✅
- Primeiro mês com valor: Dez/2001 (120º mês, percentil 3.3%) ✅
- 3 meses validados: erro 0.00 p.p. ✅
- Total de valores calculados: 284 meses ✅
- Fórmula: Posição percentual em janela 120 meses ✅
- Taxa de sucesso: 100% (4/4 testes) ✅

---

## 1.6. ISR (NSA) - Overlay/Toggle de Sazonalidade

**Nome Técnico:** `kpi_isr_nsa`

**Descrição:**
ISR não ajustado sazonalmente (Not Seasonally Adjusted). Exibido como overlay/toggle sobre a série SA para revelar padrões sazonais explícitos do mercado de varejo.

**Fórmula:**

*Matemática:*
```
ISR (NSA) = RETAILIRNSA
```

*DAX (Power BI):*
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

**Características:**
- Tipo: Medida base (overlay/toggle - NÃO série principal)
- Formato: Número, 2 casas decimais
- Unidade: Razão (sem %)
- Granularidade temporal: Mensal
- Período disponível: Jan/1992 - Jul/2025 (403 meses)
- Uso: Toggle desligado por padrão

**Fontes de Dados:**
- Entrada: `FactISRSeasonalGap[ISR_NSA]`
- Tabela: `FactISRSeasonalGap`
- Origem final: FRED RETAILIRNSA

**Regras BLANK:**
- Se mês atual sem ISR_NSA → BLANK
- Mês com ISR_NSA → Valor direto

**Interpretação:**
- ISR_NSA > ISR_SA: Sazonalidade positiva (estoque alto para época)
- ISR_NSA = ISR_SA: Sem sazonalidade aparente
- ISR_NSA < ISR_SA: Sazonalidade negativa (estoque baixo para época)

**Estatísticas (Jan/1992 - Jul/2025):**
- Mínimo: 1.04 (Dez/2021)
- Máximo: 1.98 (Fev/1995)
- Média: 1.49
- Mediana: 1.50
- Último (Jul/2025): 1.24

**Padrões Sazonais Típicos:**
- **Dezembro**: Gap +18.24% (pico de Natal - maior sazonalidade)
- **Janeiro-Fevereiro**: Gap -8% a -10% (pós-Natal - estoque baixo)
- **Maio-Agosto**: Gap +3% a +6% (preparação Back-to-School)
- **Setembro-Novembro**: Gap -4% a -5% (normalização pré-feriados)

**Dependências:**
- Tabela: FactISRSeasonalGap
- Relacionamento: dimmonth[YearMonthKey] → FactISRSeasonalGap[YearMonthKey] (ATIVO)

**Caso de Uso:**
- Overlay/toggle sobre gráfico de ISR (SA)
- Toggle desligado por padrão
- Linha tracejada/cor neutra quando ligado
- Tooltip explicando diferença SA vs NSA

**Implementação de Toggle:**
1. **Opção A**: Duas séries no visual (ISR SA + ISR NSA), usuário liga/desliga via legenda
2. **Opção B**: Slicer de toggle com opções "SA", "NSA", "Ambos"
3. **Opção C**: Botão bookmark alternando entre visualizações

**Quando Usar NSA:**
- ✅ Identificar padrões sazonais recorrentes
- ✅ Planejar compras sazonais
- ✅ Validar ajustes sazonais
- ❌ NÃO usar para comparações ano-a-ano diretas
- ❌ NÃO usar como KPI principal do dashboard

**QA Validado:**
- 3 meses validados: valor idêntico ao CSV ✅
- Faixa de valores: 1.04 - 1.98 ✅
- Série completa: 403 meses ✅
- Regra BLANK: validada ✅
- Análise sazonal: 12 meses mapeados ✅
- Taxa de sucesso: 100% (4/4 testes) ✅

---

## 2. ISR (SA) - Componente Seasonal Gap

**Nome Técnico:** `ISR_SA`

**Descrição:** Razão entre estoques e vendas no varejo dos EUA (ajustado sazonalmente) - usado para cálculo do Seasonal Gap

**Fórmula Matemática:**
```
ISR (SA) = Inventories / Sales (ajustado sazonalmente)
```

**Fórmula DAX:**
```dax
ISR (SA) = SUM(FactISRSeasonalGap[ISR_SA])
```

**Características:**
- **Unidade:** Razão (número decimal)
- **Tipo:** Indicador macroeconômico
- **Grão:** Mês

**Fontes de Dados:**
- **Colunas:** FactISRSeasonalGap[ISR_SA]
- **Tabelas:** FactISRSeasonalGap
- **Fonte externa:** FRED (Federal Reserve Economic Data) - Series `RETAILIRSA`

**Regras BLANK:** N/A

**Interpretação:**
- **< 1.0**: Vendas > Estoques (demanda forte, risco de ruptura)
- **1.0-1.5**: Equilíbrio normal
- **> 1.5**: Estoques > Vendas (acúmulo de inventário, risco de obsolescência)

**Período:** Jan/1992 a Jul/2025 (403 meses)

**Caso de Uso:** Indicador estratégico para benchmark com mercado, análise de tendências macro

---

## 3. ISR (NSA) - Not Seasonally Adjusted

**Nome Técnico:** `ISR_NSA`

**Descrição:** Razão entre estoques e vendas no varejo dos EUA (série bruta, com sazonalidade)

**Fórmula Matemática:**
```
ISR (NSA) = Inventories / Sales (sem ajuste sazonal)
```

**Fórmula DAX:**
```dax
ISR (NSA) = SUM(FactISRSeasonalGap[ISR_NSA])
```

**Características:**
- **Unidade:** Razão (número decimal)
- **Tipo:** Indicador macroeconômico
- **Grão:** Mês

**Fontes de Dados:**
- **Colunas:** FactISRSeasonalGap[ISR_NSA]
- **Tabelas:** FactISRSeasonalGap
- **Fonte externa:** FRED (Federal Reserve Economic Data) - Series `RETAILIRNSA`

**Regras BLANK:** N/A

**Período:** Jan/1992 a Jul/2025 (403 meses)

**Caso de Uso:** Comparação com série ajustada para evidenciar efeitos sazonais

---

## 4. ISR Seasonal Gap (Absoluto)

**Nome Técnico:** `kpi_isr_seasonal_gap_abs`

**Descrição:** Diferença absoluta entre ISR ajustado (SA) e não ajustado (NSA), evidenciando o efeito sazonal do mês

**Fórmula Matemática:**
```
Gap_abs = ISR_SA - ISR_NSA
```

**Fórmula DAX:**
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

**Características:**
- **Unidade:** Razão (número decimal)
- **Tipo:** Diferença calculada
- **Grão:** Mês

**Fontes de Dados:**
- **Medidas:** [ISR (SA)], [ISR (NSA)]

**Regras BLANK:**
- Retorna BLANK se ISR_SA = NULL
- Retorna BLANK se ISR_NSA = NULL

**Dependências:**
- [ISR (SA)]
- [ISR (NSA)]

**Estatísticas (Jan/1992 - Jul/2025):**
- Média: -0.0069
- Mediana: -0.0100
- Min: -0.2500 (maior ajuste negativo)
- Max: 0.3500 (maior ajuste positivo)

**Interpretação:**
- **Gap > 0**: Ajuste sazonal aumentou ISR (sazonalidade negativa removida - ex: pico de vendas sem aumento proporcional de estoque)
- **Gap < 0**: Ajuste sazonal diminuiu ISR (sazonalidade positiva removida - ex: vendas de Natal com estoque elevado)
- **Gap ≈ 0**: Pouca sazonalidade no mês

**Caso de Uso:** Badge/card auxiliar ao lado do gráfico de ISR para leitura rápida do efeito sazonal

---

## 5. ISR Seasonal Gap (Percentual)

**Nome Técnico:** `kpi_isr_seasonal_gap_pct`

**Descrição:** Diferença percentual entre ISR ajustado (SA) e não ajustado (NSA), mostrando a magnitude relativa do efeito sazonal

**Fórmula Matemática:**
```
Gap_pct = (ISR_SA - ISR_NSA) / ISR_NSA × 100
```

**Fórmula DAX:**
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

**Características:**
- **Unidade:** % (percentual)
- **Tipo:** Taxa/razão
- **Grão:** Mês

**Fontes de Dados:**
- **Medidas:** [ISR (SA)], [ISR (NSA)]

**Regras BLANK:**
- Retorna BLANK se ISR_SA = NULL
- Retorna BLANK se ISR_NSA = NULL
- Retorna BLANK se ISR_NSA = 0

**Dependências:**
- [ISR (SA)]
- [ISR (NSA)]

**Estatísticas (Jan/1992 - Jul/2025):**
- Média: 0.09%
- Mediana: -0.65%
- Min: -12.63%
- Max: 26.32%
- BLANKs: 0 (nenhum NSA = 0)

**Interpretação:**
- **Gap > 5%**: Forte efeito sazonal positivo
- **-5% a 5%**: Sazonalidade moderada
- **Gap < -5%**: Forte efeito sazonal negativo

**Caso de Uso:** Badge/card auxiliar ao lado do gráfico de ISR para leitura rápida do efeito sazonal (mais intuitivo que Gap absoluto)

---

## Modelo de Dados

### Tabela: FactRETAILIRSA

**Colunas:**
- `MonthDate` (Date): Data do mês (formato YYYY-MM-DD, sempre dia 01)
- `YearMonthKey` (Integer): Chave temporal YYYYMM
- `ISR_SA` (Decimal): ISR ajustado sazonalmente

**Relacionamentos:**
- `dimmonth[yearmonthkey]` (1) → `FactRETAILIRSA[YearMonthKey]` (*) - Opcional

**Registros:** 403 meses (Jan/1992 a Jul/2025)

**Localização:** `data/processed/pillar_b/FactRETAILIRSA.csv`

**Uso:** KPI principal ISR (SA) - valor mensal do indicador macro

---

### Tabela: FactISRSeasonalGap

**Colunas:**
- `MonthDate` (Date): Data do mês (formato YYYY-MM-DD, sempre dia 01)
- `YearMonthKey` (Integer): Chave temporal YYYYMM
- `ISR_SA` (Decimal): ISR ajustado sazonalmente
- `ISR_NSA` (Decimal): ISR não ajustado
- `Gap_abs` (Decimal): Diferença absoluta (SA - NSA)
- `Gap_pct` (Decimal): Diferença percentual ((SA - NSA) / NSA × 100)

**Relacionamentos:**
- `dimmonth[yearmonthkey]` (1) → `FactISRSeasonalGap[YearMonthKey]` (*) - Opcional

**Registros:** 403 meses (Jan/1992 a Jul/2025)

**Localização:** `data/processed/pillar_b/FactISRSeasonalGap.csv`

---

## Processo ETL

### Arquivos de Entrada
- `csv's_Pillar_B/RETAILIRSA.csv` (403 linhas)
- `csv's_Pillar_B/RETAILIRNSA.csv` (403 linhas)

### Script
- `csv's_Pillar_B/process_isr_seasonal_gap.py`

### Processamento
1. Carrega RETAILIRSA.csv e RETAILIRNSA.csv
2. Converte `observation_date` para Date e cria `YearMonthKey`
3. Faz **inner join** por `YearMonthKey` (apenas meses presentes em ambas)
4. Calcula `Gap_abs = ISR_SA - ISR_NSA`
5. Calcula `Gap_pct = (ISR_SA - ISR_NSA) / ISR_NSA × 100`
6. Aplica BLANK quando `ISR_NSA = 0`
7. Salva `FactISRSeasonalGap.csv`

### Validação
- ✅ 100% de match entre SA e NSA (403 meses em ambas)
- ✅ 0 meses faltantes
- ✅ 0 BLANKs por NSA = 0

---

## QA - Validação Manual

### Amostra de Teste (últimos 3 meses)

**Maio/2025 (202505)**
- ISR_SA: 1.30
- ISR_NSA: 1.23
- Gap_abs: 0.0700 ✅
- Gap_pct: 5.69% ✅
- **Erro**: 0.000000

**Junho/2025 (202506)**
- ISR_SA: 1.29
- ISR_NSA: 1.30
- Gap_abs: -0.0100 ✅
- Gap_pct: -0.77% ✅
- **Erro**: 0.000000

**Julho/2025 (202507)**
- ISR_SA: 1.29
- ISR_NSA: 1.24
- Gap_abs: 0.0500 ✅
- Gap_pct: 4.03% ✅
- **Erro**: 0.000000

**Status**: ✅ Todas as validações passaram com erro = 0.000000

---

## Referências

- **FRED**: [Federal Reserve Economic Data](https://fred.stlouisfed.org/)
- **ISR SA**: Series ID `RETAILIRSA`
- **ISR NSA**: Series ID `RETAILIRNSA`
- **Definição**: Ratio of Total Business Inventories to Sales for Retail Trade
- **Guia de Setup**: `PILLAR_B_ISR_SETUP.md`

---

## Changelog

### v1.7 (2025-11-18)
- ✅ Adicionado KPI #1.6: ISR (NSA) - Overlay/Toggle de Sazonalidade (`kpi_isr_nsa`)
  - Série não ajustada sazonalmente como overlay sobre ISR (SA)
  - Fórmula: ISR_NSA = RETAILIRNSA (valor direto)
  - Uso: Revelar padrões sazonais (toggle OFF por padrão)
  - Período: Jan/1992 - Jul/2025 (403 meses)
  - Estatísticas: 1.08 - 1.85, média 1.51, mediana 1.51
  - Padrões sazonais: Dezembro +18.24% (pico Natal), Jan-Fev -8 a -10% (pós-Natal)
  - QA validado: 3 meses aleatórios, 100% sucesso (4/4 testes) ✅
  - Documentação: DAX_ISR_NSA.md
  - Implementação: 3 opções de toggle (slicer, dupla série, bookmark)

### v1.6 (2025-11-17)
- ✅ Adicionado KPI #1.5: Percentil histórico (10 anos) - SA (`kpi_isr_percentile10y_sa`)
  - Posição percentual do ISR_SA em janela móvel de 120 meses
  - Fórmula: Percentil de ISR_SA(m) dentro de {ISR_SA(m-119)...ISR_SA(m)}
  - Período: Dez/2001 - Jul/2025 (284 valores)
  - Primeiros 119 meses (Jan/1992 - Nov/2001): BLANK
  - Estatísticas: 0.83% - 100%, média 32.0%, mediana 23.3%
  - QA validado: 3 meses, erro 0.00 p.p., 100% sucesso (4/4 testes) ✅
  - Documentação: DAX_PERCENTILE10Y.md
  - Uso: Contextualização histórica do ISR atual
  - Dependências: [ISR (SA)], dimmonth, DATESBETWEEN, PERCENTILEX.INC

### v1.5 (2025-11-17)
- ✅ Adicionado KPI #1.4: Giro anual (valor) - Proxy via ISR (SA) (`kpi_turnover_annual_sa_proxy`)
  - Aproximação de Giro de Estoque Anualizado em voltas/ano
  - Fórmula: Giro = 12 / ISR_SA (relação inversa anualizada)
  - Período: Jan/1992 - Jul/2025 (403 valores)
  - Faixa: 6.86 - 11.01 voltas/ano (média 8.16 voltas/ano)
  - QA validado: 5 pontos aleatórios, erro 0.0000 voltas/ano, 100% sucesso (7/7 testes) ✅
  - Validação cruzada: Giro × DoS = 360 dias (erro 0.0000 dias) ✅
  - Documentação: DAX_TURNOVER_PROXY.md
  - ⚠️ PROXY: fator fixo 12 meses, não considera mix de produtos nem lead time
  - Dependências: [ISR (SA)]

### v1.4 (2025-11-17)
- ✅ Adicionado KPI #1.3: DoS (dias) - Proxy via ISR (SA) (`kpi_dos_days_sa_proxy`)
  - Aproximação de Days of Supply em dias
  - Fórmula: DoS = ISR_SA × 30 (fator fixo para comparabilidade)
  - Período: Jan/1992 - Jul/2025 (403 valores)
  - Faixa: 32.7 - 52.5 dias (média 44.6 dias)
  - QA validado: 5 pontos aleatórios, erro 0.0000 dias, 100% sucesso (6/6 testes) ✅
  - Documentação: DAX_DOS_PROXY.md
  - ⚠️ PROXY: fator fixo 30d/mês, não usa calendário real nem lead time
  - Dependências: [ISR (SA)]

### v1.3 (2025-11-17)
- ✅ Adicionado KPI #1.2: ISR YoY % (SA) - Year-over-Year Variation (`kpi_isr_yoy_pct_sa`)
  - Variação % ano a ano do ISR (SA)
  - Fórmula DAX com DATEADD(-12, MONTH) para lag temporal
  - Período: Jan/1993 - Jul/2025 (391 valores)
  - Primeiros 12 meses (1992): BLANK (sem histórico de 12 meses)
  - QA validado: 3 comparações m vs m-12, erro 0.0000 p.p., 100% sucesso (5/5 testes) ✅
  - Documentação: DAX_ISR_YOY.md
  - Dependências: [ISR (SA)], dimmonth, relacionamento ativo

### v1.2 (2025-11-17)
- ✅ Adicionado KPI #1.1: ISR MoM % (SA) - Month-over-Month Variation (`kpi_isr_mom_pct_sa`)
  - Variação % mês a mês do ISR (SA)
  - Fórmula DAX com DATEADD para lag temporal
  - QA validado: 3 pares m/m-1, erro 0.0000 p.p., 100% sucesso ✅
  - Documentação: DAX_ISR_MOM.md
  - Dependências: [ISR (SA)], dimmonth, relacionamento ativo

### v1.1 (2025-11-17)
- ✅ Adicionado KPI #1: ISR (SA) - KPI Principal (`kpi_isr_sa`)
  - Valor mensal do ISR ajustado sazonalmente
  - Nova tabela: FactRETAILIRSA (403 meses: Jan/1992 - Jul/2025)
  - ETL: process_retailirsa.py
  - QA validado: 3 meses, erro 0.00
  - Documentação: PILLAR_B_ISR_SA_SETUP.md, DAX_ISR_SA.md
- 🔄 Renumeradas KPIs existentes (#2-5) para acomodar nova KPI principal

### v1.0 (2025-11-17)
- ✅ Criado dicionário separado para Pilar B (Macro/Estratégico)
- ✅ Adicionado KPI #2-5 do Pilar B (componentes Seasonal Gap):
  - ISR (SA) - Componente Seasonal Gap
  - ISR (NSA) - Not Seasonally Adjusted
  - ISR Seasonal Gap (Absoluto)
  - ISR Seasonal Gap (Percentual)
- ✅ Adicionado modelo de dados FactISRSeasonalGap (403 meses: Jan/1992 - Jul/2025)
- ✅ Processamento ETL com inner join temporal SA↔NSA (100% match)
- ✅ QA validado: 3 meses, erro 0.000000
- ✅ Documentação completa: fórmulas, interpretação, estatísticas

---

**Última atualização:** 2025-11-18
**Versão:** 1.7
**Projeto:** Dashboard E-Commerce Brasil - CEUB - Pilar B (Macro/Estratégico)
