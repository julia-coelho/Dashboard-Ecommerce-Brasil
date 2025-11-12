# Guia Completo: Configurar Azure SQL Database para Projeto Power BI

## Pré-requisitos
- ✅ Email institucional CEUB (@ceub.edu.br)
- ✅ Navegador web (Chrome, Safari, Firefox)
- ✅ Conexão com internet

---

## Parte 1: Criar Conta Azure for Students

### Passo 1: Acessar Azure for Students

1. Acesse: https://azure.microsoft.com/pt-br/free/students/
2. Clique em **"Ativar agora"** ou **"Começar gratuitamente"**

### Passo 2: Fazer Login

1. Use sua conta Microsoft:
   - Se já tem: faça login
   - Se não tem: crie uma conta com seu email pessoal ou CEUB
2. **IMPORTANTE**: Mesmo criando com email pessoal, você vai verificar como estudante com email CEUB

### Passo 3: Verificar Como Estudante

1. Após login, será pedido para verificar status de estudante
2. Escolha método de verificação:
   - **Opção 1 (Recomendada)**: Email institucional
     - Digite seu email @ceub.edu.br
     - Verifique o email de confirmação
     - Clique no link de verificação

   - **Opção 2**: Documento de estudante
     - Faça upload de declaração de matrícula ou carteirinha

3. Aguarde aprovação (geralmente instantânea)

### Passo 4: Ativar Azure for Students

1. Após aprovação, você receberá:
   - ✅ **$100 USD em créditos** (válido por 12 meses)
   - ✅ **Serviços gratuitos permanentes** (incluindo Azure SQL Database free tier)
   - ✅ **Sem necessidade de cartão de crédito**

2. Complete o cadastro com suas informações

---

## Parte 2: Criar Azure SQL Database

### Passo 1: Acessar Azure Portal

1. Acesse: https://portal.azure.com
2. Faça login com a conta que criou
3. Você verá o painel do Azure Portal

### Passo 2: Criar Resource Group (Grupo de Recursos)

1. No menu lateral, clique em **"Resource groups"** (Grupos de recursos)
2. Clique em **"+ Create"** (Criar)
3. Preencha:
   - **Subscription**: Azure for Students
   - **Resource group name**: `ceub-analytics-2024`
   - **Region**: `East US` - região permitida no Azure for Students
4. Clique em **"Review + create"** → **"Create"**

### Passo 3: Criar SQL Database

1. No menu superior, clique na barra de pesquisa e digite: **"SQL Database"**
2. Clique em **"SQL databases"** nos resultados
3. Clique em **"+ Create"** (Criar)

### Passo 4: Configurar SQL Database - Basics (Básico)

**Project Details:**
- **Subscription**: Azure for Students
- **Resource group**: `ceub-analytics-2024` (selecione o que criou)

**Database Details:**
- **Database name**: `sales_analytics_db`

**Server:** Clique em **"Create new"**
- **Server name**: `ceub-sales-server` (tem que ser único globalmente)
  - Se já existir, tente: `ceub-powerbi-2024`, `ceub-sales-db`, etc.
- **Location**: `East US`
- **Authentication method**: **"Use SQL authentication"**
  - **Server admin login**: `adminceub` (ou outro nome)
  - **Password**: Crie senha forte (min. 8 caracteres, maiúsculas, minúsculas, números, símbolos)
    - Exemplo: `Ceub@2024#PowerBI`
  - **⚠️ IMPORTANTE**: Anote essas credenciais! Você vai precisar delas sempre.
- Clique **"OK"**

**Workload environment:**
- Selecione: **"Development"** (mais barato)

### Passo 5: Configurar Compute + Storage (FREE TIER!)

1. Clique em **"Configure database"**
2. Na página de configuração:
   - Clique em **"Looking for basic, standard, premium?"**
   - Selecione a aba **"Basic"** (5 DTUs, 2GB) - MAIS BARATO
   - OU
   - Mantenha serverless e ajuste:
     - **Service tier**: General Purpose - Serverless
     - **Compute Hardware**: Standard-series (Gen5)
     - **Min vCores**: 0.5
     - **Max vCores**: 1
     - **Data max size**: 32 GB
     - **Auto-pause delay**: 1 hour

3. **Para FREE TIER verdadeiro**: Use Basic (mais barato) ou ajuste para menor configuração
4. Clique **"Apply"**

### Passo 6: Networking (Rede)

1. Vá para aba **"Networking"**
2. **Connectivity method**: Selecione **"Public endpoint"**
3. **Firewall rules**:
   - ✅ Marque: **"Allow Azure services and resources to access this server"**
   - ✅ Marque: **"Add current client IP address"**
4. Clique **"Next"**

### Passo 7: Security (Segurança)

1. Deixe configurações padrão
2. **Enable Microsoft Defender for SQL**: Selecione **"Not now"** (economiza créditos)
3. Clique **"Next"**

### Passo 8: Additional Settings (Configurações Adicionais)

1. **Use existing data**: Selecione **"None"**
2. **Database collation**: Deixe padrão (`SQL_Latin1_General_CP1_CI_AS`)
3. Clique **"Next"**

### Passo 9: Review + Create (Revisar e Criar)

1. Revise todas as configurações
2. **Verifique o custo estimado**: Deve ser ~$5/mês (Basic) ou dentro do free tier
3. Clique **"Create"**
4. **Aguarde 3-5 minutos** para criação

---

## Parte 3: Configurar Firewall para Equipe

### Passo 1: Acessar Configurações do Servidor

1. Após criação, vá para **"SQL databases"**
2. Clique no database: `sales_analytics_db`
3. Na página do database, clique em **"Set server firewall"** (topo da página)

### Passo 2: Adicionar IPs da Equipe

**Opção A: Cada membro adiciona seu próprio IP**

1. Compartilhe este link com a equipe: https://portal.azure.com
2. Cada membro:
   - Faz login com credenciais compartilhadas (ou cria user read-only)
   - Vai para SQL Server → Networking
   - Clica em **"Add client IP"**
   - Salva

**Opção B: Você adiciona manualmente**

1. Peça para cada membro acessar: https://whatismyipaddress.com
2. Eles te enviam o IP público deles
3. No firewall, clique **"+ Add client IP"** para cada um:
   - **Name**: `nome-do-membro`
   - **Start IP**: IP do membro
   - **End IP**: Mesmo IP
4. Clique **"Save"**

**Opção C: Liberar todos os IPs (NÃO RECOMENDADO - menos seguro)**

1. Adicione regra:
   - **Name**: `allow-all`
   - **Start IP**: `0.0.0.0`
   - **End IP**: `255.255.255.255`
2. ⚠️ Use apenas temporariamente ou para testes

### Passo 3: Salvar Configurações

1. Clique **"Save"** no topo
2. Aguarde confirmação

---

## Parte 4: Obter Connection String (String de Conexão)

### Passo 1: Copiar Connection String

1. Volte para o database: `sales_analytics_db`
2. No menu lateral, clique em **"Connection strings"**
3. Copie a string **"ADO.NET"**:

```
Server=tcp:ceub-sales-server.database.windows.net,1433;Initial Catalog=sales_analytics_db;Persist Security Info=False;User ID=adminceub;Password={your_password};MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;
```

4. Substitua `{your_password}` pela senha real que você criou
5. **Salve essa string** em local seguro

### Passo 2: Informações para Python/Power BI

Anote essas informações:

```
SERVER: ceub-sales-server.database.windows.net
DATABASE: sales_analytics_db
USERNAME: adminceub
PASSWORD: [sua senha]
PORT: 1433
```

---

## Parte 5: Testar Conexão (Opcional)

### Opção A: Via Azure Portal Query Editor

1. No database, clique em **"Query editor"** no menu lateral
2. Faça login com:
   - **Login**: `adminceub`
   - **Password**: [sua senha]
3. Se conectar com sucesso, você verá o editor SQL
4. Teste executando:
```sql
SELECT @@VERSION;
```

### Opção B: Via Azure Data Studio (Recomendado para Mac)

1. Baixe Azure Data Studio: https://aka.ms/azuredatastudio-macos
2. Instale o .dmg
3. Abra Azure Data Studio
4. Clique em **"New Connection"**
5. Preencha:
   - **Connection type**: Microsoft SQL Server
   - **Server**: `ceub-sales-server.database.windows.net`
   - **Authentication type**: SQL Login
   - **User name**: `adminceub`
   - **Password**: [sua senha]
   - **Database**: `sales_analytics_db`
   - **Encrypt**: True
6. Clique **"Connect"**

---

## Parte 6: Próximos Passos

✅ Azure SQL Database criado
✅ Firewall configurado
✅ Connection string obtida

**Agora você pode:**

1. Executar o script Python `02_import_data_to_azure.py` para importar os CSVs
2. Conectar o Power BI Desktop ao banco
3. Compartilhar acesso com equipe

---

## Troubleshooting (Solução de Problemas)

### Erro: "Cannot connect to server"
- ✅ Verifique se seu IP está no firewall
- ✅ Verifique usuário e senha
- ✅ Confirme que o servidor está rodando (Azure Portal)

### Erro: "Login failed for user"
- ✅ Confirme username: `adminceub`
- ✅ Confirme senha correta
- ✅ Verifique se não há espaços extras

### Erro: "Your client IP address does not have access"
- ✅ Adicione seu IP ao firewall (Passo da Parte 3)
- ✅ Ou marque "Allow Azure services"

### Database pausou (serverless)
- ✅ Normal - primeiro acesso após inatividade pode demorar 30s
- ✅ Configure auto-pause delay para mais tempo se necessário

---

## Custos Esperados

- **Basic tier**: ~R$ 25/mês (~$5/mês)
- **Serverless (0.5-1 vCore)**: ~R$ 50/mês (~$10/mês) quando ativo
- **Com Azure for Students**: Coberto pelos $100 de crédito

**Para manter 100% gratuito**: Use Basic tier e monitore uso mensal

---

## Segurança - Boas Práticas

✅ **Nunca compartilhe senha admin publicamente**
✅ **Use IP whitelisting** (não libere 0.0.0.0/0)
✅ **Crie usuários read-only** para membros da equipe
✅ **Habilite SSL/encryption** (padrão no Azure)
✅ **Monitore custos** no Azure Portal → Cost Management

---

## Contatos Úteis

- **Suporte Azure for Students**: https://aka.ms/azureforeducation
- **Documentação Azure SQL**: https://learn.microsoft.com/azure/azure-sql/
- **Comunidade CEUB**: [adicionar se houver]

---

**Criado em**: 2024-11-10
**Versão**: 1.0
**Projeto**: Sales Analytics - Power BI - CEUB
