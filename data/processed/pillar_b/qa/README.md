# Scripts de Validação QA - Pilar B

Esta pasta contém todos os scripts de validação QA (Quality Assurance) e seus resultados para os KPIs do **Pilar B (Macro/Estratégico)**.

## Estrutura de Arquivos

Cada KPI possui 3 arquivos de validação:

1. **`QA_[NOME_KPI]_VALIDATION.py`**: Script Python de validação
2. **`QA_[NOME_KPI]_VALIDATION.csv`**: Resultados detalhados da validação
3. **`QA_[NOME_KPI]_Sample_12M.csv`**: Amostra dos últimos 12 meses

## Scripts Disponíveis

### KPI #1: ISR (SA) - KPI Principal
- **Script:** [QA_ISR_SA.csv](QA_ISR_SA.csv)
- **Validação:** 3 meses, erro 0.00
- **Status:** ✅ 100%

### KPI #1.1: ISR MoM % (SA)
- **Script:** [QA_ISR_MOM_VALIDATION.py](QA_ISR_MOM_VALIDATION.py)
- **Resultados:** [QA_ISR_MOM_VALIDATION.csv](QA_ISR_MOM_VALIDATION.csv)
- **Sample:** [QA_ISR_MOM_Sample_12M.csv](QA_ISR_MOM_Sample_12M.csv)
- **Validação:** 3 pares m/m-1, erro 0.0000 p.p.
- **Status:** ✅ 100% (4/4 testes)

### KPI #1.2: ISR YoY % (SA)
- **Script:** [QA_ISR_YOY_VALIDATION.py](QA_ISR_YOY_VALIDATION.py)
- **Resultados:** [QA_ISR_YOY_VALIDATION.csv](QA_ISR_YOY_VALIDATION.csv)
- **Sample:** [QA_ISR_YOY_Sample_12M.csv](QA_ISR_YOY_Sample_12M.csv)
- **Validação:** 3 comparações m vs m-12, erro 0.0000 p.p.
- **Status:** ✅ 100% (5/5 testes)

### KPI #1.3: DoS (dias) - Proxy via ISR (SA)
- **Script:** [QA_DOS_PROXY_VALIDATION.py](QA_DOS_PROXY_VALIDATION.py)
- **Resultados:** [QA_DOS_PROXY_VALIDATION.csv](QA_DOS_PROXY_VALIDATION.csv)
- **Sample:** [QA_DOS_PROXY_Sample_12M.csv](QA_DOS_PROXY_Sample_12M.csv)
- **Validação:** 5 pontos aleatórios, erro 0.0000 dias
- **Status:** ✅ 100% (6/6 testes)

### KPI #1.4: Giro anual - Proxy via ISR (SA)
- **Script:** [QA_TURNOVER_PROXY_VALIDATION.py](QA_TURNOVER_PROXY_VALIDATION.py)
- **Resultados:** [QA_TURNOVER_PROXY_VALIDATION.csv](QA_TURNOVER_PROXY_VALIDATION.csv)
- **Sample:** [QA_TURNOVER_PROXY_Sample_12M.csv](QA_TURNOVER_PROXY_Sample_12M.csv)
- **Validação:** 5 pontos aleatórios + validação cruzada Giro×DoS
- **Status:** ✅ 100% (7/7 testes)

### KPI #1.5: Percentil histórico (10 anos) - SA
- **Script:** [QA_PERCENTILE10Y_VALIDATION.py](QA_PERCENTILE10Y_VALIDATION.py)
- **Resultados:** [QA_PERCENTILE10Y_VALIDATION.csv](QA_PERCENTILE10Y_VALIDATION.csv)
- **Sample:** [QA_PERCENTILE10Y_Sample_12M.csv](QA_PERCENTILE10Y_Sample_12M.csv)
- **Validação:** 3 meses + regra BLANK (119 primeiros meses)
- **Status:** ✅ 100% (4/4 testes)

### Seasonal Gap
- **Arquivo:** [QA_ISR_Seasonal_Gap.csv](QA_ISR_Seasonal_Gap.csv)
- **Validação:** 3 meses, erro 0.000000
- **Status:** ✅ 100%

## Como Executar os Scripts

### Pré-requisitos

```bash
# Ativar ambiente virtual
source /Volumes/Crucial\ X6/Projeto_integrador/venv/bin/activate

# Ou usar o Python do venv diretamente
/Volumes/Crucial\ X6/Projeto_integrador/venv/bin/python
```

### Executar Validação

```bash
# Navegar para a pasta de dados
cd /Volumes/Crucial\ X6/Projeto_integrador/data/processed/pillar_b

# Executar script de validação
/Volumes/Crucial\ X6/Projeto_integrador/venv/bin/python qa/QA_[NOME]_VALIDATION.py
```

### Exemplo - ISR YoY %

```bash
cd /Volumes/Crucial\ X6/Projeto_integrador/data/processed/pillar_b
/Volumes/Crucial\ X6/Projeto_integrador/venv/bin/python qa/QA_ISR_YOY_VALIDATION.py
```

## Estrutura de um Script QA

Cada script de validação segue este padrão:

1. **Carregar dados** do CSV processado
2. **Calcular KPI automaticamente** usando fórmula Python
3. **Calcular KPI manualmente** para comparação
4. **Validar regras BLANK** conforme especificação
5. **Comparar resultados** (automático vs manual)
6. **Gerar relatório** de validação
7. **Salvar resultados** em CSV

## Critérios de Aceite

Cada validação verifica:

- ✅ **Fórmula correta**: Cálculo automático = manual
- ✅ **Regras BLANK**: Meses sem dados retornam BLANK
- ✅ **Tolerância**: Erro ≤ 0.01 (1 centésimo de unidade)
- ✅ **Cobertura**: Mínimo 3-5 pontos validados
- ✅ **Taxa de sucesso**: 100% dos testes

## Resultados de Validação

### Resumo Geral

| KPI | Testes | Erro Máx | Taxa Sucesso |
|-----|--------|----------|--------------|
| ISR (SA) | 3/3 | 0.00 | 100% |
| ISR MoM % | 4/4 | 0.0000 p.p. | 100% |
| ISR YoY % | 5/5 | 0.0000 p.p. | 100% |
| DoS (dias) | 6/6 | 0.0000 dias | 100% |
| Giro anual | 7/7 | 0.0000 voltas/ano | 100% |
| Percentil 10y | 4/4 | 0.00 p.p. | 100% |
| Seasonal Gap | 3/3 | 0.000000 | 100% |

**Total:** 32/32 testes passados ✅

## Dependências Python

Os scripts requerem:

- `pandas`: Manipulação de dados
- `numpy`: Cálculos numéricos

Instaladas no ambiente virtual do projeto.

## Arquivos de Saída

### Arquivo VALIDATION.csv

Contém colunas:
- `Mês`: Mês validado (formato Mon/YYYY)
- `YearMonthKey`: Chave temporal (YYYYMM)
- `ISR_SA`: Valor base do ISR
- `[KPI]_calculated`: Valor calculado automaticamente
- `[KPI]_manual`: Valor calculado manualmente
- `Erro_[unidade]`: Diferença absoluta
- `Status`: ✅ PASS ou ❌ FAIL

### Arquivo Sample_12M.csv

Contém últimos 12 meses com:
- `MonthDate`: Data do mês
- `YearMonthKey`: Chave temporal
- `ISR_SA`: Valor base
- `[KPI]`: Valor do KPI calculado

## Referências

- **Documentação DAX:** [../../../documentation/dax/](../../../documentation/dax/)
- **Dicionário de KPIs:** [../../metadata/kpi_dictionary_pillar-B.md](../../metadata/kpi_dictionary_pillar-B.md)
- **Dados Processados:** [../](../)

---

**Última atualização:** 2025-11-18
**Versão:** 1.6
**Projeto:** Dashboard E-Commerce Brasil - CEUB
