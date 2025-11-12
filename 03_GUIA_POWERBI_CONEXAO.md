# Guia: Conectar Power BI ao Azure SQL Database

## Pré-requisitos

- ✅ Azure SQL Database criado e configurado
- ✅ Dados importados (script `02_import_data_to_azure.py` executado)
- ✅ Power BI Desktop instalado
- ✅ Credenciais do banco de dados

---

## Parte 1: Instalar Power BI Desktop

### No Mac (Usando Parallels/VMWare ou Boot Camp)

⚠️ **IMPORTANTE**: Power BI Desktop é **apenas para Windows**

**Opções para usuários Mac:**

1. **Parallels Desktop** (Recomendado)
   - Permite rodar Windows no Mac
   - Melhor performance
   - Custo: ~$100/ano (tem trial de 14 dias)
   - Download: https://www.parallels.com

2. **Boot Camp** (Gratuito)
   - Instala Windows nativo no Mac
   - Gratuito (precisa licença Windows)
   - Requer reiniciar para usar Windows

3. **CrossOver** (Alternativa)
   - Roda apps Windows no Mac sem VM
   - Custo: ~$60
   - Compatibilidade limitada com Power BI

4. **Usar computador Windows** (Mais simples)
   - Lab da universidade
   - Computador de colega
   - Biblioteca/sala de informática

### No Windows

1. Acesse: https://powerbi.microsoft.com/desktop/
2. Clique em **"Download gratuito"** ou **"Baixar agora"**
3. Execute o instalador `.exe`
4. Siga o wizard de instalação
5. Inicie o Power BI Desktop

---

## Parte 2: Conectar ao Azure SQL Database

### Passo 1: Abrir Power BI Desktop

1. Abra o Power BI Desktop
2. Na tela inicial, você verá opções de "Get Data"

### Passo 2: Selecionar Fonte de Dados

1. Clique em **"Get data"** (Obter dados) no ribbon superior
   - OU clique no ícone de "Get data" na Home tab
2. Na janela que abrir:
   - Pesquise por: **"Azure SQL"** ou **"SQL Server"**
   - Selecione: **"Azure SQL database"**
3. Clique em **"Connect"** (Conectar)

### Passo 3: Configurar Conexão

Na janela de conexão, preencha:

**SQL Server database:**
```
Server: ceub-sales-server.database.windows.net
Database (optional): sales_analytics_db
```

⚠️ **IMPORTANTE**: Substitua `ceub-sales-server` pelo nome do SEU servidor!

**Data Connectivity mode:**
- Selecione: ✅ **Import** (Recomendado para dados estáticos)
  - Copia dados para o Power BI
  - Mais rápido para análises
  - Adequado para 27MB de dados

- OU

- Selecione: ⬜ **DirectQuery** (Se preferir consultar em tempo real)
  - Consulta banco ao vivo
  - Dados sempre atualizados
  - Mais lento para visualizações

**Recomendação**: Use **Import** já que os dados não mudarão

4. Clique em **"OK"**

### Passo 4: Autenticação

1. Uma janela de autenticação aparecerá
2. Selecione a aba: **"Database"** (à esquerda)
3. Preencha:
   - **User name**: `adminceub` (ou seu username)
   - **Password**: [sua senha do Azure]
4. Clique em **"Connect"**

⚠️ Se aparecer erro de certificado SSL:
- Volte e marque: "Encrypt connection" = No
- Ou: "Trust server certificate" = Yes

### Passo 5: Selecionar Tabelas

1. Uma janela "Navigator" aparecerá com as tabelas disponíveis
2. ✅ Marque as seguintes tabelas:
   - ✅ `DimMonth`
   - ✅ `DimCategoria`
   - ✅ `FactRetailMonthly`

3. **Pré-visualização**: Clique em cada tabela para ver os dados

4. Opções:
   - **Load**: Carrega dados diretamente
   - **Transform Data**: Abre Power Query para transformações

**Recomendação**: Clique em **"Load"** (os dados já foram tratados no Python)

### Passo 6: Aguardar Importação

1. Power BI importará os dados
2. Progresso aparecerá na barra inferior
3. Aguarde conclusão (deve levar 1-2 minutos para 27MB)

---

## Parte 3: Criar Relacionamentos no Modelo

### Passo 1: Abrir Model View

1. No lado esquerdo, clique no ícone **"Model"** (terceiro ícone)
   - Ou use atalho: `Ctrl + Alt + M` (Windows)

2. Você verá as 3 tabelas no canvas

### Passo 2: Criar Relacionamento 1: DimMonth → FactRetailMonthly

1. Arraste `YearMonthKey` da tabela `DimMonth`
2. Solte sobre `YearMonthKey` da tabela `FactRetailMonthly`
3. Uma linha de relacionamento aparecerá

4. Clique duas vezes na linha para editar:
   - **From table**: `DimMonth`
   - **From column**: `YearMonthKey`
   - **To table**: `FactRetailMonthly`
   - **To column**: `YearMonthKey`
   - **Cardinality**: `One to many (1:*)` ← Deve estar automático
   - **Cross filter direction**: `Single` ← Importante!
   - **Make this relationship active**: ✅ Marcado

5. Clique **"OK"**

### Passo 3: Criar Relacionamento 2: DimCategoria → FactRetailMonthly

1. Arraste `ItemType` da tabela `DimCategoria`
2. Solte sobre `ItemType` da tabela `FactRetailMonthly`
3. Uma linha de relacionamento aparecerá

4. Clique duas vezes na linha para editar:
   - **From table**: `DimCategoria`
   - **From column**: `ItemType`
   - **To table**: `FactRetailMonthly`
   - **To column**: `ItemType`
   - **Cardinality**: `One to many (1:*)` ← Automático
   - **Cross filter direction**: `Single`
   - **Make this relationship active**: ✅ Marcado

5. Clique **"OK"**

### Passo 4: Verificar Modelo

Seu modelo deve ficar assim:

```
DimMonth (1) ────► FactRetailMonthly (*)
                           ▲
                           │
DimCategoria (1) ──────────┘
```

**Verifique:**
- ✅ Setas apontam de DIM (1) para FACT (*)
- ✅ Relacionamentos estão **ativos** (linha sólida)
- ✅ Cardinalidade está correta (1:*)

---

## Parte 4: Criar Hierarquia de Categorias

### Passo 1: Criar Hierarquia

1. Na tabela `DimCategoria`:
   - Clique com botão direito em `Categoria`
   - Selecione: **"Create hierarchy"**

2. Renomeie para: `Hierarquia Produtos`

3. Arraste `ItemType` para dentro da hierarquia (abaixo de Categoria)

4. Hierarquia final:
   ```
   Hierarquia Produtos
   ├── Categoria
   └── ItemType
   ```

### Passo 2: Adicionar ItemCode (Opcional)

Se quiser drill-down até item individual:

1. Vá para tabela `FactRetailMonthly`
2. Arraste `ItemCode` para a hierarquia
3. Ficará:
   ```
   Hierarquia Produtos
   ├── Categoria (DimCategoria)
   ├── ItemType (DimCategoria)
   └── ItemCode (FactRetailMonthly)
   ```

---

## Parte 5: Criar Medidas DAX

### Passo 1: Criar Pasta de Medidas (Organização)

1. Clique com botão direito em `FactRetailMonthly`
2. Selecione: **"New measure"**
3. Digite:
```dax
_Medidas = BLANK()
```
4. Pressione Enter
5. (Opcional) Oculte essa medida: clique direito → Hide

### Passo 2: Medida 1 - Retail Sales (M)

1. Clique em **"New measure"** na ribbon
2. Digite:
```dax
Retail Sales (M) = SUM(FactRetailMonthly[RetailSales])
```
3. Pressione Enter

4. Configure formatação:
   - Selecione a medida
   - No painel "Measure tools":
     - **Format**: Currency
     - **Decimal places**: 2
     - **Currency symbol**: $ (ou R$)

### Passo 3: Medida 2 - Avg Retail Sales Prev 3M

1. Clique em **"New measure"**
2. Digite:
```dax
Avg Retail Sales Prev 3M =
VAR MaxMes = MAX(DimMonth[MonthDate])
RETURN
IF(
    CALCULATE(
        DISTINCTCOUNT(DimMonth[YearMonthKey]),
        DATESINPERIOD(
            DimMonth[MonthDate],
            EOMONTH(MaxMes, -1),
            -3,
            MONTH
        )
    ) < 3,
    BLANK(),
    AVERAGEX(
        DATESINPERIOD(
            DimMonth[MonthDate],
            EOMONTH(MaxMes, -1),
            -3,
            MONTH
        ),
        [Retail Sales (M)]
    )
)
```
3. Pressione Enter

4. Configure formatação: Currency, 2 decimais

### Passo 4: Medida 3 - Δ Vendas vs Média 3M %

1. Clique em **"New measure"**
2. Digite:
```dax
Δ Vendas vs Média 3M % =
VAR Base3M = [Avg Retail Sales Prev 3M]
RETURN
IF(
    ISBLANK(Base3M) || Base3M = 0,
    BLANK(),
    DIVIDE(
        [Retail Sales (M)] - Base3M,
        Base3M
    )
)
```
3. Pressione Enter

4. Configure formatação:
   - **Format**: Percentage
   - **Decimal places**: 1
   - **Show as**: %

### Passo 5: Organizar Medidas

1. Selecione todas as medidas criadas
2. No painel Properties:
   - **Display folder**: `KPIs`

Ficará organizado:
```
FactRetailMonthly
└── 📁 KPIs
    ├── Retail Sales (M)
    ├── Avg Retail Sales Prev 3M
    └── Δ Vendas vs Média 3M %
```

---

## Parte 6: Criar Card de KPI (Exemplo)

### Passo 1: Adicionar Visual

1. Clique na aba **"Report"** (primeiro ícone à esquerda)
2. No painel Visualizations, clique em **"Card"**
3. Arraste para o canvas

### Passo 2: Configurar Card

1. Arraste a medida `Δ Vendas vs Média 3M %` para **"Fields"**
2. O card mostrará o valor

### Passo 3: Formatar Card

1. Selecione o card
2. No painel Format (ícone de pincel):
   - **Callout value**: Ajuste tamanho da fonte
   - **Category label**: Renomeie para "Tendência 3M (%)"
   - **Conditional formatting**: Adicione cores
     - Verde se > 0%
     - Vermelho se < 0%

### Passo 4: Adicionar Tooltip (Informações Extras)

1. Crie uma página de Tooltip:
   - Nova página → Page Information → Set as tooltip page
2. Adicione cards com:
   - `Retail Sales (M)` → "Vendas Mês Atual"
   - `Avg Retail Sales Prev 3M` → "Média 3M Anterior"
   - `Δ Vendas vs Média 3M %` → "Variação %"
3. Adicione texto explicativo

---

## Parte 7: Atualizar Dados (Refresh)

### Refresh Manual

1. Na ribbon, clique em **"Refresh"**
2. Power BI consultará o Azure SQL e atualizará dados
3. Use quando houver mudanças no banco

### Configurar Refresh Automático (Power BI Service)

⚠️ Requer: Power BI Pro ou Premium Per User ($10/mês)

1. Publique o relatório: **Home → Publish**
2. No Power BI Service (app.powerbi.com):
   - Vá para Dataset Settings
   - Configure "Scheduled refresh"
   - Máximo: 8x por dia

---

## Troubleshooting

### Erro: "Cannot connect to database"

✅ **Soluções:**
1. Verifique credenciais (username/password)
2. Confirme nome do servidor correto
3. Adicione seu IP no firewall do Azure
4. Teste conexão via Azure Data Studio primeiro

### Erro: "Login failed for user"

✅ **Soluções:**
1. Confirme username: `adminceub` (sem domínio)
2. Verifique senha (sem espaços extras)
3. Use autenticação **Database**, não Windows

### Erro: "Timeout expired"

✅ **Soluções:**
1. Conexão lenta - aguarde mais tempo
2. Se serverless: primeiro acesso demora ~30s
3. Reduza timeout: File → Options → Current File → Data Load

### Medidas DAX retornam erro

✅ **Soluções:**
1. Verifique nomes das colunas (case-sensitive)
2. Certifique-se que relacionamentos estão ativos
3. Teste medidas simples primeiro (`SUM(...)`)
4. Use DAX Formatter online para formatar código

### Relacionamentos não criam automaticamente

✅ **Soluções:**
1. Crie manualmente (arraste campo entre tabelas)
2. Verifique tipos de dados compatíveis
3. Confirme que colunas têm mesmos valores

---

## Checklist Final

- [ ] Power BI Desktop instalado
- [ ] Conectado ao Azure SQL Database
- [ ] 3 tabelas importadas (DimMonth, DimCategoria, FactRetailMonthly)
- [ ] Relacionamentos criados (2 relacionamentos ativos 1:*)
- [ ] Hierarquia de produtos criada
- [ ] 3 medidas DAX implementadas
- [ ] Card de KPI criado e formatado
- [ ] Tooltip configurado
- [ ] Teste de refresh manual funcionando

---

## Próximos Passos

1. ✅ Criar visualizações (gráficos de linha, barras, etc.)
2. ✅ Aplicar filtros e slicers
3. ✅ Criar dashboard completo
4. ✅ Compartilhar .pbix com equipe via OneDrive
5. ✅ (Opcional) Publicar no Power BI Service

---

## Recursos de Aprendizado

- **DAX Guide**: https://dax.guide
- **SQLBI (Experts)**: https://sqlbi.com
- **Guy in a Cube (YouTube)**: Tutoriais em vídeo
- **Microsoft Learn**: Power BI learning paths
- **Comunidade**: community.powerbi.com

---

**Criado em**: 2024-11-10
**Versão**: 1.0
**Projeto**: Sales Analytics - Power BI - CEUB
