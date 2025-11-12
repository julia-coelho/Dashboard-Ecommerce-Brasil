# ⚡ Início Rápido - Supabase (5 minutos)

## 🎯 Passo a Passo Simplificado

### 1️⃣ Criar Conta Supabase (2 min)

```
1. Acesse: https://supabase.com
2. Clique "Start your project"
3. Sign in with GitHub (mais rápido)
4. Pronto!
```

### 2️⃣ Criar Projeto (1 min)

```
1. Click "New project"
2. Preencha:
   - Organization: CEUB
   - Project name: sales-analytics
   - Database password: Ceub@2024#Sales (ANOTE!)
   - Region: South America (São Paulo)
   - Plan: FREE
3. Click "Create new project"
4. Aguarde 1-2 minutos
```

### 3️⃣ Copiar Credenciais (1 min)

```
1. Settings → Database
2. Copie:

   HOST: db.xxxxxxxxxxxxx.supabase.co
   PORT: 5432
   DATABASE: postgres
   USER: postgres
   PASSWORD: [sua senha do passo 2]
```

### 4️⃣ Importar Dados via Python (1 min)

```bash
# No terminal Mac:
cd "/Volumes/Crucial X6/Projeto_integrador/database_setup"

# Instalar dependências:
pip install pandas psycopg2-binary

# Editar script:
nano import_to_supabase.py

# Substituir nas linhas 17-21:
HOST = 'db.xxxxxxxxxxxxx.supabase.co'  # Seu host
PASSWORD = 'Ceub@2024#Sales'  # Sua senha

# Executar:
python import_to_supabase.py
```

**Resultado esperado:**
```
✓ Conectado ao Supabase: postgres
✓ Tabela DimMonth criada
✓ Tabela DimCategoria criada
✓ Tabela FactRetailMonthly criada
✓ 444 registros importados (DimMonth)
✓ 5 registros importados (DimCategoria)
✓ [N] registros importados (FactRetailMonthly)
🎉 PROCESSO CONCLUÍDO COM SUCESSO!
```

---

## 🔌 Conectar Power BI

### Power BI Desktop (Windows)

```
1. Get Data → PostgreSQL database
2. Preencha:
   Server: db.xxxxxxxxxxxxx.supabase.co:5432
   Database: postgres
3. Authentication: Database
   Username: postgres
   Password: [sua senha]
4. Selecione tabelas:
   ✅ DimMonth
   ✅ DimCategoria
   ✅ FactRetailMonthly
5. Load
```

---

## 👥 Compartilhar com Equipe

**Envie por mensagem privada:**

```
🔐 CREDENCIAIS SUPABASE

Server: db.xxxxxxxxxxxxx.supabase.co:5432
Database: postgres
Username: postgres
Password: Ceub@2024#Sales

Para conectar no Power BI:
1. Get Data → PostgreSQL database
2. Cole o server acima
3. Use username e password
```

**Sem firewall! Todo mundo conecta de qualquer lugar!** ✅

---

## ✅ Checklist

- [ ] Conta Supabase criada
- [ ] Projeto criado
- [ ] Credenciais anotadas
- [ ] Script Python editado (HOST e PASSWORD)
- [ ] Dependências instaladas (`pip install pandas psycopg2-binary`)
- [ ] Script executado (`python import_to_supabase.py`)
- [ ] 3 tabelas criadas e populadas
- [ ] Testado conexão Power BI

---

## 🆘 Problemas?

### "Cannot connect"
→ Verifique HOST e PASSWORD no script

### "pip command not found"
→ Use: `pip3 install pandas psycopg2-binary`

### "Module not found"
→ Execute: `pip install pandas psycopg2-binary`

### "File not found"
→ Verifique se está na pasta `database_setup`

---

## 📚 Guia Completo

Para mais detalhes, veja:
- [GUIA_SUPABASE_SIMPLES.md](GUIA_SUPABASE_SIMPLES.md) - Guia detalhado
- [import_to_supabase.py](import_to_supabase.py) - Script Python

---

**Tempo total**: 5 minutos ⚡
**Custo**: $0 (100% gratuito)
**Dificuldade**: ⭐☆☆☆☆ (Muito fácil)

Boa sorte! 🚀
