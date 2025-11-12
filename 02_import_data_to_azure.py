"""
Script para Importar Dados para Azure SQL Database
Projeto: Sales Analytics - Power BI - CEUB

Este script:
1. Conecta no Azure SQL Database
2. Cria as tabelas necessárias
3. Importa os CSVs processados
4. Aplica transformações (remove NaN, etc.)
"""

import pandas as pd
import pyodbc
import sys
from pathlib import Path

# ============================================================================
# CONFIGURAÇÕES - EDITE AQUI COM SUAS CREDENCIAIS
# ============================================================================

# Credenciais do Azure SQL Database
SERVER = 'ceub-sales-server.database.windows.net'  # Substitua pelo seu server
DATABASE = 'sales_analytics_db'  # Substitua pelo seu database
USERNAME = 'adminceub'  # Substitua pelo seu username
PASSWORD = 'SUA_SENHA_AQUI'  # ⚠️ SUBSTITUA PELA SUA SENHA!

# Caminhos dos arquivos CSV
BASE_DIR = Path(__file__).parent.parent
CSV_PATHS = {
    'fact_retail_monthly': BASE_DIR / 'data' / 'processed' / 'FactRetailMonthly.csv',
    'dim_month': BASE_DIR / 'data' / 'dims' / 'dim_month_1992_2028.csv',
    'dim_categoria': BASE_DIR / 'data' / 'dims' / 'DimCategoria.csv'
}

# ============================================================================
# FUNÇÕES
# ============================================================================

def create_connection():
    """
    Cria conexão com Azure SQL Database
    """
    try:
        # Driver ODBC - tenta diferentes versões
        drivers = [
            'ODBC Driver 18 for SQL Server',
            'ODBC Driver 17 for SQL Server',
            'ODBC Driver 13 for SQL Server',
            'FreeTDS'  # Alternativa para Mac
        ]

        driver = None
        for d in drivers:
            try:
                test_conn = f'DRIVER={{{d}}};SERVER={SERVER}'
                pyodbc.connect(test_conn, timeout=1)
                driver = d
                break
            except:
                continue

        if not driver:
            print("❌ Nenhum driver ODBC encontrado!")
            print("\n📥 Instale o driver:")
            print("   Mac: brew install msodbcsql18")
            print("   ou: brew install freetds")
            sys.exit(1)

        print(f"✓ Driver encontrado: {driver}")

        # String de conexão
        conn_str = (
            f'DRIVER={{{driver}}};'
            f'SERVER={SERVER};'
            f'DATABASE={DATABASE};'
            f'UID={USERNAME};'
            f'PWD={PASSWORD};'
            f'Encrypt=yes;'
            f'TrustServerCertificate=no;'
        )

        conn = pyodbc.connect(conn_str, timeout=30)
        print(f"✓ Conectado ao Azure SQL Database: {DATABASE}")
        return conn

    except pyodbc.Error as e:
        print(f"❌ Erro ao conectar: {e}")
        print("\n🔍 Verifique:")
        print("   1. Credenciais corretas (SERVER, DATABASE, USERNAME, PASSWORD)")
        print("   2. Firewall do Azure permite seu IP")
        print("   3. Database está rodando no Azure Portal")
        sys.exit(1)


def create_tables(conn):
    """
    Cria as tabelas no banco de dados
    """
    cursor = conn.cursor()

    print("\n📊 Criando tabelas...")

    # Drop tables se existirem (para re-execução)
    drop_tables = """
    IF OBJECT_ID('dbo.FactRetailMonthly', 'U') IS NOT NULL DROP TABLE dbo.FactRetailMonthly;
    IF OBJECT_ID('dbo.DimCategoria', 'U') IS NOT NULL DROP TABLE dbo.DimCategoria;
    IF OBJECT_ID('dbo.DimMonth', 'U') IS NOT NULL DROP TABLE dbo.DimMonth;
    """
    cursor.execute(drop_tables)
    conn.commit()

    # Tabela DimMonth (Dimensão Temporal)
    create_dim_month = """
    CREATE TABLE DimMonth (
        YearMonthKey VARCHAR(6) PRIMARY KEY,
        MonthDate DATE,
        Year INT,
        MonthNumber INT,
        MonthNamePT VARCHAR(20),
        YearMonth VARCHAR(7),
        DaysInMonth INT,
        StartOfMonth DATE,
        EndOfMonth DATE
    );
    """
    cursor.execute(create_dim_month)
    print("  ✓ Tabela DimMonth criada")

    # Tabela DimCategoria (Dimensão de Categorias)
    create_dim_categoria = """
    CREATE TABLE DimCategoria (
        CategoriaID INT PRIMARY KEY,
        ItemType VARCHAR(50),
        Categoria VARCHAR(100)
    );
    """
    cursor.execute(create_dim_categoria)
    print("  ✓ Tabela DimCategoria criada")

    # Tabela FactRetailMonthly (Fato - Vendas Mensais)
    create_fact_retail = """
    CREATE TABLE FactRetailMonthly (
        YearMonthKey VARCHAR(6) NOT NULL,
        ItemCode VARCHAR(50) NOT NULL,
        ItemDescription NVARCHAR(500),
        ItemType VARCHAR(50),
        RetailSales DECIMAL(18,2),
        RetailTransfers DECIMAL(18,2),
        WarehouseSales DECIMAL(18,2),
        TotalSales DECIMAL(18,2),
        CONSTRAINT FK_FactRetail_DimMonth FOREIGN KEY (YearMonthKey) REFERENCES DimMonth(YearMonthKey),
        CONSTRAINT FK_FactRetail_DimCategoria FOREIGN KEY (ItemType) REFERENCES DimCategoria(ItemType)
    );
    """
    cursor.execute(create_fact_retail)
    print("  ✓ Tabela FactRetailMonthly criada")

    # Criar índices para melhor performance
    create_indexes = """
    CREATE INDEX IX_FactRetail_YearMonthKey ON FactRetailMonthly(YearMonthKey);
    CREATE INDEX IX_FactRetail_ItemCode ON FactRetailMonthly(ItemCode);
    CREATE INDEX IX_FactRetail_ItemType ON FactRetailMonthly(ItemType);
    """
    cursor.execute(create_indexes)
    print("  ✓ Índices criados")

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
            VALUES (?, ?, ?)
        """, row['CategoriaID'], row['ItemType'], row['Categoria'])

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
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            str(row['YearMonthKey']),
            row['MonthDate'],
            row['Year'],
            row['MonthNumber'],
            row['MonthNamePT'],
            row['YearMonth'],
            row['DaysInMonth'],
            row['StartOfMonth'],
            row['EndOfMonth']
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

        for _, row in batch.iterrows():
            cursor.execute("""
                INSERT INTO FactRetailMonthly (
                    YearMonthKey, ItemCode, ItemDescription, ItemType,
                    RetailSales, RetailTransfers, WarehouseSales, TotalSales
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                row['YearMonthKey'],
                row['ItemCode'],
                row['ItemDescription'],
                row['ItemType'],
                float(row['RetailSales']),
                float(row['RetailTransfers']),
                float(row['WarehouseSales']),
                float(row['TotalSales'])
            )

        conn.commit()
        progress = min(i + batch_size, total_rows)
        print(f"    → Progresso: {progress}/{total_rows} registros ({progress*100//total_rows}%)")

    print(f"    ✓ {len(df_fact)} registros importados\n")


def verify_import(conn):
    """
    Verifica se os dados foram importados corretamente
    """
    cursor = conn.cursor()

    print("🔍 Verificando importação...\n")

    # Contar registros em cada tabela
    tables = ['DimMonth', 'DimCategoria', 'FactRetailMonthly']

    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"  ✓ {table}: {count:,} registros")

    # Verificar relacionamentos
    print("\n🔗 Verificando relacionamentos...")

    # Chaves órfãs em FactRetailMonthly (YearMonthKey)
    cursor.execute("""
        SELECT COUNT(DISTINCT f.YearMonthKey)
        FROM FactRetailMonthly f
        LEFT JOIN DimMonth d ON f.YearMonthKey = d.YearMonthKey
        WHERE d.YearMonthKey IS NULL
    """)
    orphan_months = cursor.fetchone()[0]

    if orphan_months == 0:
        print("  ✓ Relacionamento FactRetailMonthly → DimMonth: OK")
    else:
        print(f"  ⚠️  {orphan_months} YearMonthKey órfãos encontrados")

    # Chaves órfãs em FactRetailMonthly (ItemType)
    cursor.execute("""
        SELECT COUNT(DISTINCT f.ItemType)
        FROM FactRetailMonthly f
        LEFT JOIN DimCategoria d ON f.ItemType = d.ItemType
        WHERE d.ItemType IS NULL
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
    print("IMPORTAÇÃO DE DADOS PARA AZURE SQL DATABASE")
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
        print("  1. Conecte o Power BI Desktop ao Azure SQL Database")
        print("  2. Use as credenciais:")
        print(f"     Server: {SERVER}")
        print(f"     Database: {DATABASE}")
        print(f"     Username: {USERNAME}")
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
