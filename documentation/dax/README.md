# Documentação DAX - Pilar B

Esta pasta contém a documentação completa de todas as medidas DAX do **Pilar B (Macro/Estratégico)** do projeto Dashboard E-Commerce Brasil - CEUB.

## Estrutura de Arquivos

Cada arquivo de documentação DAX segue o padrão `DAX_[NOME_KPI].md` e contém:

- Objetivo da medida
- Fórmulas (matemática e DAX)
- Características e formatação
- Regras de BLANK
- Fontes de dados e dependências
- Interpretação de valores
- Estatísticas históricas
- Casos de uso e tooltips
- Validação QA
- Limitações e avisos

## Arquivos Disponíveis

### KPI #1: ISR (SA) - KPI Principal
**Arquivo:** [DAX_ISR_SA.md](DAX_ISR_SA.md)
- **Descrição:** Valor mensal do ISR ajustado sazonalmente
- **Fonte:** FRED RETAILIRSA
- **Período:** Jan/1992 - Jul/2025 (403 meses)

### KPI #1.1: ISR MoM % (SA)
**Arquivo:** [DAX_ISR_MOM.md](DAX_ISR_MOM.md)
- **Descrição:** Variação percentual mês a mês do ISR_SA
- **Fórmula:** MoM% = (ISR_SA(m) − ISR_SA(m−1)) / ISR_SA(m−1)
- **Período:** Fev/1992 - Jul/2025 (402 valores)

### KPI #1.2: ISR YoY % (SA)
**Arquivo:** [DAX_ISR_YOY.md](DAX_ISR_YOY.md)
- **Descrição:** Variação percentual ano a ano do ISR_SA
- **Fórmula:** YoY% = (ISR_SA(m) − ISR_SA(m−12)) / ISR_SA(m−12)
- **Período:** Jan/1993 - Jul/2025 (391 valores)

### KPI #1.3: DoS (dias) - Proxy via ISR (SA)
**Arquivo:** [DAX_DOS_PROXY.md](DAX_DOS_PROXY.md)
- **Descrição:** Aproximação de Days of Supply em dias
- **Fórmula:** DoS ≈ ISR_SA × 30
- **Período:** Jan/1992 - Jul/2025 (403 valores)
- **⚠️ PROXY:** Fator fixo 30 dias/mês

### KPI #1.4: Giro anual - Proxy via ISR (SA)
**Arquivo:** [DAX_TURNOVER_PROXY.md](DAX_TURNOVER_PROXY.md)
- **Descrição:** Aproximação de Giro de Estoque Anualizado em voltas/ano
- **Fórmula:** Giro ≈ 12 / ISR_SA
- **Período:** Jan/1992 - Jul/2025 (403 valores)
- **⚠️ PROXY:** Fator fixo 12 meses de anualização

### KPI #1.5: Percentil histórico (10 anos) - SA
**Arquivo:** [DAX_PERCENTILE10Y.md](DAX_PERCENTILE10Y.md)
- **Descrição:** Posição percentual do ISR_SA em janela móvel de 120 meses
- **Fórmula:** Percentil em janela {ISR_SA(m-119)...ISR_SA(m)}
- **Período:** Dez/2001 - Jul/2025 (284 valores)
- **Janela:** 120 meses (10 anos)

### Taxa de Transferência (Pilar A)
**Arquivo:** [DAX_TAXA_TRANSFERENCIA.md](DAX_TAXA_TRANSFERENCIA.md)
- **Descrição:** KPI do Pilar A (Micro/Operacional)
- **Nota:** Arquivo mantido para referência

## Convenções de Nomenclatura

- **Nome Técnico DAX:** Usa espaços e caracteres especiais para legibilidade no Power BI
  - Exemplo: `ISR (SA)`, `Percentil 10 anos (SA)`

- **Nome Técnico no Dicionário:** Usa snake_case com prefixo `kpi_`
  - Exemplo: `kpi_isr_sa`, `kpi_isr_percentile10y_sa`

## Como Usar

1. **Leia a documentação** do KPI desejado para entender a fórmula e dependências
2. **Copie o código DAX** da seção "Fórmula DAX (Power BI)"
3. **Cole no Power BI Desktop** criando uma nova medida
4. **Renomeie a medida** conforme especificado na seção "Nome Técnico"
5. **Configure a formatação** conforme seção "Formatação no Power BI"
6. **Valide** usando os critérios da seção "Validação QA"

## Dependências Comuns

Todas as medidas derivadas do ISR (SA) dependem de:

- **Tabela:** `FactRETAILIRSA`
- **Medida base:** `[ISR (SA)]`
- **Calendário:** `dimmonth`
- **Relacionamento:** `dimmonth[YearMonthKey] → FactRETAILIRSA[YearMonthKey]` (ATIVO)

## Referências

- **Dicionário de KPIs:** [kpi_dictionary_pillar-B.md](../../data/metadata/kpi_dictionary_pillar-B.md)
- **Scripts de Validação QA:** [../data/processed/pillar_b/qa/](../../data/processed/pillar_b/qa/)
- **Setup do Pilar B:** PILLAR_B_ISR_SA_SETUP.md, PILLAR_B_ISR_SETUP.md

---

**Última atualização:** 2025-11-18
**Versão:** 1.6
**Projeto:** Dashboard E-Commerce Brasil - CEUB
