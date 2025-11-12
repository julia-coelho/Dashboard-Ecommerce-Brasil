"""
Script para Importar Dados para Neon (PostgreSQL)
Projeto: Sales Analytics - Power BI - CEUB

Este script:
1. Conecta no Neon PostgreSQL
2. Cria as tabelas necessárias
3. Importa os CSVs processados
4. Aplica transformações (remove NaN, etc.)
"""

import pandas as pd
import psycopg2
from psycopg2 import sql
import sys
from pathlib import Path

# ============================================================================
# CONFIGURAÇÕES - EDITE AQUI COM SUAS CREDENCIAIS DO SUPABASE
# ============================================================================

# Credenciais do Neon
# Você encontra essas informações em: Neon Console → Connection String
HOST = 'ep-patient-dawn-aciwozz1-pooler.sa-east-1.aws.neon.tech'
PORT = 5432
DATABASE = 'neondb'
USER = 'neondb_owner'
PASSWORD = 'npg_LiH0fcSJjy6b'

# Caminhos dos arquivos CSV
BASE_DIR = Path(__file__).parent.parent
CSV_PATHS = {
    'fact_retail_monthly': BASE_DIR / 'data' / 'processed' / 'FactRetailMonthly.csv',
    'fact_inventory_snapshot': BASE_DIR / 'data' / 'processed' / 'FactInventorySnapshotMonthly.csv',
    'dim_month': BASE_DIR / 'data' / 'dims' / 'dim_month_1992_2028.csv',
    'dim_categoria': BASE_DIR / 'data' / 'dims' / 'DimCategoria.csv'
}

# ============================================================================
# FUNÇÕES
# ============================================================================

def create_connection():
    """
    Cria conexão com Supabase PostgreSQL
    """
    try:
        conn = psycopg2.connect(
            host=HOST,
            port=PORT,
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            sslmode='require'  # Supabase requer SSL
        )
        print(f"✓ Conectado ao Supabase: {DATABASE}")
        return conn

    except psycopg2.Error as e:
        print(f"❌ Erro ao conectar: {e}")
        print("\n🔍 Verifique:")
        print("   1. Credenciais corretas (HOST, DATABASE, USER, PASSWORD)")
        print("   2. Projeto Supabase está ativo")
        print("   3. Internet funcionando")
        sys.exit(1)


def create_tables(conn):
    """
    Cria as tabelas no banco de dados
    """
    cursor = conn.cursor()

    print("\n📊 Criando tabelas...")

    # Drop tables se existirem (para re-execução)
    drop_tables = """
    DROP TABLE IF EXISTS FactRetailMonthly CASCADE;
    DROP TABLE IF EXISTS FactInventorySnapshotMonthly CASCADE;
    DROP TABLE IF EXISTS DimCategoria CASCADE;
    DROP TABLE IF EXISTS DimMonth CASCADE;
    """
    cursor.execute(drop_tables)
    conn.commit()

    # Tabela DimMonth (Dimensão Temporal)
    create_dim_month = """
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
    """
    cursor.execute(create_dim_month)
    print("  ✓ Tabela DimMonth criada")

    # Tabela DimCategoria (Dimensão de Categorias)
    create_dim_categoria = """
    CREATE TABLE DimCategoria (
        CategoriaID INTEGER PRIMARY KEY,
        ItemType VARCHAR(50) UNIQUE,
        Categoria VARCHAR(100)
    );
    """
    cursor.execute(create_dim_categoria)
    print("  ✓ Tabela DimCategoria criada")

    # Tabela FactRetailMonthly (Fato - Vendas Mensais)
    create_fact_retail = """
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
    """
    cursor.execute(create_fact_retail)
    print("  ✓ Tabela FactRetailMonthly criada")

    # Tabela FactInventorySnapshotMonthly (Fato - Inventário)
    create_fact_inventory = """
    CREATE TABLE FactInventorySnapshotMonthly (
        YearMonthKey VARCHAR(6),
        ItemCode VARCHAR(50),
        ItemDescription TEXT,
        ItemCategory VARCHAR(100),
        ItemSize VARCHAR(50),
        TotalInventory NUMERIC(18,2),
        Price NUMERIC(18,2),
        StockValue NUMERIC(18,2),
        SnapshotDate DATE
    );
    """
    cursor.execute(create_fact_inventory)
    print("  ✓ Tabela FactInventorySnapshotMonthly criada")

    # Criar índices para melhor performance
    create_indexes = """
    CREATE INDEX idx_fact_retail_yearmonth ON FactRetailMonthly(YearMonthKey);
    CREATE INDEX idx_fact_retail_itemcode ON FactRetailMonthly(ItemCode);
    CREATE INDEX idx_fact_retail_itemtype ON FactRetailMonthly(ItemType);
    CREATE INDEX idx_fact_inventory_yearmonth ON FactInventorySnapshotMonthly(YearMonthKey);
    CREATE INDEX idx_fact_inventory_itemcode ON FactInventorySnapshotMonthly(ItemCode);
    """
    cursor.execute(create_indexes)
    print("  ✓ Índices criados")

    # Criar foreign keys
    create_fks = """
    ALTER TABLE FactRetailMonthly
    ADD CONSTRAINT fk_fact_retail_dimmonth
    FOREIGN KEY (YearMonthKey) REFERENCES DimMonth(YearMonthKey);

    ALTER TABLE FactRetailMonthly
    ADD CONSTRAINT fk_fact_retail_dimcategoria
    FOREIGN KEY (ItemType) REFERENCES DimCategoria(ItemType);

    ALTER TABLE FactInventorySnapshotMonthly
    ADD CONSTRAINT fk_fact_inventory_dimmonth
    FOREIGN KEY (YearMonthKey) REFERENCES DimMonth(YearMonthKey);
    """
    cursor.execute(create_fks)
    print("  ✓ Foreign keys criadas")

    conn.commit()
    print("✓ Todas as tabelas criadas com sucesso!\n")


def import_csv_data(conn):
    """
    Importa dados dos CSVs para as tabelas
    """
    cursor = conn.cursor()

    print("📥 Importando dados dos CSVs...\n")

    # 1. Importar DimCategoria
    print("  → Importando DimCategoria...")
    df_categoria = pd.read_csv(CSV_PATHS['dim_categoria'])

    for _, row in df_categoria.iterrows():
        cursor.execute("""
            INSERT INTO DimCategoria (CategoriaID, ItemType, Categoria)
            VALUES (%s, %s, %s)
        """, (int(row['CategoriaID']), row['ItemType'], row['Categoria']))

    conn.commit()
    print(f"    ✓ {len(df_categoria)} registros importados\n")

    # 2. Importar DimMonth
    print("  → Importando DimMonth...")
    df_month = pd.read_csv(CSV_PATHS['dim_month'])

    # Converter datas para formato correto
    df_month['MonthDate'] = pd.to_datetime(df_month['MonthDate'], format='%d/%m/%y', errors='coerce')
    df_month['StartOfMonth'] = pd.to_datetime(df_month['StartOfMonth'], format='%d/%m/%y', errors='coerce')
    df_month['EndOfMonth'] = pd.to_datetime(df_month['EndOfMonth'], format='%d/%m/%y', errors='coerce')

    for _, row in df_month.iterrows():
        cursor.execute("""
            INSERT INTO DimMonth (
                YearMonthKey, MonthDate, Year, MonthNumber,
                MonthNamePT, YearMonth, DaysInMonth, StartOfMonth, EndOfMonth
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
            (
                str(row['YearMonthKey']),
                row['MonthDate'],
                int(row['Year']),
                int(row['MonthNumber']),
                row['MonthNamePT'],
                row['YearMonth'],
                int(row['DaysInMonth']),
                row['StartOfMonth'],
                row['EndOfMonth']
            )
        )

    conn.commit()
    print(f"    ✓ {len(df_month)} registros importados\n")

    # 3. Importar FactRetailMonthly
    print("  → Importando FactRetailMonthly...")
    df_fact = pd.read_csv(CSV_PATHS['fact_retail_monthly'])

    # Tratamento de dados: remover NaN
    print("    → Tratando dados (removendo NaN)...")
    original_count = len(df_fact)

    # Remover linhas com NaN em colunas críticas
    df_fact = df_fact.dropna(subset=['YearMonthKey', 'ItemCode'])

    # Preencher NaN em colunas numéricas com 0
    numeric_cols = ['RetailSales', 'RetailTransfers', 'WarehouseSales', 'TotalSales']
    df_fact[numeric_cols] = df_fact[numeric_cols].fillna(0)

    # Preencher NaN em colunas texto com string vazia
    df_fact['ItemDescription'] = df_fact['ItemDescription'].fillna('')
    df_fact['ItemType'] = df_fact['ItemType'].fillna('UNKNOWN')

    removed_count = original_count - len(df_fact)
    if removed_count > 0:
        print(f"    ⚠️  {removed_count} linhas removidas por falta de dados críticos")

    # Inserir dados em lotes (mais rápido)
    batch_size = 1000
    total_rows = len(df_fact)

    for i in range(0, total_rows, batch_size):
        batch = df_fact.iloc[i:i+batch_size]

        # Usar COPY com CSV adequadamente escapado
        from io import StringIO
        buffer = StringIO()
        batch[['YearMonthKey', 'ItemCode', 'ItemDescription', 'ItemType',
               'RetailSales', 'RetailTransfers', 'WarehouseSales', 'TotalSales']].to_csv(
            buffer, index=False, header=False, quoting=1  # QUOTE_ALL para escapar vírgulas
        )
        buffer.seek(0)

        cursor.copy_expert(
            """COPY factretailmonthly (yearmonthkey, itemcode, itemdescription, itemtype,
                    retailsales, retailtransfers, warehousesales, totalsales)
               FROM STDIN WITH CSV""",
            buffer
        )

        conn.commit()
        progress = min(i + batch_size, total_rows)
        print(f"    → Progresso: {progress}/{total_rows} registros ({progress*100//total_rows}%)")

    print(f"    ✓ {len(df_fact)} registros importados\n")

    # 4. Importar FactInventorySnapshotMonthly
    print("  → Importando FactInventorySnapshotMonthly...")
    df_inventory = pd.read_csv(CSV_PATHS['fact_inventory_snapshot'])

    # Tratamento de dados
    print("    → Tratando dados (removendo NaN)...")
    original_count_inv = len(df_inventory)

    # Remover linhas com NaN em colunas críticas
    df_inventory = df_inventory.dropna(subset=['YearMonthKey', 'ItemCode', 'Price', 'TotalInventory'])

    # Preencher NaN em colunas numéricas com 0
    df_inventory['StockValue'] = df_inventory['StockValue'].fillna(0)

    # Preencher NaN em colunas texto
    df_inventory['ItemDescription'] = df_inventory['ItemDescription'].fillna('')
    df_inventory['ItemCategory'] = df_inventory['ItemCategory'].fillna('UNKNOWN')
    df_inventory['ItemSize'] = df_inventory['ItemSize'].fillna('')

    removed_count_inv = original_count_inv - len(df_inventory)
    if removed_count_inv > 0:
        print(f"    ⚠️  {removed_count_inv} linhas removidas por falta de dados críticos")

    # Inserir dados em lotes
    batch_size = 1000
    total_rows_inv = len(df_inventory)

    for i in range(0, total_rows_inv, batch_size):
        batch = df_inventory.iloc[i:i+batch_size]

        # Usar COPY com CSV adequadamente escapado
        from io import StringIO
        buffer = StringIO()
        batch[['YearMonthKey', 'ItemCode', 'ItemDescription', 'ItemCategory', 'ItemSize',
               'TotalInventory', 'Price', 'StockValue', 'SnapshotDate']].to_csv(
            buffer, index=False, header=False, quoting=1
        )
        buffer.seek(0)

        cursor.copy_expert(
            """COPY factinventorysnapshotmonthly (yearmonthkey, itemcode, itemdescription, itemcategory, itemsize,
                    totalinventory, price, stockvalue, snapshotdate)
               FROM STDIN WITH CSV""",
            buffer
        )

        conn.commit()
        progress = min(i + batch_size, total_rows_inv)
        print(f"    → Progresso: {progress}/{total_rows_inv} registros ({progress*100//total_rows_inv}%)")

    print(f"    ✓ {len(df_inventory)} registros importados\n")


def verify_import(conn):
    """
    Verifica se os dados foram importados corretamente
    """
    cursor = conn.cursor()

    print("🔍 Verificando importação...\n")

    # Contar registros em cada tabela
    tables = ['dimmonth', 'dimcategoria', 'factretailmonthly', 'factinventorysnapshotmonthly']

    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"  ✓ {table}: {count:,} registros")

    # Verificar relacionamentos
    print("\n🔗 Verificando relacionamentos...")

    # Chaves órfãs em FactRetailMonthly (YearMonthKey)
    cursor.execute("""
        SELECT COUNT(DISTINCT f.yearmonthkey)
        FROM factretailmonthly f
        LEFT JOIN dimmonth d ON f.yearmonthkey = d.yearmonthkey
        WHERE d.yearmonthkey IS NULL
    """)
    orphan_months = cursor.fetchone()[0]

    if orphan_months == 0:
        print("  ✓ Relacionamento FactRetailMonthly → DimMonth: OK")
    else:
        print(f"  ⚠️  {orphan_months} YearMonthKey órfãos encontrados")

    # Chaves órfãs em FactRetailMonthly (ItemType)
    cursor.execute("""
        SELECT COUNT(DISTINCT f.itemtype)
        FROM factretailmonthly f
        LEFT JOIN dimcategoria d ON f.itemtype = d.itemtype
        WHERE d.itemtype IS NULL
    """)
    orphan_types = cursor.fetchone()[0]

    if orphan_types == 0:
        print("  ✓ Relacionamento FactRetailMonthly → DimCategoria: OK")
    else:
        print(f"  ⚠️  {orphan_types} ItemType órfãos encontrados")

    print("\n✅ Importação concluída com sucesso!")


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 80)
    print("IMPORTAÇÃO DE DADOS PARA SUPABASE (PostgreSQL)")
    print("Projeto: Sales Analytics - Power BI - CEUB")
    print("=" * 80)
    print()

    # Verificar se arquivos existem
    print("📁 Verificando arquivos CSV...")
    for name, path in CSV_PATHS.items():
        if not path.exists():
            print(f"  ❌ Arquivo não encontrado: {path}")
            sys.exit(1)
        print(f"  ✓ {name}: {path.name}")
    print()

    # Conectar ao banco
    conn = create_connection()

    try:
        # Criar tabelas
        create_tables(conn)

        # Importar dados
        import_csv_data(conn)

        # Verificar importação
        verify_import(conn)

        print("\n" + "=" * 80)
        print("🎉 PROCESSO CONCLUÍDO COM SUCESSO!")
        print("=" * 80)
        print("\n📊 Próximos passos:")
        print("  1. Conecte o Power BI Desktop ao Supabase")
        print("  2. Use as credenciais:")
        print(f"     Host: {HOST}")
        print(f"     Database: {DATABASE}")
        print(f"     User: {USER}")
        print("  3. Crie os relacionamentos no modelo")
        print("  4. Implemente as medidas DAX")
        print()

    except Exception as e:
        print(f"\n❌ Erro durante execução: {e}")
        import traceback
        traceback.print_exc()

    finally:
        conn.close()
        print("✓ Conexão fechada")


if __name__ == "__main__":
    main()
