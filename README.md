# Database Setup - Neon PostgreSQL

Scripts para importar dados para o banco Neon PostgreSQL.

## Arquivos

- **`import_to_neon.py`** - Script principal de importação de dados
- **`requirements.txt`** - Dependências Python necessárias

## Uso Rápido

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Executar importação
python import_to_neon.py
```

## Credenciais Neon

As credenciais já estão configuradas no script:
- **Host:** ep-patient-dawn-aciwozz1-pooler.sa-east-1.aws.neon.tech
- **Database:** neondb
- **User:** neondb_owner
- **Port:** 5432

## O que o script faz

1. Conecta ao Neon PostgreSQL
2. Remove tabelas existentes (se houver)
3. Cria 4 tabelas:
   - `dimmonth` (444 registros)
   - `dimcategoria` (8 registros)
   - `factretailmonthly` (307,644 registros)
   - `factinventorysnapshotmonthly` (6,785 registros)
4. Importa dados dos CSVs
5. Cria índices e relacionamentos
6. Verifica a importação

## Tabelas Criadas

### Dimensões
- **dimmonth**: Dimensão temporal (1992-2028)
- **dimcategoria**: Categorias de produtos

### Fatos
- **factretailmonthly**: Vendas mensais por item
- **factinventorysnapshotmonthly**: Snapshot de inventário (18/09/2025)

## Próximos Passos

Após a importação, use as credenciais acima para conectar o Power BI ao Neon.
