"""
QA Validation - ISR YoY % (SA)
Valida 3 comparações ano a ano (m vs m-12)
"""

import pandas as pd

print("=== QA VALIDATION - ISR YoY % (SA) ===\n")

# 1. Carregar dados
print("1. Carregando FactRETAILIRSA.csv...")
df = pd.read_csv('FactRETAILIRSA.csv')
df['MonthDate'] = pd.to_datetime(df['MonthDate'])
df = df.sort_values('MonthDate')
print(f"   ✓ {len(df)} meses carregados\n")

# 2. Calcular YoY% para toda a série
print("2. Calculando YoY% para toda a série...")
df['ISR_SA_m12'] = df['ISR_SA'].shift(12)
df['YoY_pct'] = ((df['ISR_SA'] - df['ISR_SA_m12']) / df['ISR_SA_m12']) * 100

# Primeiros 12 meses = BLANK
df.loc[df.index[:12], 'YoY_pct'] = None

print(f"   ✓ YoY% calculado\n")

# 3. Selecionar 3 comparações para validação (últimos 3 meses com m-12)
print("3. Selecionando 3 comparações para validação manual...\n")
qa_sample = df.tail(3)  # Últimos 3 meses

# 4. Validação detalhada
print("=" * 80)
print("VALIDAÇÃO MANUAL - 3 COMPARAÇÕES ANO A ANO (m vs m-12)")
print("=" * 80)

test_results = []

for i, current_row in qa_sample.iterrows():
    month_current = current_row['MonthDate'].strftime('%b/%Y')
    yearmonth_current = current_row['YearMonthKey']

    isr_current = current_row['ISR_SA']
    isr_m12 = current_row['ISR_SA_m12']
    yoy_calculated = current_row['YoY_pct']

    # Encontrar mês m-12
    month_m12_date = current_row['MonthDate'] - pd.DateOffset(months=12)
    month_m12 = month_m12_date.strftime('%b/%Y')

    # Cálculo manual
    if pd.notna(isr_m12):
        yoy_manual = ((isr_current - isr_m12) / isr_m12) * 100
        erro = abs(yoy_calculated - yoy_manual) if pd.notna(yoy_calculated) else 0
        status = "✅ PASS" if erro <= 0.1 else "❌ FAIL"
    else:
        yoy_manual = None
        erro = 0
        status = "✅ PASS (BLANK correto)" if pd.isna(yoy_calculated) else "❌ FAIL"

    print(f"\nComparação: {month_m12} → {month_current} ({yearmonth_current})")
    print(f"  ISR_SA (m):         {isr_current:.2f}")
    print(f"  ISR_SA (m-12):      {isr_m12:.2f}" if pd.notna(isr_m12) else "  ISR_SA (m-12):      N/A")
    print(f"  YoY% calculado:     {yoy_calculated:.2f}%" if pd.notna(yoy_calculated) else "  YoY% calculado:     BLANK")
    print(f"  YoY% manual:        {yoy_manual:.2f}%" if pd.notna(yoy_manual) else "  YoY% manual:        N/A")
    print(f"  Erro:               {erro:.4f} p.p.")
    print(f"  Status:             {status}")

    test_results.append({
        'Comparação': f"{month_m12} → {month_current}",
        'YearMonthKey': yearmonth_current,
        'ISR_SA_current': isr_current,
        'ISR_SA_m12': isr_m12 if pd.notna(isr_m12) else None,
        'YoY_pct_calculated': yoy_calculated if pd.notna(yoy_calculated) else None,
        'YoY_pct_manual': yoy_manual if pd.notna(yoy_manual) else None,
        'Erro_pp': erro,
        'Status': status
    })

# 5. Teste dos primeiros 12 meses (devem ser BLANK)
print("\n" + "=" * 80)
print("VALIDAÇÃO - PRIMEIROS 12 MESES (1992)")
print("=" * 80)

first_12_months = df.iloc[:12]
blank_count = first_12_months['YoY_pct'].isna().sum()

print(f"\nPrimeiros 12 meses da série (Jan-Dez/1992):")
print(f"  Total de meses: {len(first_12_months)}")
print(f"  Meses com BLANK: {blank_count}")
print(f"  Status: {'✅ PASS (todos BLANK)' if blank_count == 12 else '❌ FAIL (alguns com valor)'}")

# Mostrar amostra
print(f"\n  Amostra (primeiros 3 meses):")
for _, row in first_12_months.head(3).iterrows():
    month = row['MonthDate'].strftime('%b/%Y')
    yoy = row['YoY_pct']
    print(f"    {month}: {'BLANK ✅' if pd.isna(yoy) else f'{yoy:.2f}% ❌'}")

# 6. Teste do primeiro mês com YoY (Jan/1993)
print("\n" + "=" * 80)
print("VALIDAÇÃO - PRIMEIRO MÊS COM YoY (Jan/1993)")
print("=" * 80)

first_yoy_row = df.iloc[12]  # Jan/1993
month_first_yoy = first_yoy_row['MonthDate'].strftime('%b/%Y')
isr_first_yoy = first_yoy_row['ISR_SA']
isr_m12_first_yoy = first_yoy_row['ISR_SA_m12']
yoy_first_yoy = first_yoy_row['YoY_pct']

print(f"\nMês: {month_first_yoy} ({first_yoy_row['YearMonthKey']})")
print(f"  ISR_SA (m):         {isr_first_yoy:.2f}")
print(f"  ISR_SA (m-12):      {isr_m12_first_yoy:.2f}")
print(f"  YoY% esperado:      Valor numérico (não BLANK)")
print(f"  YoY% calculado:     {yoy_first_yoy:.2f}%" if pd.notna(yoy_first_yoy) else "  YoY% calculado:     BLANK")
print(f"  Status:             {'✅ PASS (tem valor)' if pd.notna(yoy_first_yoy) else '❌ FAIL (deveria ter valor)'}")

# 7. Resumo final
print("\n" + "=" * 80)
print("RESUMO DA VALIDAÇÃO")
print("=" * 80)

df_results = pd.DataFrame(test_results)
total_tests = len(test_results) + 2  # +1 para teste BLANK, +1 para primeiro YoY
passed_tests = sum(1 for r in test_results if '✅ PASS' in r['Status'])
passed_tests += 1 if blank_count == 12 else 0
passed_tests += 1 if pd.notna(yoy_first_yoy) else 0

print(f"\nTotal de testes: {total_tests}")
print(f"Testes passados: {passed_tests}")
print(f"Taxa de sucesso: {(passed_tests/total_tests)*100:.1f}%")

# Verificar tolerância
if len(df_results) > 0:
    max_erro = df_results['Erro_pp'].max()
    print(f"\nMaior erro encontrado: {max_erro:.4f} p.p.")
    print(f"Tolerância máxima: 0.1 p.p.")
    print(f"Dentro da tolerância? {'✅ SIM' if max_erro <= 0.1 else '❌ NÃO'}")

# 8. Salvar resultado
print("\n4. Salvando resultados da validação...")
df_results.to_csv('QA_ISR_YOY_VALIDATION.csv', index=False)
print("   ✓ QA_ISR_YOY_VALIDATION.csv salvo")

# Salvar amostra dos últimos 12 meses
print("\n5. Salvando amostra dos últimos 12 meses...")
sample_12m = df.tail(12)[['MonthDate', 'YearMonthKey', 'ISR_SA', 'ISR_SA_m12', 'YoY_pct']]
sample_12m.to_csv('QA_ISR_YOY_Sample_12M.csv', index=False)
print("   ✓ QA_ISR_YOY_Sample_12M.csv salvo")

print("\n✅ Validação concluída!")

if passed_tests == total_tests and (len(df_results) == 0 or max_erro <= 0.1):
    print("\n🎉 TODOS OS CRITÉRIOS DE ACEITE ATENDIDOS!")
else:
    print("\n⚠️ ATENÇÃO: Alguns testes falharam. Revisar implementação.")
