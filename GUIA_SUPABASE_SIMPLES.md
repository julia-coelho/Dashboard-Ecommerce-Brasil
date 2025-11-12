# 🚀 Guia Supabase - Configuração Rápida (5 minutos)

## Por que Supabase é Melhor para Este Projeto

✅ **Setup em 5 minutos** (vs 1 hora no Azure)
✅ **100% gratuito** - 500MB de storage (27MB é suficiente)
✅ **Não precisa cartão de crédito**
✅ **Sem problemas de região/firewall**
✅ **Interface web super simples**
✅ **PostgreSQL** (compatível com Power BI)

---

## Parte 1: Criar Conta e Projeto (2 minutos)

### Passo 1: Criar Conta

1. Acesse: https://supabase.com
2. Clique em **"Start your project"**
3. Escolha uma opção de login:
   - **GitHub** (mais rápido - recomendado)
   - **Email** (criar conta nova)

4. Se escolher GitHub:
   - Clique em "Sign in with GitHub"
   - Autorize Supabase
   - Pronto!

5. Se escolher Email:
   - Digite seu email
   - Crie uma senha
   - Verifique o email de confirmação

### Passo 2: Criar Projeto

1. Você verá a tela "Create a new project"
2. Preencha:
   - **Organization**: Crie uma nova ou use existente
     - Nome: `CEUB` ou `PowerBI-Project`

   - **Project Name**: `sales-analytics`

   - **Database Password**: Crie senha forte
     - Exemplo: `Ceub@2024#Sales`
     - ⚠️ **ANOTE ESSA SENHA!** Você vai precisar dela

   - **Region**: Selecione `South America (São Paulo)` ⭐
     - Ou `East US` (se São Paulo não aparecer)

   - **Pricing Plan**: FREE ✅

3. Clique em **"Create new project"**

4. Aguarde **1-2 minutos** enquanto o projeto é criado
   - Você verá uma barra de progresso
   - Pode tomar um café ☕

---

## Parte 2: Obter Credenciais de Conexão (1 minuto)

### Passo 1: Acessar Configurações

1. No painel do projeto, clique em **⚙️ Settings** (menu lateral)
2. Clique em **Database** (submenu)

### Passo 2: Copiar Informações de Conexão

Role para baixo até a seção **"Connection info"**

Você verá:

```
Host: db.[seu-projeto].supabase.co
Database name: postgres
Port: 5432
User: postgres
Password: [clique em "reveal" para ver]
```

**⚠️ ANOTE ESSAS INFORMAÇÕES:**

```
HOST: db.xxxxxxxxxxxxx.supabase.co
PORT: 5432
DATABASE: postgres
USER: postgres
PASSWORD: [sua senha criada no Passo 2]
```

### Passo 3: Copiar Connection String (Opcional)

Mais abaixo, você verá **"Connection string"**

Copie a **URI**:
```
postgresql://postgres:[YOUR-PASSWORD]@db.xxxxxxxxxxxxx.supabase.co:5432/postgres
```

Substitua `[YOUR-PASSWORD]` pela senha real

---

## Parte 3: Importar Dados via Interface Web (2 minutos)

### Opção A: Interface Gráfica (Mais Simples)

1. No menu lateral, clique em **🗂️ Table Editor**

2. Clique em **"Create a new table"**

#### Criar Tabela DimMonth:

**Configurações:**
- **Name**: `DimMonth`
- **Enable Row Level Security (RLS)**: Desmarque (por enquanto)

**Columns** (clique em "Add column" para cada):
1. `YearMonthKey` - Type: `varchar` - Primary Key ✅
2. `MonthDate` - Type: `date`
3. `Year` - Type: `int4`
4. `MonthNumber` - Type: `int4`
5. `MonthNamePT` - Type: `varchar`
6. `YearMonth` - Type: `varchar`
7. `DaysInMonth` - Type: `int4`
8. `StartOfMonth` - Type: `date`
9. `EndOfMonth` - Type: `date`

Clique em **"Save"**

**Importar CSV:**
1. Com a tabela `DimMonth` aberta, clique em **"Insert" → "Import data from CSV"**
2. Selecione o arquivo: `data/dims/dim_month_1992_2028.csv`
3. Clique em **"Import data"**
4. Aguarde importação

#### Criar Tabela DimCategoria:

Repita o processo:

**Columns:**
1. `CategoriaID` - Type: `int4` - Primary Key ✅
2. `ItemType` - Type: `varchar`
3. `Categoria` - Type: `varchar`

Importe: `data/dims/DimCategoria.csv`

#### Criar Tabela FactRetailMonthly:

**Columns:**
1. `YearMonthKey` - Type: `varchar`
2. `ItemCode` - Type: `varchar`
3. `ItemDescription` - Type: `text`
4. `ItemType` - Type: `varchar`
5. `RetailSales` - Type: `numeric`
6. `RetailTransfers` - Type: `numeric`
7. `WarehouseSales` - Type: `numeric`
8. `TotalSales` - Type: `numeric`

Importe: `data/processed/FactRetailMonthly.csv`

⚠️ **Nota**: FactRetailMonthly pode demorar um pouco (é 20MB)

---

### Opção B: SQL Editor (Mais Rápido para Programadores)

1. No menu lateral, clique em **🔨 SQL Editor**

2. Clique em **"New query"**

3. Cole este SQL:

```sql
-- Criar tabela DimMonth
CREATE TABLE DimMonth (
    YearMonthKey VARCHAR(6) PRIMARY KEY,
    MonthDate DATE,
    Year INTEGER,
    MonthNumber INTEGER,
    MonthNamePT VARCHAR(20),
    YearMonth VARCHAR(7),
    DaysInMonth INTEGER,
    StartOfMonth DATE,
    EndOfMonth DATE
);

-- Criar tabela DimCategoria
CREATE TABLE DimCategoria (
    CategoriaID INTEGER PRIMARY KEY,
    ItemType VARCHAR(50),
    Categoria VARCHAR(100)
);

-- Criar tabela FactRetailMonthly
CREATE TABLE FactRetailMonthly (
    YearMonthKey VARCHAR(6),
    ItemCode VARCHAR(50),
    ItemDescription TEXT,
    ItemType VARCHAR(50),
    RetailSales NUMERIC(18,2),
    RetailTransfers NUMERIC(18,2),
    WarehouseSales NUMERIC(18,2),
    TotalSales NUMERIC(18,2)
);

-- Criar índices para performance
CREATE INDEX idx_fact_yearmonth ON FactRetailMonthly(YearMonthKey);
CREATE INDEX idx_fact_itemcode ON FactRetailMonthly(ItemCode);
CREATE INDEX idx_fact_itemtype ON FactRetailMonthly(ItemType);

-- Criar foreign keys
ALTER TABLE FactRetailMonthly
ADD CONSTRAINT fk_fact_dimmonth
FOREIGN KEY (YearMonthKey) REFERENCES DimMonth(YearMonthKey);

ALTER TABLE FactRetailMonthly
ADD CONSTRAINT fk_fact_dimcategoria
FOREIGN KEY (ItemType) REFERENCES DimCategoria(ItemType);
```

4. Clique em **"Run"**

5. **Depois use o script Python** (próxima seção) para importar os CSVs

---

## Parte 4: Importar Dados via Python (Recomendado)

Vou criar um script Python para você executar no Mac.

**Vantagens:**
- ✅ Importa tudo automaticamente
- ✅ Trata dados (remove NaN)
- ✅ Mais rápido para arquivos grandes

Veja o arquivo: `import_to_supabase.py`

---

## Parte 5: Conectar Power BI ao Supabase

### Passo 1: Abrir Power BI Desktop

1. Abra Power BI Desktop (Windows)
2. Clique em **"Get data"**
3. Pesquise: **"PostgreSQL database"**
4. Selecione e clique em **"Connect"**

### Passo 2: Configurar Conexão

**PostgreSQL database:**
```
Server: db.[seu-projeto].supabase.co:5432
Database: postgres
```

**Data Connectivity mode:**
- Selecione: ✅ **Import** (recomendado)

Clique em **"OK"**

### Passo 3: Autenticação

1. Selecione aba **"Database"**
2. Preencha:
   - **User name**: `postgres`
   - **Password**: [senha que você criou]
3. Clique em **"Connect"**

### Passo 4: Selecionar Tabelas

1. Marque as tabelas:
   - ✅ `DimMonth`
   - ✅ `DimCategoria`
   - ✅ `FactRetailMonthly`

2. Clique em **"Load"**

3. Aguarde importação

### Passo 5: Criar Relacionamentos

(Mesmo processo que no guia Azure)

1. Vá para **Model View**
2. Arraste `YearMonthKey`: DimMonth → FactRetailMonthly
3. Arraste `ItemType`: DimCategoria → FactRetailMonthly

Pronto! 🎉

---

## Parte 6: Compartilhar com Equipe

### Opção 1: Credenciais Compartilhadas (Simples)

Compartilhe com a equipe (por mensagem privada):

```
HOST: db.[seu-projeto].supabase.co
PORT: 5432
DATABASE: postgres
USER: postgres
PASSWORD: [sua senha]
```

**Sem firewall!** Todos podem conectar de qualquer lugar.

### Opção 2: Criar Usuários Individuais (Mais Seguro)

No SQL Editor:

```sql
-- Criar usuário read-only
CREATE USER membro1 WITH PASSWORD 'senha123';
GRANT CONNECT ON DATABASE postgres TO membro1;
GRANT USAGE ON SCHEMA public TO membro1;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO membro1;
```

---

## Vantagens vs Azure

| Recurso | Supabase | Azure SQL |
|---------|----------|-----------|
| **Setup** | 5 min ⚡ | 60 min 🐌 |
| **Custo** | Grátis ✅ | Grátis* (com limitações) |
| **Cartão** | Não precisa ✅ | Às vezes precisa ⚠️ |
| **Firewall** | Não tem ✅ | Precisa configurar IP ⚠️ |
| **Região** | Sem restrição ✅ | Limitado no Students ⚠️ |
| **Interface** | Moderna ✅ | Complexa ⚠️ |

---

## Troubleshooting

### "Cannot connect to server"

✅ Verifique:
1. Host está correto (`db.xxxx.supabase.co`)
2. Porta é `5432`
3. Senha está correta
4. Internet funcionando

### "Authentication failed"

✅ Soluções:
1. Confirme username: `postgres`
2. Confirme senha criada no setup
3. Resete senha: Settings → Database → Reset database password

### "Table not found"

✅ Soluções:
1. Verifique se tabelas foram criadas (Table Editor)
2. Execute SQL para criar tabelas
3. Importe CSVs novamente

---

## Próximos Passos

1. ✅ Supabase criado
2. ✅ Tabelas criadas
3. ✅ Dados importados
4. ✅ Power BI conectado
5. ✅ Equipe tem acesso

**Agora:**
- Crie visualizações no Power BI
- Implemente medidas DAX
- Compartilhe .pbix com equipe

---

## Links Úteis

- **Supabase Docs**: https://supabase.com/docs
- **PostgreSQL + Power BI**: https://learn.microsoft.com/power-bi/connect-data/desktop-connect-to-postgresql
- **Supabase SQL Editor**: Direto no dashboard

---

**Criado em**: 2024-11-10
**Versão**: 1.0
**Projeto**: Sales Analytics - Power BI - CEUB
