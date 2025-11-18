# 📊 Guia Completo - Setup Power BI
**Projeto: Sales Analytics - CEUB**
**Data:** Novembro 2025

---

## 🔌 PASSO 1: Conectar ao Banco Neon PostgreSQL

### Credenciais de Conexão:
```
Server: ep-patient-dawn-aciwozz1-pooler.sa-east-1.aws.neon.tech:5432
Database: neondb
User: neondb_owner
Password: npg_LiH0fcSJjy6b
```

### Como Conectar:
1. Abra Power BI Desktop
2. **Get Data** → **PostgreSQL database**
3. Preencha:
   - **Server:** `ep-patient-dawn-aciwozz1-pooler.sa-east-1.aws.neon.tech:5432`
   - **Database:** `neondb`
4. Data Connectivity mode: **Import**
5. Clique **OK**
6. Na autenticação:
   - Selecione aba **Database**
   - **User name:** `neondb_owner`
   - **Password:** `npg_LiH0fcSJjy6b`
7. Clique **Connect**

---

## 📦 PASSO 2: Importar Tabelas

Selecione as **4 tabelas** abaixo do Neon PostgreSQL:

- ✅ **dimmonth** (444 registros)
- ✅ **dimcategoria** (8 registros)
- ✅ **factretailmonthly** (307,644 registros)
  - ⚠️ **Nota**: Esta tabela contém `retailsales` E `retailtransfers` - use para Taxa de Transferência!
- ✅ **factinventorysnapshotmonthly** (6,785 registros)

Clique em **Load**

---

## 🔗 PASSO 3: Criar Relacionamentos (Model View)

Vá para **Model View** (ícone de 3 caixas conectadas no menu lateral)

### Relacionamento 1: DimMonth → FactRetailMonthly
- Arraste `dimmonth[yearmonthkey]` → `factretailmonthly[yearmonthkey]`
- **Cardinalidade:** One-to-Many (1:*)
- **Cross-filter direction:** Single
- **Make this relationship active:** ✅ Sim

### Relacionamento 2: DimCategoria → FactRetailMonthly
- Arraste `dimcategoria[itemtype]` → `factretailmonthly[itemtype]`
- **Cardinalidade:** One-to-Many (1:*)
- **Cross-filter direction:** Single
- **Make this relationship active:** ✅ Sim

### Relacionamento 3: DimMonth → FactInventorySnapshotMonthly
- Arraste `dimmonth[yearmonthkey]` → `factinventorysnapshotmonthly[yearmonthkey]`
- **Cardinalidade:** One-to-Many (1:*)
- **Cross-filter direction:** Single
- **Make this relationship active:** ✅ Sim

---

## 📐 PASSO 4: Criar Medidas DAX

Vá para **Report View** ou **Data View**

### Opção A: Organizar em Pastas (Recomendado)

Crie uma tabela vazia para organizar medidas:
1. **Home** → **Enter Data** → Nomeie como `_Measures`
2. Delete as colunas padrão, deixe vazia
3. Crie medidas dentro dessa tabela

---

## 📁 MEDIDAS - Pasta: _Base Measures

### 1️⃣ Retail Sales (M)
```dax
Retail Sales (M) = SUM(factretailmonthly[retailsales])
```
**Formatação:**
- Formato: Currency ($)
- Decimal places: 2
- Display Units: None

---

### 2️⃣ Days in Month (M)
```dax
Days in Month (M) = SELECTEDVALUE(dimmonth[daysinmonth])
```
**Formatação:**
- Formato: Whole Number
- Decimal places: 0

---

### 3️⃣ Vendas_dia_$
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
**Formatação:**
- Formato: Currency ($)
- Decimal places: 2
- Display Units: None

**Descrição (opcional):**
"Vendas médias por dia (normalizado por dias do mês)"

---

## 📁 MEDIDAS - Pasta: Tendência

### 4️⃣ Avg Retail Sales Prev 3M
```dax
Avg Retail Sales Prev 3M =
VAR MaxMes = MAX(dimmonth[monthdate])
VAR CountMeses =
    CALCULATE(
        DISTINCTCOUNT(dimmonth[yearmonthkey]),
        DATESINPERIOD(
            dimmonth[monthdate],
            EOMONTH(MaxMes, -1),
            -3,
            MONTH
        )
    )
RETURN
    IF(
        CountMeses < 3,
        BLANK(),
        AVERAGEX(
            DATESINPERIOD(
                dimmonth[monthdate],
                EOMONTH(MaxMes, -1),
                -3,
                MONTH
            ),
            [Retail Sales (M)]
        )
    )
```
**Formatação:**
- Formato: Currency ($)
- Decimal places: 2

**Regra:** Retorna BLANK se menos de 3 meses disponíveis

---

### 5️⃣ Δ Vendas vs Média 3M %
```dax
Δ Vendas vs Média 3M % =
VAR Base3M = [Avg Retail Sales Prev 3M]
RETURN
    IF(
        ISBLANK(Base3M) || Base3M = 0,
        BLANK(),
        DIVIDE([Retail Sales (M)] - Base3M, Base3M)
    )
```
**Formatação:**
- Formato: Percentage (%)
- Decimal places: 1

**Descrição:**
"Tendência 3M: crescimento positivo ou queda nas vendas"

**Regra:** BLANK se <3 meses ou média=0

---

## 📁 MEDIDAS - Pasta: Inventário

### 6️⃣ Stock Value (Snapshot)
```dax
Stock Value (Snapshot) = SUM(factinventorysnapshotmonthly[stockvalue])
```
**Formatação:**
- Formato: Currency ($)
- Decimal places: 2

**Descrição:**
"Proxy: snapshot único de 18/09/2025. Não reflete estoque médio real."

---

### 7️⃣ DoS (Dias, Proxy)
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
**Formatação:**
- Formato: Whole Number
- Decimal places: 0

**Descrição:**
"DoS (Proxy): Estimativa em valor ($) usando snapshot de 18/09/2025. BLANK se sem dados de venda ou match entre inventário e vendas (56.2% de cobertura)."

**Regra:** BLANK se vendas/dia ≤ 0 ou sem match inventory↔sales

---

## 📁 MEDIDAS AUXILIARES (Opcional - para debug)

### 8️⃣ Total Inventory (Debug)
```dax
Total Inventory = SUM(factinventorysnapshotmonthly[totalinventory])
```
**Formatação:** Whole Number

---

### 9️⃣ Average Price (Debug)
```dax
Average Price = AVERAGE(factinventorysnapshotmonthly[price])
```
**Formatação:** Currency ($), 2 decimais

---

## 🎨 TABELA RESUMO DE FORMATAÇÃO

| Medida | Tipo | Decimais | Display Units |
|--------|------|----------|---------------|
| Retail Sales (M) | Currency | 2 | None |
| Days in Month (M) | Whole Number | 0 | None |
| Vendas_dia_$ | Currency | 2 | None |
| Avg Retail Sales Prev 3M | Currency | 2 | None |
| Δ Vendas vs Média 3M % | Percentage | 1 | None |
| Stock Value (Snapshot) | Currency | 2 | None |
| DoS (Dias, Proxy) | Whole Number | 0 | None |

---

## ✅ CHECKLIST DE VALIDAÇÃO

### Conexão e Importação:
- [ ] 4 tabelas importadas com sucesso
- [ ] Número de registros conferido (dimmonth: 444, dimcategoria: 8, factretailmonthly: 307,644, factinventorysnapshotmonthly: 6,785)

### Relacionamentos:
- [ ] dimmonth → factretailmonthly (ativo, 1:*)
- [ ] dimcategoria → factretailmonthly (ativo, 1:*)
- [ ] dimmonth → factinventorysnapshotmonthly (ativo, 1:*)

### Medidas:
- [ ] 7 medidas principais criadas
- [ ] Formatação aplicada conforme tabela acima
- [ ] Testado cada medida em um visual simples (card)

### Validação de Dados:
- [ ] Retail Sales (M) retorna valores > 0
- [ ] Δ Vendas vs Média 3M % retorna BLANK para primeiros 3 meses
- [ ] DoS (Dias, Proxy) retorna valores entre 0-365 dias (ou BLANK)

---

## 🎯 ESTRUTURA DE PÁGINAS SUGERIDA

```
📁 Dashboard_Vendas_CEUB.pbix
│
├── 📄 Página 1: Visão Geral
│   ├── 4 Cards principais (KPIs)
│   ├── Gráfico de linha: Vendas mensais
│   └── Tabela: Top 10 produtos
│
├── 📄 Página 2: Análise de Tendência
│   ├── Gráfico combo: Retail Sales + Δ 3M%
│   ├── Matrix: Categoria × Mês × Δ 3M%
│   └── Slicer: Categoria
│
├── 📄 Página 3: Análise de Inventário (DoS)
│   ├── Gráfico de barras: DoS por Categoria
│   ├── Scatter: StockValue × Vendas_dia_$
│   └── Tabela: Items críticos (DoS < 30 dias)
│
└── 📄 Página 4: Análise Cruzada
    └── Matrix: DoS × Δ Vendas 3M%
```

---

## ⚠️ LIMITAÇÕES CONHECIDAS

### DoS (Days of Supply):
- **Match de 56.2%** entre inventário e vendas
- Dos 6,785 itens de inventário, apenas 3,811 têm vendas correspondentes
- Items sem match retornam **BLANK**
- Snapshot fixo de **18/09/2025** - não reflete estoque médio real
- Cálculo em **valor ($)**, não em unidades físicas

### Δ Vendas vs Média 3M %:
- Retorna **BLANK** se menos de 3 meses de histórico
- Retorna **BLANK** se média dos 3 meses anteriores = 0

---

## 📁 MEDIDAS - Pasta: Giro (Turnover)

### 🔧 Parâmetro: Giro Max per Month

**Criar Parâmetro Numérico:**
1. **Modeling** → **New Parameter** → **Numeric Range**
2. Configurações:
   - **Name:** `Giro Max per Month Param`
   - **Minimum:** 5
   - **Maximum:** 60
   - **Increment:** 1
   - **Default:** 30
   - **Add slicer to this page:** ✅ Sim (opcional)

---

### 🔟 Giro Max (mpm)
```dax
Giro Max (mpm) = 'Giro Max per Month Param'[Giro Max per Month Param Value]
```
**Formatação:**
- Formato: Whole Number
- Decimal places: 0

**Descrição:** Limite superior para censura do Giro (valor do parâmetro)

---

### 1️⃣1️⃣ Giro (voltas/mês)
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
**Formatação:**
- Formato: Decimal Number
- Decimal places: 2
- Display Units: None
- Sufixo: " voltas/mês" (opcional, configurar em Format)

**Descrição:**
"Giro Mensal (valor): velocidade de renovação do estoque. Quanto maior, mais rápido o estoque se renova."

**Tooltip sugerido:**
"Fórmula: 30 ÷ DoS (dias). Proxy baseado em valor ($), não unidades. Herda limitações do DoS (snapshot único 18/09/2025). Valores <1: estoque parado; >4: risco de ruptura."

**Regras:**
- BLANK se DoS ≤ 0 ou BLANK
- Limitado ao valor do parâmetro (default: 30 voltas/mês)
- Usa 30 dias para comparabilidade entre meses

---

## 📚 DOCUMENTAÇÃO ADICIONAL

- **KPI Dictionary:** `data/metadata/kpi_dictionary.md`
- **QA Test Cases:** `data/metadata/qa_kpi_delta_vendas_3m.csv`
- **Key Map (Inventory↔Sales):** `data/metadata/KeyMap_Inventory_Sales.csv`

---

## 📊 MEDIDAS DAX - Taxa de Transferência

### 10. Retail Sales (M) - Transfer Rate

```dax
Retail Sales (M) = SUM(factretailmonthly[retailsales])
```

**Formato**: Currency ($)
**Casas decimais**: 2
**Nota**: Usa a mesma tabela `factretailmonthly` que já existe no Neon

---

### 11. Retail Transfers (M)

```dax
Retail Transfers (M) = SUM(factretailmonthly[retailtransfers])
```

**Formato**: Currency ($)
**Casas decimais**: 2

---

### 12. Outflow (M)

```dax
Outflow (M) = [Retail Sales (M)] + [Retail Transfers (M)]
```

**Formato**: Currency ($)
**Casas decimais**: 2
**Descrição**: Saída total do varejo (vendas + transferências)

---

### 13. Taxa de Transferência (%)

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

**Formato**: Percentage (%)
**Casas decimais**: 1

**Regras BLANK**:
- Se `Outflow = 0` → BLANK
- Se `Outflow = NULL` → BLANK
- Se `Retail Transfers = NULL` → BLANK
- Se `Retail Sales = NULL` → BLANK

**Interpretação**:
- **0-20%**: Vendas diretas predominam (padrão saudável)
- **20-40%**: Rebalanceamento moderado entre lojas
- **40%+**: Alta movimentação entre lojas (investigar desbalanceamento)

---

### 14. Faixa de Taxa (helper)

```dax
Faixa de Taxa =
VAR Taxa = [Taxa de Transferência (%)]
RETURN
    SWITCH(
        TRUE(),
        ISBLANK(Taxa), BLANK(),
        Taxa < 0.20, "0-20% (Vendas diretas)",
        Taxa < 0.40, "20-40% (Rebalanc. moderado)",
        "40-100% (Alta transferência)"
    )
```

**Uso**: Segmentação/categorização em visuais

---

## 🆘 TROUBLESHOOTING

### Problema: "Não consigo conectar ao Neon"
**Solução:**
1. Verifique se o projeto Neon está ativo (pode pausar após inatividade)
2. Teste credenciais usando ferramenta como DBeaver ou pgAdmin
3. Verifique firewall/VPN

### Problema: "Medidas retornam BLANK ou erro"
**Solução:**
1. Verifique se relacionamentos estão ativos
2. Confira se nomes de colunas estão corretos (tudo em minúsculo no Neon)
3. Teste cada medida base primeiro (Retail Sales (M), Days in Month (M))

### Problema: "DoS retorna só BLANK"
**Solução:**
1. Verifique se importou `factinventorysnapshotmonthly`
2. Verifique relacionamento dimmonth → factinventorysnapshotmonthly
3. Lembre-se: 43.8% dos items não têm match e retornarão BLANK (esperado)

---

**Última atualização:** 2025-11-11
**Versão:** 1.0
**Autor:** Claude Code + Equipe CEUB
