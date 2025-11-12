# ⚡ Início Rápido - Azure SQL Database + Power BI

Guia resumido para começar rapidamente. Para detalhes, veja os guias completos.

---

## 👤 Para o ADMINISTRADOR (Você - Primeira vez)

### Passo 1: Criar Azure SQL Database (30-60 min)

1. ✅ Acesse: https://azure.microsoft.com/pt-br/free/students/
2. ✅ Cadastre-se com email CEUB (@ceub.edu.br)
3. ✅ Ganhe $100 de créditos gratuitos
4. ✅ Siga o guia: [01_GUIA_AZURE_SETUP.md](01_GUIA_AZURE_SETUP.md)

**Anote essas informações:**
```
SERVER: seu-servidor.database.windows.net
DATABASE: sales_analytics_db
USERNAME: adminceub
PASSWORD: [sua senha forte]
```

### Passo 2: Instalar Dependências Python

```bash
# No terminal Mac:
pip install pandas pyodbc

# Instalar driver ODBC:
brew install msodbcsql18
# OU
brew install freetds
```

### Passo 3: Importar Dados (5-10 min)

```bash
# 1. Edite o arquivo:
nano 02_import_data_to_azure.py

# 2. Substitua as credenciais (linhas 17-20):
SERVER = 'seu-servidor.database.windows.net'
DATABASE = 'sales_analytics_db'
USERNAME = 'adminceub'
PASSWORD = 'SuaSenhaAqui'

# 3. Execute:
python 02_import_data_to_azure.py
```

**Resultado esperado:**
```
✓ Conectado ao Azure SQL Database: sales_analytics_db
✓ Tabela DimMonth criada
✓ Tabela DimCategoria criada
✓ Tabela FactRetailMonthly criada
✓ 444 registros importados (DimMonth)
✓ 5 registros importados (DimCategoria)
✓ [N] registros importados (FactRetailMonthly)
🎉 PROCESSO CONCLUÍDO COM SUCESSO!
```

### Passo 4: Compartilhar com Equipe

1. ✅ Preencha as credenciais no arquivo [04_GUIA_ACESSO_EQUIPE.md](04_GUIA_ACESSO_EQUIPE.md)
2. ✅ Compartilhe os guias 03 e 04 com a equipe (por mensagem privada)
3. ✅ Adicione o IP de cada membro no Azure Portal:
   - Portal Azure → SQL Server → Networking → Add client IP

---

## 👥 Para os MEMBROS DA EQUIPE

### Passo 1: Receber Credenciais

Você deve receber do administrador:
```
SERVER: [servidor].database.windows.net
DATABASE: sales_analytics_db
USERNAME: adminceub
PASSWORD: [senha]
```

### Passo 2: Adicionar Seu IP ao Firewall

```bash
# 1. Descubra seu IP:
# Acesse: https://whatismyipaddress.com

# 2. Envie seu IP para o admin adicionar
# OU
# 3. Adicione você mesmo no Azure Portal (se tiver acesso)
```

### Passo 3: Instalar Power BI Desktop

⚠️ **Mac**: Power BI Desktop é só Windows. Opções:
- Usar Parallels/VMWare (rodar Windows no Mac)
- Usar computador Windows (lab, biblioteca)
- Boot Camp (instalar Windows nativo)

**Windows**:
1. Download: https://powerbi.microsoft.com/desktop/
2. Instale o arquivo .exe
3. Abra Power BI Desktop

### Passo 4: Conectar ao Banco

```
Power BI Desktop
→ Get Data
→ Azure SQL Database
→ Preencher:
   Server: [servidor].database.windows.net
   Database: sales_analytics_db
→ Database authentication:
   Username: adminceub
   Password: [senha]
→ Selecionar tabelas:
   ✅ DimMonth
   ✅ DimCategoria
   ✅ FactRetailMonthly
→ Load
```

### Passo 5: Criar Relacionamentos

```
Model View (ícone lateral)
→ Arrastar YearMonthKey: DimMonth → FactRetailMonthly
→ Arrastar ItemType: DimCategoria → FactRetailMonthly
```

### Passo 6: Criar Medidas DAX

```dax
Retail Sales (M) = SUM(FactRetailMonthly[RetailSales])
```

```dax
Avg Retail Sales Prev 3M =
VAR MaxMes = MAX(DimMonth[MonthDate])
RETURN
IF(
    CALCULATE(
        DISTINCTCOUNT(DimMonth[YearMonthKey]),
        DATESINPERIOD(DimMonth[MonthDate], EOMONTH(MaxMes,-1), -3, MONTH)
    ) < 3,
    BLANK(),
    AVERAGEX(
        DATESINPERIOD(DimMonth[MonthDate], EOMONTH(MaxMes,-1), -3, MONTH),
        [Retail Sales (M)]
    )
)
```

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

---

## 🎯 Fluxo de Trabalho

```
┌─────────────────────────────────────────────┐
│  ADMIN: Cria Azure SQL Database (1x)       │
│  • Azure for Students                       │
│  • Cria database                            │
│  • Importa CSVs (Python script)             │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│  ADMIN: Compartilha Credenciais             │
│  • Envia guias 03 e 04 para equipe          │
│  • Adiciona IPs ao firewall                 │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│  EQUIPE: Conecta Power BI                   │
│  • Cada um conecta ao mesmo banco           │
│  • Cria visualizações                       │
│  • Compartilha .pbix via OneDrive           │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│  TODOS: Colaboram                           │
│  • Mesmos dados (banco centralizado)        │
│  • Diferentes visualizações (criatividade)  │
│  • Compartilham insights                    │
└─────────────────────────────────────────────┘
```

---

## 🔧 Troubleshooting Rápido

| Problema | Solução Rápida |
|----------|----------------|
| "Cannot connect" | Adicione seu IP no firewall |
| "Login failed" | Verifique username/senha |
| "Timeout" | Aguarde 30s (database desperta) |
| "Driver not found" | `brew install msodbcsql18` |
| "Power BI não abre (Mac)" | Use Windows (VM ou lab) |

---

## 📚 Guias Completos

1. **[01_GUIA_AZURE_SETUP.md](01_GUIA_AZURE_SETUP.md)** - Setup Azure (Admin)
2. **[02_import_data_to_azure.py](02_import_data_to_azure.py)** - Script importação (Admin)
3. **[03_GUIA_POWERBI_CONEXAO.md](03_GUIA_POWERBI_CONEXAO.md)** - Conectar Power BI (Todos)
4. **[04_GUIA_ACESSO_EQUIPE.md](04_GUIA_ACESSO_EQUIPE.md)** - Acesso equipe (Todos)
5. **[README.md](README.md)** - Visão geral completa

---

## ✅ Checklist Mínimo

### Admin:
- [ ] Azure SQL Database criado
- [ ] Script Python executado com sucesso
- [ ] 3 tabelas criadas (DimMonth, DimCategoria, FactRetailMonthly)
- [ ] Credenciais compartilhadas com equipe

### Equipe:
- [ ] Credenciais recebidas
- [ ] IP adicionado ao firewall
- [ ] Power BI conectado ao banco
- [ ] 3 tabelas visíveis no Power BI
- [ ] Relacionamentos criados
- [ ] 3 medidas DAX implementadas

---

## 🎓 Dicas

💡 **Para economizar créditos Azure:**
- Use Basic tier (~$5/mês)
- Configure auto-pause (serverless)
- Monitore custos semanalmente

💡 **Para trabalhar em equipe:**
- Todos conectam ao mesmo banco
- Cada um cria seu .pbix
- Compartilham via OneDrive/Google Drive

💡 **Para apresentação:**
- Salve prints do modelo de dados
- Documente medidas DAX criadas
- Capture screenshots das visualizações

---

**Tempo total estimado**: 2-3 horas (setup completo)

**Custo**: $0 (com Azure for Students)

**Dificuldade**: ⭐⭐⭐☆☆ (Intermediária)

---

Boa sorte com o projeto! 🚀
