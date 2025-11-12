# Database Setup - Sales Analytics Project

Guias completos para configurar e usar o Azure SQL Database para o projeto Power BI.

---

## 📚 Índice de Documentos

### Para o Administrador (Primeira Configuração)

1. **[01_GUIA_AZURE_SETUP.md](01_GUIA_AZURE_SETUP.md)**
   - Como criar conta Azure for Students
   - Configurar Azure SQL Database (free tier)
   - Configurar firewall
   - Obter connection string
   - ⏱️ Tempo: 30-60 minutos

2. **[02_import_data_to_azure.py](02_import_data_to_azure.py)**
   - Script Python para importar CSVs
   - Cria tabelas automaticamente
   - Trata dados (remove NaN)
   - Verifica integridade
   - ⏱️ Tempo: 5-10 minutos (execução)

### Para Todos os Membros da Equipe

3. **[03_GUIA_POWERBI_CONEXAO.md](03_GUIA_POWERBI_CONEXAO.md)**
   - Como instalar Power BI Desktop (Windows)
   - Conectar ao Azure SQL Database
   - Criar relacionamentos no modelo
   - Implementar medidas DAX
   - Criar visualizações
   - ⏱️ Tempo: 1-2 horas

4. **[04_GUIA_ACESSO_EQUIPE.md](04_GUIA_ACESSO_EQUIPE.md)**
   - Credenciais de acesso
   - Como adicionar IP ao firewall
   - Regras de uso
   - Troubleshooting
   - Contatos

---

## 🚀 Início Rápido

### Passo 1: Administrador Configura Azure (Fazer UMA vez)

```bash
# 1. Siga o guia 01_GUIA_AZURE_SETUP.md
# 2. Anote as credenciais criadas
# 3. Execute o script Python:

cd "/Volumes/Crucial X6/Projeto_integrador/database_setup"
python 02_import_data_to_azure.py
```

**⚠️ ANTES de executar o script:**
- Edite `02_import_data_to_azure.py`
- Substitua as credenciais (SERVER, DATABASE, USERNAME, PASSWORD)
- Instale dependências: `pip install pandas pyodbc`

### Passo 2: Compartilhar com Equipe

1. Preencha as credenciais no arquivo `04_GUIA_ACESSO_EQUIPE.md`
2. Compartilhe os guias 03 e 04 com a equipe
3. Cada membro adiciona seu IP ao firewall
4. Cada membro conecta o Power BI

### Passo 3: Trabalhar no Power BI

1. Cada membro segue o `03_GUIA_POWERBI_CONEXAO.md`
2. Conecta ao banco compartilhado
3. Cria visualizações e dashboards
4. Compartilha arquivos .pbix via OneDrive/Google Drive

---

## 📋 Checklist de Implementação

### Fase 1: Setup Inicial (Admin)
- [ ] Criar conta Azure for Students
- [ ] Criar Azure SQL Database
- [ ] Configurar firewall (adicionar seu IP)
- [ ] Testar conexão (Azure Data Studio ou Query Editor)
- [ ] Editar script Python com credenciais
- [ ] Executar script de importação
- [ ] Verificar que 3 tabelas foram criadas
- [ ] Preencher credenciais no guia 04

### Fase 2: Onboarding da Equipe
- [ ] Compartilhar guias 03 e 04 com equipe
- [ ] Cada membro recebe credenciais (privado)
- [ ] Cada membro adiciona seu IP ao firewall
- [ ] Cada membro testa conexão

### Fase 3: Power BI (Todos)
- [ ] Instalar Power BI Desktop
- [ ] Conectar ao Azure SQL
- [ ] Importar 3 tabelas
- [ ] Criar relacionamentos
- [ ] Implementar medidas DAX
- [ ] Criar visualizações
- [ ] Testar KPIs

### Fase 4: Colaboração
- [ ] Compartilhar .pbix via OneDrive/Drive
- [ ] (Opcional) Publicar no Power BI Service
- [ ] Documentar descobertas
- [ ] Preparar apresentação

---

## 🛠️ Pré-requisitos

### Para Administrador

**Software:**
- Python 3.8+ (já instalado no Mac)
- pip (gerenciador de pacotes Python)

**Pacotes Python:**
```bash
pip install pandas pyodbc
```

**Driver ODBC (Mac):**
```bash
# Opção 1: Microsoft ODBC Driver
brew install msodbcsql18

# Opção 2: FreeTDS (alternativa)
brew install freetds
```

**Azure:**
- Email institucional CEUB (@ceub.edu.br)
- Conta Azure for Students (gratuita)

### Para Membros da Equipe

**Software:**
- Power BI Desktop (Windows)
  - OU Parallels/VM para rodar Windows no Mac
  - OU usar computador Windows (lab, biblioteca)

**Opcional (para explorar dados):**
- Azure Data Studio (gratuito, Mac/Windows)
- DBeaver (gratuito, Mac/Windows)

---

## 📊 Estrutura de Dados

### Tabelas

**DimMonth** (444 registros)
- Dimensão temporal: 1992-2028
- Chave primária: YearMonthKey

**DimCategoria** (5 registros)
- Mapeamento ItemType → Categoria
- Chave primária: CategoriaID
- Chave estrangeira: ItemType

**FactRetailMonthly** (~variável registros)
- Fato: vendas mensais por item
- Chaves estrangeiras: YearMonthKey, ItemType

### Relacionamentos

```
DimMonth (1) ────► FactRetailMonthly (*)
                          ▲
                          │
DimCategoria (1) ─────────┘
```

### Medidas DAX

1. **Retail Sales (M)**: `SUM(FactRetailMonthly[RetailSales])`
2. **Avg Retail Sales Prev 3M**: Média dos 3 meses anteriores
3. **Δ Vendas vs Média 3M %**: Variação % vs média 3M

---

## 💰 Custos

### Azure SQL Database

**Free Tier / Azure for Students:**
- ✅ $100 créditos (12 meses)
- ✅ Basic tier: ~R$ 25/mês (~$5/mês)
- ✅ Serverless: ~R$ 50/mês quando ativo
- ✅ 32GB storage (mais que suficiente para 27MB)

**Monitoramento:**
- Azure Portal → Cost Management
- Configure alertas em $5 ou $10
- Monitore semanalmente

### Power BI

**Power BI Desktop:**
- ✅ Gratuito (Windows)

**Power BI Service (Opcional):**
- Pro: $10/usuário/mês
- Premium Per User: $20/usuário/mês
- Não necessário para projeto acadêmico (use compartilhamento de .pbix)

---

## 🔐 Segurança

### Credenciais

- ⚠️ NUNCA compartilhe senha em grupos públicos
- ✅ Use mensagens privadas
- ✅ Considere criar usuários read-only individuais
- ✅ Guarde credenciais em gerenciador de senhas

### Firewall

- ✅ Adicione apenas IPs específicos
- ❌ NUNCA libere 0.0.0.0/0 (todo mundo)
- ✅ Remova IPs não utilizados regularmente
- ✅ Cada membro adiciona apenas seu IP

### Backup

- ✅ Azure faz backup automático (padrão)
- ✅ Configure retention period se necessário
- ✅ Dados podem ser restaurados em caso de problema

---

## 🐛 Troubleshooting Comum

### "Cannot connect to server"
→ Adicione seu IP ao firewall

### "Login failed"
→ Verifique username/password

### "Timeout expired"
→ Aguarde 30s (database serverless desperta)

### "Driver not found" (Python)
→ Instale: `brew install msodbcsql18` ou `brew install freetds`

### "Power BI não abre no Mac"
→ Power BI Desktop é só Windows - use VM ou computador Windows

---

## 📞 Suporte

### Documentação Oficial

- Azure SQL: https://learn.microsoft.com/azure/azure-sql/
- Power BI: https://learn.microsoft.com/power-bi/
- Azure for Students: https://aka.ms/azureforeducation

### Comunidade

- Stack Overflow: Tags `azure-sql-database`, `powerbi`
- Power BI Community: community.powerbi.com
- Reddit: r/PowerBI, r/Azure

### Contato do Projeto

- **Admin**: [Preencher nome/email]
- **Equipe**: [Preencher]

---

## 📝 Changelog

### v1.0 (2024-11-10)
- ✅ Guia Azure Setup criado
- ✅ Script Python de importação criado
- ✅ Guia Power BI conexão criado
- ✅ Guia acesso equipe criado
- ✅ README geral criado

---

## 📄 Licença

Projeto acadêmico - CEUB Brasília
Uso restrito à equipe do projeto

---

**Última atualização**: 2024-11-10
**Versão**: 1.0
**Projeto**: Sales Analytics - Power BI - CEUB
