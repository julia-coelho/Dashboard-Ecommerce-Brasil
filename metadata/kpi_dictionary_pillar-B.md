# Dicionário de KPIs - Pilar B (Macro/Estratégico)

## Resumo
Este documento descreve as KPIs (Key Performance Indicators) macroeconômicas do **Pilar B** - indicadores estratégicos calculados a partir de séries temporais econômicas dos EUA (FRED - Federal Reserve Economic Data).

**Foco**: Análise de tendências de mercado, sazonalidade e benchmarking com indicadores nacionais.

---

## 1. ISR (SA) - Seasonally Adjusted

**Nome Técnico:** `ISR_SA`

**Descrição:** Razão entre estoques e vendas no varejo dos EUA (ajustado sazonalmente)

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

## 2. ISR (NSA) - Not Seasonally Adjusted

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

## 3. ISR Seasonal Gap (Absoluto)

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

## 4. ISR Seasonal Gap (Percentual)

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

### v1.0 (2025-11-17)
- ✅ Criado dicionário separado para Pilar B (Macro/Estratégico)
- ✅ Adicionado KPI #1-4 do Pilar B:
  - ISR (SA) - Seasonally Adjusted
  - ISR (NSA) - Not Seasonally Adjusted
  - ISR Seasonal Gap (Absoluto)
  - ISR Seasonal Gap (Percentual)
- ✅ Adicionado modelo de dados FactISRSeasonalGap (403 meses: Jan/1992 - Jul/2025)
- ✅ Processamento ETL com inner join temporal SA↔NSA (100% match)
- ✅ QA validado: 3 meses, erro 0.000000
- ✅ Documentação completa: fórmulas, interpretação, estatísticas

---

**Última atualização:** 2025-11-17
**Versão:** 1.0
**Projeto:** Dashboard E-Commerce Brasil - CEUB - Pilar B (Macro/Estratégico)
