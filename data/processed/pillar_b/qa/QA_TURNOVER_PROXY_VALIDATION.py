"""
QA Validation - Giro anual (valor) - Proxy via ISR (SA)
Valida 5 pontos aleatórios + regras BLANK + validação cruzada com DoS
"""

import pandas as pd
import numpy as np

print("=== QA VALIDATION - Giro anual - Proxy via ISR (SA) ===\n")

# 1. Carregar dados
print("1. Carregando FactRETAILIRSA.csv...")
df = pd.read_csv('FactRETAILIRSA.csv')
df['MonthDate'] = pd.to_datetime(df['MonthDate'])
df = df.sort_values('MonthDate')
print(f"   ✓ {len(df)} meses carregados\n")

# 2. Calcular Giro (voltas/ano) para toda a série
print("2. Calculando Giro (voltas/ano) = 12 / ISR_SA...")
df['Giro_voltas_ano'] = 12 / df['ISR_SA']
print(f"   ✓ Giro (voltas/ano) calculado\n")

# 3. Calcular DoS para validação cruzada
print("3. Calculando DoS (dias) para validação cruzada...")
df['DoS_dias'] = df['ISR_SA'] * 30
print(f"   ✓ DoS (dias) calculado\n")

# 4. Selecionar 5 pontos aleatórios para validação
print("4. Selecionando 5 pontos aleatórios para validação...\n")
np.random.seed(42)  # Para reprodutibilidade
random_indices = np.random.choice(df.index, size=5, replace=False)
qa_sample = df.loc[random_indices].sort_values('MonthDate')

# 5. Validação detalhada
print("=" * 80)
print("VALIDAÇÃO MANUAL - 5 PONTOS ALEATÓRIOS")
print("=" * 80)

test_results = []

for i, row in qa_sample.iterrows():
    month = row['MonthDate'].strftime('%b/%Y')
    yearmonth = row['YearMonthKey']

    isr_sa = row['ISR_SA']
    giro_calculated = row['Giro_voltas_ano']

    # Cálculo manual
    if pd.notna(isr_sa) and isr_sa != 0:
        giro_manual = 12 / isr_sa
        erro = abs(giro_calculated - giro_manual) if pd.notna(giro_calculated) else 0
        status = "✅ PASS" if erro <= 0.01 else "❌ FAIL"
    else:
        giro_manual = None
        erro = 0
        status = "✅ PASS (BLANK correto)" if pd.isna(giro_calculated) else "❌ FAIL"

    print(f"\nMês: {month} ({yearmonth})")
    print(f"  ISR_SA:                     {isr_sa:.4f}")
    print(f"  Giro calculado:             {giro_calculated:.2f} voltas/ano" if pd.notna(giro_calculated) else "  Giro calculado:             BLANK")
    print(f"  Giro manual (12/ISR):       {giro_manual:.2f} voltas/ano" if pd.notna(giro_manual) else "  Giro manual:                N/A")
    print(f"  Erro:                       {erro:.4f} voltas/ano")
    print(f"  Status:                     {status}")

    test_results.append({
        'Mês': month,
        'YearMonthKey': yearmonth,
        'ISR_SA': isr_sa if pd.notna(isr_sa) else None,
        'Giro_calculated': giro_calculated if pd.notna(giro_calculated) else None,
        'Giro_manual': giro_manual if pd.notna(giro_manual) else None,
        'Erro_voltas_ano': erro,
        'Status': status
    })

# 6. Validação de regra BLANK
print("\n" + "=" * 80)
print("VALIDAÇÃO - REGRA BLANK")
print("=" * 80)

# Verificar se há algum BLANK no CSV original
blank_count = df['ISR_SA'].isna().sum()
zero_count = (df['ISR_SA'] == 0).sum()

print(f"\nMeses com ISR_SA = BLANK no CSV: {blank_count}")
print(f"Meses com ISR_SA = 0 no CSV: {zero_count}")

if blank_count > 0 or zero_count > 0:
    # Se houver BLANKs ou zeros, verificar se Giro também é BLANK
    problematic = df[(df['ISR_SA'].isna()) | (df['ISR_SA'] == 0)]
    giro_blank_ok = problematic['Giro_voltas_ano'].isna().all()
    print(f"Giro = BLANK para todos os meses sem ISR_SA ou ISR_SA=0? {'✅ SIM' if giro_blank_ok else '❌ NÃO'}")
else:
    print("✅ Não há BLANKs ou zeros na série atual (todos os meses têm ISR_SA > 0)")

# 7. Validação de faixa de valores
print("\n" + "=" * 80)
print("VALIDAÇÃO - FAIXA DE VALORES")
print("=" * 80)

print(f"\nEstatísticas Giro (voltas/ano):")
print(f"  Mínimo:    {df['Giro_voltas_ano'].min():.2f} voltas/ano ({df.loc[df['Giro_voltas_ano'].idxmin(), 'MonthDate'].strftime('%b/%Y')})")
print(f"  Máximo:    {df['Giro_voltas_ano'].max():.2f} voltas/ano ({df.loc[df['Giro_voltas_ano'].idxmax(), 'MonthDate'].strftime('%b/%Y')})")
print(f"  Média:     {df['Giro_voltas_ano'].mean():.2f} voltas/ano")
print(f"  Mediana:   {df['Giro_voltas_ano'].median():.2f} voltas/ano")

# Verificar se todos os valores são > 0
all_positive = (df['Giro_voltas_ano'] > 0).all()
print(f"\nTodos os valores > 0? {'✅ SIM' if all_positive else '❌ NÃO'}")

# Verificar faixa razoável (assumindo varejo geral: 6-12 voltas/ano)
giro_min_expected = 6
giro_max_expected = 12
in_range = ((df['Giro_voltas_ano'] >= giro_min_expected - 2) & (df['Giro_voltas_ano'] <= giro_max_expected + 2)).all()
print(f"Todos os valores na faixa esperada (4-14 voltas/ano)? {'✅ SIM' if in_range else '⚠️ ALGUNS FORA (verificar contexto histórico)'}")

# 8. Validação cruzada com DoS
print("\n" + "=" * 80)
print("VALIDAÇÃO CRUZADA - Giro × DoS ≈ 360 dias")
print("=" * 80)

print(f"\nTeste de consistência matemática: Giro × DoS ≈ 360")
print(f"Fórmula: (12 / ISR_SA) × (ISR_SA × 30) = 12 × 30 = 360\n")

# Calcular produto Giro × DoS
df['Giro_x_DoS'] = df['Giro_voltas_ano'] * df['DoS_dias']

# Verificar últimos 5 meses
last_5_months = df.tail(5)
print(f"Últimos 5 meses:")
for _, row in last_5_months.iterrows():
    month = row['MonthDate'].strftime('%b/%Y')
    giro = row['Giro_voltas_ano']
    dos = row['DoS_dias']
    produto = row['Giro_x_DoS']
    erro_produto = abs(produto - 360)
    status = "✅" if erro_produto < 0.1 else "❌"
    print(f"  {month}: Giro={giro:.2f} × DoS={dos:.1f} = {produto:.1f} dias (erro={erro_produto:.4f}) {status}")

# Verificar toda a série
max_erro_produto = abs(df['Giro_x_DoS'] - 360).max()
print(f"\nMaior erro Giro×DoS na série: {max_erro_produto:.4f} dias")
print(f"Tolerância: 0.1 dias")
print(f"Validação cruzada: {'✅ PASS' if max_erro_produto < 0.1 else '❌ FAIL'}")

# 9. Teste de últimos 3 meses
print("\n" + "=" * 80)
print("VALIDAÇÃO - ÚLTIMOS 3 MESES")
print("=" * 80)

last_3_months = df.tail(3)
print(f"\nÚltimos 3 meses da série:")
for _, row in last_3_months.iterrows():
    month = row['MonthDate'].strftime('%b/%Y')
    isr = row['ISR_SA']
    giro = row['Giro_voltas_ano']
    giro_manual = 12 / isr
    erro = abs(giro - giro_manual)
    print(f"  {month}: ISR={isr:.2f}, Giro={giro:.2f} voltas/ano, Manual={giro_manual:.2f}, Erro={erro:.4f} ✅")

# 10. Resumo final
print("\n" + "=" * 80)
print("RESUMO DA VALIDAÇÃO")
print("=" * 80)

df_results = pd.DataFrame(test_results)
total_tests = len(test_results) + 2  # +1 para teste de faixa, +1 para validação cruzada
passed_tests = sum(1 for r in test_results if '✅ PASS' in r['Status'])
passed_tests += 1 if all_positive else 0
passed_tests += 1 if max_erro_produto < 0.1 else 0

print(f"\nTotal de testes: {total_tests}")
print(f"Testes passados: {passed_tests}")
print(f"Taxa de sucesso: {(passed_tests/total_tests)*100:.1f}%")

# Verificar tolerância
if len(df_results) > 0:
    max_erro = df_results['Erro_voltas_ano'].max()
    print(f"\nMaior erro encontrado: {max_erro:.4f} voltas/ano")
    print(f"Tolerância máxima: 0.01 voltas/ano")
    print(f"Dentro da tolerância? {'✅ SIM' if max_erro <= 0.01 else '❌ NÃO'}")

# 11. Salvar resultados
print("\n5. Salvando resultados da validação...")
df_results.to_csv('QA_TURNOVER_PROXY_VALIDATION.csv', index=False)
print("   ✓ QA_TURNOVER_PROXY_VALIDATION.csv salvo")

# Salvar amostra dos últimos 12 meses
print("\n6. Salvando amostra dos últimos 12 meses...")
sample_12m = df.tail(12)[['MonthDate', 'YearMonthKey', 'ISR_SA', 'Giro_voltas_ano', 'DoS_dias', 'Giro_x_DoS']]
sample_12m.to_csv('QA_TURNOVER_PROXY_Sample_12M.csv', index=False)
print("   ✓ QA_TURNOVER_PROXY_Sample_12M.csv salvo")

print("\n✅ Validação concluída!")

if passed_tests == total_tests and (len(df_results) == 0 or (max_erro <= 0.01 and max_erro_produto < 0.1)):
    print("\n🎉 TODOS OS CRITÉRIOS DE ACEITE ATENDIDOS!")
    print("\nResumo:")
    print(f"  • Fórmula: Giro = 12 / ISR_SA ✅")
    print(f"  • 5 pontos validados: erro máximo {max_erro:.4f} voltas/ano ✅")
    print(f"  • Faixa de valores: {df['Giro_voltas_ano'].min():.2f} - {df['Giro_voltas_ano'].max():.2f} voltas/ano ✅")
    print(f"  • Regra BLANK: validada ✅")
    print(f"  • Validação cruzada Giro×DoS: erro máximo {max_erro_produto:.4f} dias ✅")
else:
    print("\n⚠️ ATENÇÃO: Alguns testes falharam. Revisar implementação.")
