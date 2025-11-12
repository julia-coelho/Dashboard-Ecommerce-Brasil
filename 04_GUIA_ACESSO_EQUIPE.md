# Guia de Acesso para Equipe - Azure SQL Database

## Informações de Acesso

### 🔐 Credenciais do Banco de Dados

⚠️ **IMPORTANTE**: Guarde essas informações em local seguro!

```
SERVER: ceub-sales-server.database.windows.net
DATABASE: sales_analytics_db
USERNAME: adminceub
PASSWORD: [PREENCHER COM SUA SENHA]
PORT: 1433
```

**⚠️ ATENÇÃO**:
- Substitua `ceub-sales-server` pelo nome real do SEU servidor Azure
- A senha é a que você definiu ao criar o servidor SQL
- NÃO compartilhe essas credenciais publicamente (WhatsApp, email aberto, etc.)

---

## Como Adicionar Seu IP ao Firewall

Cada membro da equipe precisa adicionar seu IP para acessar o banco.

### Método 1: Auto-Serviço (Recomendado)

1. **Descubra seu IP público**:
   - Acesse: https://whatismyipaddress.com
   - Anote o número que aparece (exemplo: `177.23.45.67`)

2. **Peça para o administrador adicionar seu IP**:
   - Envie seu IP por mensagem privada
   - Admin adiciona no Azure Portal → SQL Server → Networking

### Método 2: Via Azure Portal (Se tiver acesso)

1. Acesse: https://portal.azure.com
2. Faça login com as credenciais compartilhadas
3. Vá para **SQL databases** → `sales_analytics_db`
4. Clique em **"Set server firewall"** (ou "Networking")
5. Clique em **"+ Add client IP"**
6. Seu IP será adicionado automaticamente
7. Clique em **"Save"**

⚠️ **IMPORTANTE**: Se seu IP mudar (mudou de rede, reiniciou roteador), repita o processo!

---

## Como Conectar ao Banco de Dados

### Opção 1: Power BI Desktop (Principal)

Siga o guia: `03_GUIA_POWERBI_CONEXAO.md`

**Resumo rápido:**
1. Abra Power BI Desktop
2. Get Data → Azure SQL Database
3. Preencha:
   - Server: `ceub-sales-server.database.windows.net`
   - Database: `sales_analytics_db`
4. Autenticação: Database
   - Username: `adminceub`
   - Password: [senha compartilhada]
5. Selecione tabelas e Load

### Opção 2: Azure Data Studio (Para explorar dados)

**Download**: https://aka.ms/azuredatastudio-macos (Mac) ou Windows version

**Conexão:**
1. Abra Azure Data Studio
2. New Connection
3. Preencha:
   - **Connection type**: Microsoft SQL Server
   - **Server**: `ceub-sales-server.database.windows.net`
   - **Authentication type**: SQL Login
   - **User name**: `adminceub`
   - **Password**: [senha]
   - **Database**: `sales_analytics_db`
   - **Encrypt**: True
4. Connect

### Opção 3: DBeaver (Alternativa)

Se já usa DBeaver:

1. New Connection → SQL Server
2. Preencha:
   - **Host**: `ceub-sales-server.database.windows.net`
   - **Port**: 1433
   - **Database**: `sales_analytics_db`
   - **Username**: `adminceub`
   - **Password**: [senha]
   - **Use SSL**: Yes
3. Test Connection → OK

---

## Estrutura do Banco de Dados

### Tabelas Disponíveis

**1. DimMonth** (Dimensão Temporal)
```
Colunas:
- YearMonthKey (PK) - Formato: YYYYMM (ex: 202001)
- MonthDate - Data do mês
- Year - Ano
- MonthNumber - Número do mês (1-12)
- MonthNamePT - Nome do mês em português
- YearMonth - Formato YYYY-MM
- DaysInMonth - Dias no mês
- StartOfMonth - Primeiro dia do mês
- EndOfMonth - Último dia do mês

Registros: ~444 (1992-2028)
```

**2. DimCategoria** (Dimensão de Categorias)
```
Colunas:
- CategoriaID (PK) - ID único
- ItemType - Tipo do item (WINE, BEER, LIQUOR, etc.)
- Categoria - Categoria agregada (Bebidas Alcoólicas, Suprimentos)

Registros: 5
```

**3. FactRetailMonthly** (Fato - Vendas Mensais)
```
Colunas:
- YearMonthKey (FK) - Chave para DimMonth
- ItemCode - Código do item
- ItemDescription - Descrição do item
- ItemType (FK) - Chave para DimCategoria
- RetailSales - Vendas no varejo ($)
- RetailTransfers - Transferências
- WarehouseSales - Vendas no armazém ($)
- TotalSales - Total de vendas ($)

Registros: ~variável (depende dos dados)
```

### Relacionamentos

```
DimMonth[YearMonthKey] (1) ──► FactRetailMonthly[YearMonthKey] (*)
DimCategoria[ItemType] (1) ──► FactRetailMonthly[ItemType] (*)
```

---

## Regras de Uso

### ✅ Permitido

- ✅ Consultar dados (SELECT)
- ✅ Conectar Power BI Desktop
- ✅ Criar visualizações e dashboards
- ✅ Compartilhar arquivos .pbix com a equipe
- ✅ Exportar dados para análise

### ❌ NÃO Permitido

- ❌ Deletar dados (DELETE)
- ❌ Modificar estrutura de tabelas (ALTER TABLE)
- ❌ Criar novas tabelas (sem autorização)
- ❌ Compartilhar credenciais publicamente
- ❌ Usar para projetos não relacionados

⚠️ **Se precisar modificar dados**: Fale com o administrador do banco

---

## Criando Usuários Read-Only (Para Admin)

Se quiser criar usuários individuais para cada membro (mais seguro):

### Passo 1: Conectar ao Banco

Use Azure Data Studio ou Azure Portal Query Editor

### Passo 2: Criar Login no Servidor

```sql
-- No contexto do banco 'master'
CREATE LOGIN [nome_do_membro] WITH PASSWORD = 'SenhaSegura123!';
```

### Passo 3: Criar User no Database

```sql
-- No contexto do banco 'sales_analytics_db'
CREATE USER [nome_do_membro] FOR LOGIN [nome_do_membro];
```

### Passo 4: Dar Permissão Read-Only

```sql
-- Permissão de leitura em todas as tabelas
ALTER ROLE db_datareader ADD MEMBER [nome_do_membro];

-- OU permissão específica por tabela
GRANT SELECT ON DimMonth TO [nome_do_membro];
GRANT SELECT ON DimCategoria TO [nome_do_membro];
GRANT SELECT ON FactRetailMonthly TO [nome_do_membro];
```

### Passo 5: Compartilhar Credenciais

Envie privativamente para o membro:
```
Username: nome_do_membro
Password: SenhaSegura123!
```

**Vantagens**:
- ✅ Cada membro tem credenciais próprias
- ✅ Possível rastrear quem acessou
- ✅ Possível revogar acesso individual
- ✅ Mais seguro

---

## Monitoramento de Uso

### Ver Custos (Azure Portal)

1. Acesse: https://portal.azure.com
2. Vá para **Cost Management**
3. Veja gastos por serviço
4. Monitore para não ultrapassar free tier/$100 créditos

### Alertas de Custo (Recomendado)

1. Azure Portal → Cost Management → Budgets
2. Create Budget
3. Configure:
   - Amount: $5 ou $10
   - Alert threshold: 80%
   - Email notification
4. Você receberá email se custo se aproximar do limite

---

## Troubleshooting para Equipe

### "Cannot connect to server"

**Causa**: Seu IP não está no firewall

**Solução**:
1. Verifique seu IP: https://whatismyipaddress.com
2. Peça para admin adicionar seu IP
3. Ou adicione você mesmo (Método 2 acima)

### "Login failed for user"

**Causa**: Username ou senha incorretos

**Solução**:
1. Confirme username: `adminceub` (sem espaços)
2. Confirme senha correta
3. Se esqueceu senha: peça para admin resetar

### "Timeout expired"

**Causa**: Conexão lenta ou database pausado

**Solução**:
1. Aguarde 30-60 segundos (database serverless desperta)
2. Tente novamente
3. Verifique sua internet

### "IP address does not have access"

**Causa**: IP mudou ou não foi adicionado

**Solução**:
1. Verifique IP atual: https://whatismyipaddress.com
2. Se mudou: adicione novo IP ao firewall
3. Cada vez que mudar de rede, IP pode mudar

---

## Compartilhamento de Arquivos

### Compartilhar Relatórios Power BI

**Método 1: OneDrive/Google Drive**
1. Salve arquivo .pbix
2. Faça upload para OneDrive/Google Drive
3. Compartilhe link com equipe
4. ⚠️ Todos precisam ter credenciais do banco para refresh

**Método 2: Power BI Service** (Requer Pro - $10/mês)
1. Publique relatório: Home → Publish
2. Compartilhe workspace com equipe
3. Refresh automático configurável

**Método 3: Git/GitHub** (Para versionamento)
1. Crie repositório privado
2. Commit arquivo .pbix
3. ⚠️ NUNCA comite credenciais no código!

---

## Segurança - Boas Práticas

### Para Todos os Membros

✅ **Faça:**
- Use senhas fortes
- Não compartilhe credenciais em grupos públicos
- Adicione apenas seu IP ao firewall
- Desconecte quando não estiver usando
- Reporte problemas de acesso ao admin

❌ **Não Faça:**
- Compartilhar senha em WhatsApp/email
- Adicionar IP 0.0.0.0/0 (libera para mundo inteiro)
- Modificar dados sem autorização
- Usar credenciais para outros projetos

### Para o Administrador

✅ **Faça:**
- Crie usuários read-only individuais
- Monitore custos semanalmente
- Configure alertas de custo
- Faça backups regulares (Azure faz automático)
- Revise lista de IPs permitidos mensalmente
- Remova IPs não utilizados

❌ **Não Faça:**
- Compartilhar senha admin publicamente
- Liberar todos os IPs (0.0.0.0/0)
- Ignorar alertas de custo
- Dar permissões write sem necessidade

---

## Contatos

### Administrador do Banco

**Nome**: [PREENCHER]
**Email**: [PREENCHER]
**WhatsApp**: [PREENCHER]

### Suporte Técnico

- **Azure Support**: https://portal.azure.com → Support
- **Documentação**: https://learn.microsoft.com/azure/azure-sql/
- **Comunidade**: Stack Overflow (tag: azure-sql-database)

---

## Checklist de Onboarding

Use este checklist para cada novo membro:

- [ ] Recebeu credenciais de acesso (privadamente)
- [ ] Descobriu seu IP público
- [ ] IP foi adicionado ao firewall do Azure
- [ ] Testou conexão via Power BI Desktop ou Azure Data Studio
- [ ] Consegue ver as 3 tabelas (DimMonth, DimCategoria, FactRetailMonthly)
- [ ] Entendeu regras de uso (read-only)
- [ ] Salvou credenciais em local seguro
- [ ] Sabe contatar admin em caso de problemas

---

**Criado em**: 2024-11-10
**Versão**: 1.0
**Projeto**: Sales Analytics - Power BI - CEUB
