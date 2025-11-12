"""
Criar mapeamento de chaves entre Inventory e Sales
Projeto: Sales Analytics - Power BI - CEUB
"""

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent
OUTPUT_FILE = BASE_DIR / "data" / "metadata" / "KeyMap_Inventory_Sales.csv"

print("=" * 80)
print("CRIAÇÃO DE KEY MAP - Inventory ⇄ Sales")
print("=" * 80)

# Carregar dados
inventory = pd.read_csv(BASE_DIR / "csv's" / "ABS_Store_Inventory_and_Sale_Items_20250918.csv")
sales = pd.read_csv(BASE_DIR / "csv's" / "Warehouse_and_Retail_Sales.csv")

print(f"\n📊 Dados carregados:")
print(f"  Inventory: {len(inventory):,} registros, {inventory['Code'].nunique():,} códigos únicos")
print(f"  Sales: {len(sales):,} registros, {sales['ITEM CODE'].nunique():,} códigos únicos")

# Match direto de códigos
inv_codes = inventory['Code'].astype(str).str.strip()
sales_codes = sales['ITEM CODE'].astype(str).str.strip()

inv_set = set(inv_codes.unique())
sales_set = set(sales_codes.unique())
matched_codes = inv_set.intersection(sales_set)

print(f"\n🔗 Match direto:")
print(f"  Códigos com match: {len(matched_codes):,} ({len(matched_codes)/len(inv_set)*100:.1f}%)")

# Criar KeyMap
keymap = pd.DataFrame({
    'InventoryCode': list(matched_codes),
    'SalesCode': list(matched_codes),
    'MatchType': 'Direct'
})

# Adicionar informações adicionais
keymap = keymap.merge(
    inventory[['Code', 'Category', 'Description']].drop_duplicates('Code'),
    left_on='InventoryCode',
    right_on='Code',
    how='left'
).drop('Code', axis=1)

keymap = keymap.rename(columns={
    'Category': 'InventoryCategory',
    'Description': 'InventoryDescription'
})

# Adicionar info do Sales
sales_info = sales[['ITEM CODE', 'ITEM TYPE', 'ITEM DESCRIPTION']].drop_duplicates('ITEM CODE')
keymap = keymap.merge(
    sales_info,
    left_on='SalesCode',
    right_on='ITEM CODE',
    how='left'
).drop('ITEM CODE', axis=1)

keymap = keymap.rename(columns={
    'ITEM TYPE': 'SalesItemType',
    'ITEM DESCRIPTION': 'SalesDescription'
})

# Salvar
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
keymap.to_csv(OUTPUT_FILE, index=False)

print(f"\n✅ KeyMap criado!")
print(f"  📁 Local: {OUTPUT_FILE}")
print(f"  📊 Registros: {len(keymap):,}")
print(f"  🔗 Match rate: {len(matched_codes)/len(inv_set)*100:.1f}%")

# Estatísticas por categoria
print(f"\n📈 Match por Inventory Category (top 10):")
category_stats = keymap.groupby('InventoryCategory').size().sort_values(ascending=False).head(10)
for cat, count in category_stats.items():
    print(f"  {cat}: {count}")

print("\n" + "=" * 80)
print("✅ KEY MAP CONCLUÍDO")
print("=" * 80)
print("\n⚠️  LIMITAÇÃO: 56.2% de match - itens sem match não terão DoS calculado")
print("💡 SOLUÇÃO: No Power BI, a KPI retornará BLANK para itens sem match")
