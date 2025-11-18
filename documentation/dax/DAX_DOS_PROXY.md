# DAX - DoS (dias) - Proxy via ISR (SA)

**KPI:** Days of Supply (Proxy)
**Nome Técnico:** `kpi_dos_days_sa_proxy`
**Pilar:** B (Macro/Estratégico)
**Data:** 2025-11-17

---

## 1. Objetivo

Aproximar **Days of Supply (DoS)** em dias a partir do ISR (SA), usando fator fixo de 30 dias para comparabilidade mensal.

---

## 2. Fórmula Matemática

```
DoS (dias) ≈ ISR_SA × 30
```

**Onde:**
- `ISR_SA` = Inventories-to-Sales Ratio (Seasonally Adjusted)
- `30` = Fator fixo de conversão (aproximação de mês médio)

**Interpretação:**
- DoS indica quantos dias de venda o estoque atual suportaria
- Fator 30 usado para comparabilidade (não considera calendário real)
- É uma **aproximação/proxy** - não usa lead time real nem dias úteis

---

## 3. Fórmula DAX (Power BI)

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

**Componentes:**
- `[ISR (SA)]`: Medida base do ISR ajustado sazonalmente
- `30`: Fator de conversão fixo (dias médios por mês)
- `IF/ISBLANK`: Regra de BLANK para meses sem ISR_SA

---

## 4. Características

| Propriedade | Valor |
|-------------|-------|
| **Tipo** | Medida derivada (proxy) |
| **Unidade** | Dias (número decimal) |
| **Formato** | Número, 1 casa decimal |
| **Grão** | Mês (série nacional) |
| **Período** | Jan/1992 - Jul/2025 (403 meses) |
| **Dependências** | [ISR (SA)] |

---

## 5. Regras de BLANK

| Condição | Resultado |
|----------|-----------|
| Mês sem ISR_SA | BLANK |
| Mês com ISR_SA | DoS = ISR_SA × 30 |

**Exemplo:**
- ISR_SA = 1.29 → DoS ≈ 38.7 dias
- ISR_SA = BLANK → DoS = BLANK

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

| DoS (dias) | Interpretação | ISR_SA Equiv. |
|------------|---------------|---------------|
| < 30 | Cobertura baixa (< 1 mês) | < 1.0 |
| 30 - 45 | Cobertura normal (1-1.5 meses) | 1.0 - 1.5 |
| 45 - 60 | Cobertura alta (1.5-2 meses) | 1.5 - 2.0 |
| > 60 | Excesso de estoque (> 2 meses) | > 2.0 |

**Nota:** Valores são aproximações. DoS real depende de:
- Dias úteis do mês (28-31)
- Lead time específico por produto
- Sazonalidade intra-mês

---

## 8. Estatísticas da Série (Jan/1992 - Jul/2025)

### Baseado em ISR_SA × 30:

| Métrica | Valor | Mês |
|---------|-------|-----|
| **Mínimo** | 32.7 dias | Jun/2021 (ISR=1.09) |
| **Máximo** | 52.5 dias | Abr/1995 (ISR=1.75) |
| **Média** | 44.7 dias | ISR médio=1.49 |
| **Mediana** | 44.7 dias | ISR mediano=1.49 |
| **Último (Jul/2025)** | 38.7 dias | ISR=1.29 |

---

## 9. Formatação no Power BI

### Card Principal
```
Formato: Número
Casas decimais: 1
Sufixo: " dias"
Exemplo: 38.7 dias
```

### Tooltip
```
DoS (dias) - Proxy: 38.7 dias
ISR (SA): 1.29
Período: Jul/2025

⚠️ Proxy com fator fixo 30 dias/mês
Não considera calendário real nem lead time
```

---

## 10. Caso de Uso

### Exemplo de Card
```
┌─────────────────────────┐
│ DoS (dias) - Proxy      │
│                         │
│      38.7 dias          │
│                         │
│ ⚠️ Aproximação (30d/mês)│
└─────────────────────────┘
```

### Tooltip Detalhado
- **Definição**: Cobertura de estoque aproximada em dias
- **Fórmula**: DoS ≈ ISR (SA) × 30
- **ISR (SA)**: 1.29
- **DoS (dias)**: 38.7 dias
- **Nota**: Proxy com fator fixo para comparabilidade

---

## 11. Validação QA

### Critérios de Aceite:
- ✅ Fórmula: DoS = ISR_SA × 30
- ✅ Unidade: dias (1 casa decimal)
- ✅ Regra BLANK: mês sem ISR_SA → BLANK
- ✅ 5 pontos auditados: |DoS − ISR×30| = 0
- ✅ Tooltip com aviso de proxy

### Script de Validação:
`QA_DOS_PROXY_VALIDATION.py`

---

## 12. Limitações e Avisos

### ⚠️ Este KPI é um PROXY:

1. **Fator fixo 30 dias/mês**:
   - Não considera dias reais do mês (28-31)
   - Não diferencia dias úteis vs finais de semana

2. **Não considera lead time**:
   - DoS real depende do ciclo de reposição
   - Cada produto tem lead time diferente

3. **Agregação nacional**:
   - Média de todo varejo dos EUA
   - Não reflete variações regionais

4. **Uso recomendado**:
   - Comparação de tendências ao longo do tempo
   - Benchmark macro com mercado nacional
   - **NÃO usar** para decisões operacionais de estoque

---

## 13. Dependências

### Medidas DAX:
- `[ISR (SA)]` - Medida base obrigatória

### Tabelas:
- `FactRETAILIRSA` - Fonte de ISR_SA
- `dimmonth` - Calendário mensal

### Relacionamentos:
- `dimmonth[YearMonthKey] → FactRETAILIRSA[YearMonthKey]` (ATIVO)

---

## 14. Arquivos Relacionados

| Arquivo | Descrição |
|---------|-----------|
| `FactRETAILIRSA.csv` | Dados processados (403 meses) |
| `DAX_ISR_SA.md` | Documentação da medida base |
| `QA_DOS_PROXY_VALIDATION.py` | Script de validação QA |
| `kpi_dictionary_pillar-B.md` | Dicionário de KPIs Pilar B |

---

**Última atualização:** 2025-11-17
**Versão:** 1.0
**Autor:** Dashboard E-Commerce Brasil - CEUB
