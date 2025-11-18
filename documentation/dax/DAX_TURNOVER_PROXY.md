# DAX - Giro anual (valor) - Proxy via ISR (SA)

**KPI:** Turnover/Giro Anual (Proxy)
**Nome Técnico:** `kpi_turnover_annual_sa_proxy`
**Pilar:** B (Macro/Estratégico)
**Data:** 2025-11-17

---

## 1. Objetivo

Aproximar **Giro de Estoque Anualizado** (inventory turnover) em voltas/ano a partir do ISR (SA), usando relação inversa anualizada.

---

## 2. Fórmula Matemática

```
Giro (voltas/ano) ≈ 12 / ISR_SA
```

**Onde:**
- `ISR_SA` = Inventories-to-Sales Ratio (Seasonally Adjusted)
- `12` = Fator de anualização (12 meses)

**Interpretação:**
- Giro indica quantas vezes o estoque "gira" (é vendido e reposto) por ano
- É o **inverso** do ISR anualizado
- Maior giro = estoque gira mais rápido (mais eficiente)
- Menor giro = estoque gira mais lento (menos eficiente)

**Exemplo:**
- ISR_SA = 1.5 → Giro ≈ 12/1.5 = 8.0 voltas/ano
- ISR_SA = 1.2 → Giro ≈ 12/1.2 = 10.0 voltas/ano

---

## 3. Fórmula DAX (Power BI)

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

**Componentes:**
- `[ISR (SA)]`: Medida base do ISR ajustado sazonalmente
- `12`: Fator de anualização
- `IF/ISBLANK`: Regra de BLANK para meses sem ISR_SA
- `CurrentISR = 0`: Proteção contra divisão por zero (improvável)

---

## 4. Características

| Propriedade | Valor |
|-------------|-------|
| **Tipo** | Medida derivada (proxy) |
| **Unidade** | Voltas/ano (número decimal) |
| **Formato** | Número, 2 casas decimais |
| **Grão** | Mês (série nacional) |
| **Período** | Jan/1992 - Jul/2025 (403 meses) |
| **Dependências** | [ISR (SA)] |

---

## 5. Regras de BLANK

| Condição | Resultado |
|----------|-----------|
| Mês sem ISR_SA | BLANK |
| ISR_SA = 0 | BLANK (proteção) |
| Mês com ISR_SA | Giro = 12 / ISR_SA |

**Exemplo:**
- ISR_SA = 1.29 → Giro ≈ 9.30 voltas/ano
- ISR_SA = BLANK → Giro = BLANK

---

## 6. Fontes de Dados

### Tabelas
- **FactRETAILIRSA**: Fonte do ISR_SA

### Relacionamentos
- **dimmonth[YearMonthKey] → FactRETAILIRSA[YearMonthKey]** (ATIVO)

### Origem Externa
- **FRED** (Federal Reserve Economic Data)
- **Série**: RETAILIRSA
- **Descrição**: Retail Inventories to Sales Ratio (SA)

---

## 7. Interpretação de Valores

| Giro (voltas/ano) | Interpretação | ISR_SA Equiv. | Eficiência |
|-------------------|---------------|---------------|------------|
| > 12 | Giro muito rápido | < 1.0 | Muito eficiente |
| 8 - 12 | Giro rápido | 1.0 - 1.5 | Eficiente |
| 6 - 8 | Giro moderado | 1.5 - 2.0 | Moderado |
| < 6 | Giro lento | > 2.0 | Pouco eficiente |

**Contexto Setorial:**
- **Varejo de alimentos**: 12-20 voltas/ano (giro rápido)
- **Varejo de moda**: 4-6 voltas/ano (giro moderado)
- **Varejo de móveis**: 2-4 voltas/ano (giro lento)
- **Varejo geral (média nacional)**: ~8-10 voltas/ano

---

## 8. Estatísticas da Série (Jan/1992 - Jul/2025)

### Baseado em 12 / ISR_SA:

| Métrica | Valor | Mês |
|---------|-------|-----|
| **Mínimo** | 6.86 voltas/ano | Abr/1995 (ISR=1.75) |
| **Máximo** | 11.01 voltas/ano | Jun/2021 (ISR=1.09) |
| **Média** | 8.10 voltas/ano | ISR médio=1.49 |
| **Mediana** | 8.05 voltas/ano | ISR mediano=1.49 |
| **Último (Jul/2025)** | 9.30 voltas/ano | ISR=1.29 |

**Observação:** Valores atuais (2021-2025) indicam giro mais rápido (~9-11 voltas/ano) comparado aos anos 90 (~7-8 voltas/ano), sugerindo maior eficiência de estoque.

---

## 9. Formatação no Power BI

### Card Principal
```
Formato: Número
Casas decimais: 2
Sufixo: " voltas/ano"
Exemplo: 9.30 voltas/ano
```

### Tooltip
```
Giro anual - Proxy: 9.30 voltas/ano
ISR (SA): 1.29
Período: Jul/2025

⚠️ Proxy com fator fixo 12 meses
Não reflete mix de produtos nem lead time
```

---

## 10. Caso de Uso

### Exemplo de Card
```
┌─────────────────────────┐
│ Giro anual - Proxy      │
│                         │
│   9.30 voltas/ano       │
│                         │
│ ⚠️ Aproximação anualizada│
└─────────────────────────┘
```

### Tooltip Detalhado
- **Definição**: Quantas vezes o estoque gira por ano
- **Fórmula**: Giro ≈ 12 / ISR (SA)
- **ISR (SA)**: 1.29
- **Giro**: 9.30 voltas/ano
- **Nota**: Proxy anualizado para comparabilidade

---

## 11. Validação QA

### Critérios de Aceite:
- ✅ Fórmula: Giro = 12 / ISR_SA
- ✅ Unidade: voltas/ano (2 casas decimais)
- ✅ Regra BLANK: mês sem ISR_SA → BLANK
- ✅ Proteção: ISR_SA = 0 → BLANK
- ✅ 5 pontos auditados: |Giro − 12/ISR| = 0
- ✅ Tooltip com aviso de proxy

### Script de Validação:
`QA_TURNOVER_PROXY_VALIDATION.py`

---

## 12. Limitações e Avisos

### ⚠️ Este KPI é um PROXY:

1. **Fator fixo de anualização (12 meses)**:
   - Assume giro constante ao longo do ano
   - Não considera sazonalidade intra-anual

2. **Não considera mix de produtos**:
   - Agregação nacional de todos os produtos
   - Diferentes categorias têm giros distintos
   - Não reflete composição de vendas

3. **Não considera lead time**:
   - Giro real depende do ciclo de reposição
   - Cada produto/categoria tem lead time diferente

4. **Agregação nacional**:
   - Média de todo varejo dos EUA
   - Não reflete variações regionais
   - Não diferencia canais (online vs físico)

5. **Uso recomendado**:
   - Comparação de tendências ao longo do tempo
   - Benchmark macro com mercado nacional
   - Análise de eficiência relativa de estoque
   - **NÃO usar** para decisões operacionais de giro

---

## 13. Relação com Outros KPIs

### Relacionamento Matemático:

| KPI | Fórmula | Relação |
|-----|---------|---------|
| **ISR (SA)** | ISR_SA | Base |
| **DoS (dias)** | ISR_SA × 30 | Proporcional ao ISR |
| **Giro anual** | 12 / ISR_SA | **Inverso** ao ISR |

**Exemplo numérico:**
- ISR_SA = 1.29
- DoS = 1.29 × 30 = **38.7 dias**
- Giro = 12 / 1.29 = **9.30 voltas/ano**

**Observação:** ISR alto → DoS alto + Giro baixo (estoque parado)
                ISR baixo → DoS baixo + Giro alto (estoque girando rápido)

---

## 14. Validação Cruzada

### Teste de Consistência Matemática:

```
Giro (voltas/ano) × DoS (dias) ≈ 360 dias

Exemplo:
9.30 voltas/ano × 38.7 dias ≈ 360 dias ✅
```

Esta relação deve ser **sempre verdadeira** (dentro de tolerância de arredondamento).

---

## 15. Dependências

### Medidas DAX:
- `[ISR (SA)]` - Medida base obrigatória

### Tabelas:
- `FactRETAILIRSA` - Fonte de ISR_SA
- `dimmonth` - Calendário mensal

### Relacionamentos:
- `dimmonth[YearMonthKey] → FactRETAILIRSA[YearMonthKey]` (ATIVO)

---

## 16. Arquivos Relacionados

| Arquivo | Descrição |
|---------|-----------|
| `FactRETAILIRSA.csv` | Dados processados (403 meses) |
| `DAX_ISR_SA.md` | Documentação da medida base |
| `DAX_DOS_PROXY.md` | Documentação do DoS (relacionado) |
| `QA_TURNOVER_PROXY_VALIDATION.py` | Script de validação QA |
| `kpi_dictionary_pillar-B.md` | Dicionário de KPIs Pilar B |

---

**Última atualização:** 2025-11-17
**Versão:** 1.0
**Autor:** Dashboard E-Commerce Brasil - CEUB
