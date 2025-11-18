# Guias de Setup - Projeto Dashboard E-Commerce Brasil

Esta pasta contém os guias de configuração inicial (setup) do projeto. Estes arquivos foram criados durante a fase de implementação e servem como **referência histórica** e **documentação de processo**.

## ⚠️ Arquivos de Referência

Estes guias foram utilizados durante a implementação inicial e podem conter informações desatualizadas. Para documentação atualizada, consulte:

- **Dicionário de KPIs:** [../../data/metadata/kpi_dictionary_pillar-B.md](../../data/metadata/kpi_dictionary_pillar-B.md)
- **Documentação DAX:** [../dax/](../dax/)
- **Scripts QA:** [../../data/processed/pillar_b/qa/](../../data/processed/pillar_b/qa/)

## Arquivos Disponíveis

### 1. POWER_BI_SETUP.md
**Descrição:** Guia geral de configuração do Power BI Desktop para o projeto.

**Conteúdo:**
- Instruções de instalação do Power BI Desktop
- Configuração de conexão com Neon PostgreSQL
- Setup inicial do modelo de dados
- Configurações de DirectQuery
- Criação de relacionamentos básicos

**Status:** Referência histórica - verificar antes de usar

---

### 2. PILLAR_B_ISR_SA_SETUP.md
**Descrição:** Guia de setup específico para o KPI #1: ISR (SA) - KPI Principal.

**Conteúdo:**
- Criação da tabela FactRETAILIRSA no Neon
- Upload de dados RETAILIRSA.csv
- Configuração do relacionamento com dimmonth
- Implementação da medida DAX [ISR (SA)]
- Validação inicial

**Status:** Concluído - KPI implementado
**Documentação atualizada:** [../dax/DAX_ISR_SA.md](../dax/DAX_ISR_SA.md)

---

### 3. PILLAR_B_ISR_SETUP.md
**Descrição:** Guia de setup para componentes do ISR Seasonal Gap.

**Conteúdo:**
- Criação da tabela FactISRSeasonalGap no Neon
- Processamento ETL (RETAILIRSA + RETAILIRNSA)
- Cálculo do Seasonal Gap (absoluto e percentual)
- Implementação de medidas DAX derivadas
- Validação de 403 meses

**Status:** Concluído - KPIs #2-5 implementados
**Documentação atualizada:** [../../data/metadata/kpi_dictionary_pillar-B.md](../../data/metadata/kpi_dictionary_pillar-B.md)

---

## Estrutura do Projeto (Atual)

```
Projeto_integrador/
├── documentation/
│   ├── dax/                    ← Documentação técnica DAX (ATUAL)
│   └── setup/                  ← Guias de setup (REFERÊNCIA)
│
├── data/
│   ├── processed/pillar_b/
│   │   ├── FactRETAILIRSA.csv
│   │   ├── FactISRSeasonalGap.csv
│   │   └── qa/                 ← Scripts de validação (ATUAL)
│   │
│   └── metadata/
│       └── kpi_dictionary_pillar-B.md  ← Documentação principal (ATUAL)
│
└── database_setup/
    └── [Scripts SQL de criação de tabelas]
```

## Quando Usar Estes Arquivos

### ✅ Use se:
- Precisar recriar o setup do zero
- Quiser entender o processo de implementação inicial
- Estiver fazendo troubleshooting de problemas de conexão
- Precisar replicar o ambiente em outra máquina

### ❌ Não use se:
- Estiver procurando fórmulas DAX atualizadas → Use [../dax/](../dax/)
- Quiser validar KPIs → Use [../../data/processed/pillar_b/qa/](../../data/processed/pillar_b/qa/)
- Precisar de referência completa → Use [kpi_dictionary_pillar-B.md](../../data/metadata/kpi_dictionary_pillar-B.md)

## Migração de Informações

As informações destes guias foram migradas para:

| Setup Original | Documentação Atual |
|----------------|-------------------|
| POWER_BI_SETUP.md | Informações incorporadas ao dicionário de KPIs |
| PILLAR_B_ISR_SA_SETUP.md | DAX_ISR_SA.md + kpi_dictionary_pillar-B.md |
| PILLAR_B_ISR_SETUP.md | kpi_dictionary_pillar-B.md (KPIs #2-5) |

## Histórico de Implementação

### Fase 1: Setup Inicial (Nov/2024)
- ✅ Configuração Power BI Desktop
- ✅ Conexão com Neon PostgreSQL
- ✅ Upload FactRETAILIRSA (403 meses)

### Fase 2: ISR Principal (Nov/2024)
- ✅ KPI #1: ISR (SA) - KPI Principal
- ✅ Validação: 3 meses, erro 0.00

### Fase 3: ISR Seasonal Gap (Nov/2024)
- ✅ Upload FactISRSeasonalGap (403 meses)
- ✅ KPIs #2-5: Componentes Seasonal Gap
- ✅ Validação: 3 meses, erro 0.000000

### Fase 4: KPIs Derivados (Nov/2024)
- ✅ KPI #1.1: ISR MoM % (SA)
- ✅ KPI #1.2: ISR YoY % (SA)
- ✅ KPI #1.3: DoS (dias) - Proxy
- ✅ KPI #1.4: Giro anual - Proxy
- ✅ KPI #1.5: Percentil 10 anos (SA)

**Total:** 10 KPIs implementados no Pilar B

## Credenciais de Conexão

**⚠️ ATENÇÃO:** Credenciais sensíveis foram **removidas** destes arquivos por segurança.

Para conectar ao Neon PostgreSQL, consulte:
- Arquivo de configuração local (não versionado)
- Gerenciador de secrets do projeto
- Documentação interna da equipe

## Notas Importantes

1. **Não modificar** estes arquivos - são referência histórica
2. **Não commitar** alterações nesta pasta sem revisão
3. **Verificar atualização** antes de usar qualquer procedimento
4. **Priorizar** documentação em [../dax/](../dax/) e QA scripts

---

**Última atualização:** 2025-11-18
**Status:** Arquivo - Referência Histórica
**Projeto:** Dashboard E-Commerce Brasil - CEUB
