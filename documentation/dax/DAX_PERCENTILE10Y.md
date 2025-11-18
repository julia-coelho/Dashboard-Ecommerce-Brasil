# DAX - Percentil histórico (10 anos) - SA

**KPI:** ISR Percentile (10-year rolling window)
**Nome Técnico:** `kpi_isr_percentile10y_sa`
**Pilar:** B (Macro/Estratégico)
**Data:** 2025-11-17

---

## 1. Objetivo

Contextualizar o nível atual do ISR_SA através de sua **posição percentual** dentro de uma janela móvel de 10 anos (120 meses). Indica se o ISR atual está alto ou baixo em relação ao histórico recente.

---

## 2. Fórmula Matemática

```
Para cada mês m:
Percentil(m) = Posição percentual de ISR_SA(m)
               dentro da janela {ISR_SA(m-119), ..., ISR_SA(m)}
```

**Onde:**
- Janela móvel = 120 meses (10 anos)
- Percentil calculado usando método inclusivo (PERCENTILE.INC)
- Resultado: 0% (mínimo histórico) a 100% (máximo histórico)

**Interpretação:**
- Percentil 90%: ISR atual está acima de 90% dos valores dos últimos 10 anos (muito alto)
- Percentil 50%: ISR atual está na mediana dos últimos 10 anos (neutro)
- Percentil 10%: ISR atual está abaixo de 90% dos valores dos últimos 10 anos (muito baixo)

---

## 3. Fórmula DAX (Power BI)

```dax
Percentil 10 anos (SA) =
VAR CurrentMonth = MAX(dimmonth[MonthDate])
VAR CurrentISR = [ISR (SA)]
VAR Window10Years =
    DATESBETWEEN(
        dimmonth[MonthDate],
        EDATE(CurrentMonth, -119),  -- 120 meses atrás
        CurrentMonth                 -- Mês atual (inclusivo)
    )
VAR WindowValues =
    CALCULATETABLE(
        ADDCOLUMNS(
            Window10Years,
            "ISR_Value", [ISR (SA)]
        ),
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

**Componentes:**
- `CurrentMonth`: Mês no contexto atual
- `CurrentISR`: Valor ISR_SA do mês atual
- `Window10Years`: Janela móvel de 120 meses (m-119 até m)
- `WindowValues`: Tabela com todos os valores ISR_SA na janela
- `WindowCount`: Número de valores não-BLANK na janela
- `PERCENTILEX.INC`: Calcula percentil inclusivo (0-1, convertido para %)
- Regra: WindowCount < 120 → BLANK

---

## 4. Características

| Propriedade | Valor |
|-------------|-------|
| **Tipo** | Medida derivada (estatística móvel) |
| **Unidade** | Percentual (%) |
| **Formato** | Percentual, 1 casa decimal |
| **Grão** | Mês (série nacional) |
| **Janela** | 120 meses (10 anos) |
| **Período disponível** | Jan/2002 - Jul/2025 (283 meses) |
| **Primeiros 119 meses** | BLANK (Jan/1992 - Nov/2001) |

---

## 5. Regras de BLANK

| Condição | Resultado |
|----------|-----------|
| Mês sem ISR_SA | BLANK |
| Histórico < 120 meses | BLANK |
| Janela com ≥ 120 valores | Percentil calculado |

**Exemplo:**
- Jan/2002 (120º mês): Primeiro valor calculado
- Jan/1992 - Nov/2001: BLANK (< 120 observações)

---

## 6. Fontes de Dados

### Tabelas
- **FactRETAILIRSA**: Fonte do ISR_SA
- **dimmonth**: Calendário para janela móvel

### Relacionamentos
- **dimmonth[YearMonthKey] → FactRETAILIRSA[YearMonthKey]** (ATIVO)

### Origem Externa
- **FRED** (Federal Reserve Economic Data)
- **Série**: RETAILIRSA

---

## 7. Interpretação de Valores

| Percentil | Interpretação | Contexto |
|-----------|---------------|----------|
| 90-100% | ISR muito alto | Estoque acumulando (últimos 10 anos) |
| 75-90% | ISR alto | Acima do normal recente |
| 50-75% | ISR moderado-alto | Acima da mediana |
| 25-50% | ISR moderado-baixo | Abaixo da mediana |
| 10-25% | ISR baixo | Abaixo do normal recente |
| 0-10% | ISR muito baixo | Estoque baixo (últimos 10 anos) |

**Nota:** Percentil alto (>75%) indica que o ISR atual está elevado em relação ao histórico recente, sugerindo acúmulo de estoque relativo às vendas.

---

## 8. Estatísticas da Série (Jan/2002 - Jul/2025)

### Baseado em janela móvel de 120 meses:

| Métrica | Valor | Mês |
|---------|-------|-----|
| **Mínimo** | 0.0% | Diversos meses em ponto mínimo da janela |
| **Máximo** | 100.0% | Diversos meses em ponto máximo da janela |
| **Média** | ~50% | Tendência central |
| **Mediana** | ~50% | Por construção do percentil |

**Observação:** Por definição, o percentil varia de 0% a 100%, com distribuição dependente da volatilidade histórica do ISR.

---

## 9. Formatação no Power BI

### Card Principal
```
Formato: Percentual
Casas decimais: 1
Exemplo: 67.8%
```

### Tooltip
```
Percentil 10 anos (SA): 67.8%
ISR (SA): 1.29
Janela: Ago/2015 - Jul/2025 (120 meses)

Interpretação: ISR atual está acima de 67.8%
dos valores dos últimos 10 anos
```

---

## 10. Caso de Uso

### Exemplo de Card
```
┌─────────────────────────┐
│ Percentil 10 anos (SA)  │
│                         │
│      67.8%              │
│                         │
│ Janela móvel 120 meses  │
└─────────────────────────┘
```

### Tooltip Detalhado
- **Definição**: Posição percentual do ISR atual vs histórico de 10 anos
- **ISR (SA)**: 1.29
- **Percentil**: 67.8%
- **Janela**: Ago/2015 - Jul/2025 (120 meses)
- **Interpretação**: ISR atual está relativamente moderado-alto no contexto histórico

---

## 11. Validação QA

### Critérios de Aceite:
- ✅ Fórmula: Percentil dentro de janela móvel 120 meses
- ✅ Unidade: percentual (0-100%)
- ✅ Regra BLANK: histórico < 120 meses → BLANK
- ✅ 3 meses auditados: diferença ≤ 1 p.p. vs planilha manual
- ✅ Tooltip com descrição da janela

### Script de Validação:
`QA_PERCENTILE10Y_VALIDATION.py`

---

## 12. Cálculo Manual (Exemplo)

### Jul/2025:
**Passo 1:** Identificar janela
- Janela: Ago/2015 (m-119) até Jul/2025 (m)
- Total: 120 meses

**Passo 2:** Ordenar valores ISR_SA na janela
- Valores em ordem crescente

**Passo 3:** Encontrar posição de ISR_SA(Jul/2025) = 1.29
- Contar quantos valores ≤ 1.29
- Percentil = (Posição / Total) × 100%

**Passo 4:** Resultado
- Exemplo: Se 81 valores ≤ 1.29, então Percentil = 81/120 = 67.5%

---

## 13. Limitações e Avisos

### ⚠️ Considerações:

1. **Janela móvel de 10 anos**:
   - Sempre os últimos 120 meses
   - Não considera períodos mais longos

2. **Sensibilidade a outliers**:
   - Valores extremos na janela afetam o percentil
   - Eventos únicos (ex: COVID-2020) podem distorcer

3. **Contexto temporal**:
   - Reflete apenas os últimos 10 anos
   - Não compara com toda a história (1992+)

4. **Interpretação relativa**:
   - Percentil é sempre relativo à janela
   - Percentil 90% em período volátil ≠ Percentil 90% em período estável

5. **Uso recomendado**:
   - Contextualização histórica do ISR atual
   - Identificação de níveis extremos
   - Benchmark com histórico recente
   - **NÃO usar** como previsão ou tendência futura

---

## 14. Relação com Outros KPIs

### Complementaridade:

| KPI | Uso | Complemento com Percentil |
|-----|-----|---------------------------|
| **ISR (SA)** | Valor absoluto | Percentil contextualiza o valor |
| **ISR MoM %** | Variação curto prazo | Percentil mostra contexto histórico |
| **ISR YoY %** | Variação longo prazo | Percentil indica posição relativa |
| **DoS (dias)** | Cobertura de estoque | Percentil indica se cobertura é alta/baixa |
| **Giro anual** | Eficiência | Percentil indica se eficiência é alta/baixa |

**Exemplo integrado:**
- ISR (SA) = 1.29
- Percentil 10 anos = 67.8%
- **Interpretação**: ISR está em nível moderado-alto para o histórico recente

---

## 15. Performance e Otimização

### Considerações DAX:

1. **CALCULATETABLE com ALL**:
   - Remove filtros para calcular janela completa
   - Pode ser custoso em datasets grandes

2. **PERCENTILEX.INC**:
   - Calcula percentil sobre tabela filtrada
   - Performance depende do tamanho da janela (120 linhas)

3. **Otimização**:
   - Pré-calcular percentis em ETL para análise histórica
   - Usar medida DAX para análise interativa

---

## 16. Dependências

### Medidas DAX:
- `[ISR (SA)]` - Medida base obrigatória

### Tabelas:
- `FactRETAILIRSA` - Fonte de ISR_SA (403 meses)
- `dimmonth` - Calendário mensal (1992-2028)

### Relacionamentos:
- `dimmonth[YearMonthKey] → FactRETAILIRSA[YearMonthKey]` (ATIVO)

---

## 17. Arquivos Relacionados

| Arquivo | Descrição |
|---------|-----------|
| `FactRETAILIRSA.csv` | Dados processados (403 meses) |
| `DAX_ISR_SA.md` | Documentação da medida base |
| `QA_PERCENTILE10Y_VALIDATION.py` | Script de validação QA |
| `kpi_dictionary_pillar-B.md` | Dicionário de KPIs Pilar B |

---

**Última atualização:** 2025-11-17
**Versão:** 1.0
**Autor:** Dashboard E-Commerce Brasil - CEUB
