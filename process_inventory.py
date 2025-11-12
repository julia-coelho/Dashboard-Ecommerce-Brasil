"""
ETL para criar FactInventorySnapshotMonthly
Projeto: Sales Analytics - Power BI - CEUB

Processa ABS_Store_Inventory_and_Sale_Items_20250918.csv
e cria tabela fato de inventário mensal
"""

import pandas as pd
from pathlib import Path

# Caminhos
BASE_DIR = Path(__file__).parent
INPUT_FILE = BASE_DIR / "csv's" / "ABS_Store_Inventory_and_Sale_Items_20250918.csv"
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "FactInventorySnapshotMonthly.csv"

print("=" * 80)
print("ETL - FactInventorySnapshotMonthly")
print("=" * 80)

# Carregar dados
print(f"\n📁 Carregando {INPUT_FILE.name}...")
df = pd.read_csv(INPUT_FILE)
print(f"  ✓ {len(df):,} registros carregados")

# Snapshot date
snapshot_date = "2025-09-18"
print(f"\n📅 Snapshot Date: {snapshot_date}")

# Criar colunas temporais
df['SnapshotDate'] = snapshot_date
df['Year'] = 2025
df['Month'] = 9
df['YearMonthKey'] = '202509'

# Limpar Price (remover $ e converter para float)
print(f"\n💰 Limpando coluna Price (removendo '$')...")
df['Price'] = df['Price'].astype(str).str.replace('$', '', regex=False).str.replace(',', '', regex=False)
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

# Calcular StockValue
print(f"💰 Calculando StockValue = Total Inventory × Price...")
df['StockValue'] = df['Total Inventory'] * df['Price']

# Tratar valores nulos
original_count = len(df)
df = df.dropna(subset=['Code', 'Price', 'Total Inventory'])
removed = original_count - len(df)
if removed > 0:
    print(f"  ⚠️  {removed} registros removidos (Price ou Total Inventory nulos)")

# Renomear Code para ItemCode (padronizar)
df = df.rename(columns={'Code': 'ItemCode'})

# Selecionar colunas finais
fact_inventory = df[[
    'YearMonthKey',
    'ItemCode',
    'Description',
    'Category',
    'Size',
    'Total Inventory',
    'Price',
    'StockValue',
    'SnapshotDate'
]].copy()

# Renomear para manter consistência
fact_inventory = fact_inventory.rename(columns={
    'Description': 'ItemDescription',
    'Category': 'ItemCategory',
    'Size': 'ItemSize',
    'Total Inventory': 'TotalInventory'
})

# Salvar
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
fact_inventory.to_csv(OUTPUT_FILE, index=False)

print(f"\n✅ FactInventorySnapshotMonthly criado!")
print(f"  📁 Local: {OUTPUT_FILE}")
print(f"  📊 Registros: {len(fact_inventory):,}")
print(f"  💵 StockValue Total: ${fact_inventory['StockValue'].sum():,.2f}")

# Estatísticas
print(f"\n📈 Estatísticas:")
print(f"  - Items únicos: {fact_inventory['ItemCode'].nunique():,}")
print(f"  - StockValue médio por item: ${fact_inventory['StockValue'].mean():,.2f}")
print(f"  - Price médio: ${fact_inventory['Price'].mean():,.2f}")
print(f"  - Total Inventory médio: {fact_inventory['TotalInventory'].mean():,.2f}")

print("\n" + "=" * 80)
print("✅ ETL CONCLUÍDO")
print("=" * 80)
