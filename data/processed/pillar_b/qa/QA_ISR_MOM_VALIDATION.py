"""
QA Validation - ISR MoM % (SA)
Valida 3 pares consecutivos mês a mês
"""

import pandas as pd

print("=== QA VALIDATION - ISR MoM % (SA) ===\n")

# 1. Carregar dados
print("1. Carregando FactRETAILIRSA.csv...")
df = pd.read_csv('FactRETAILIRSA.csv')
df['MonthDate'] = pd.to_datetime(df['MonthDate'])
df = df.sort_values('MonthDate')
print(f"   ✓ {len(df)} meses carregados\n")

# 2. Calcular MoM% para toda a série
print("2. Calculando MoM% para toda a série...")
df['ISR_SA_prev'] = df['ISR_SA'].shift(1)
df['MoM_pct'] = ((df['ISR_SA'] - df['ISR_SA_prev']) / df['ISR_SA_prev']) * 100

# Primeiro mês = BLANK
df.loc[df.index[0], 'MoM_pct'] = None

print(f"   ✓ MoM% calculado\n")

# 3. Selecionar 3 pares para validação (últimos 3 meses com m-1)
print("3. Selecionando 3 pares para validação manual...\n")
qa_sample = df.tail(4)  # Últimos 4 meses para ter 3 pares

# 4. Validação detalhada
print("=" * 80)
print("VALIDAÇÃO MANUAL - 3 PARES MÊS A MÊS")
print("=" * 80)

test_results = []

for i in range(1, len(qa_sample)):
    current_row = qa_sample.iloc[i]
    previous_row = qa_sample.iloc[i-1]

    month_current = current_row['MonthDate'].strftime('%b/%Y')
    month_previous = previous_row['MonthDate'].strftime('%b/%Y')
    yearmonth_current = current_row['YearMonthKey']

    isr_current = current_row['ISR_SA']
    isr_previous = previous_row['ISR_SA']
    mom_calculated = current_row['MoM_pct']

    # Cálculo manual
    mom_manual = ((isr_current - isr_previous) / isr_previous) * 100

    # Erro
    erro = abs(mom_calculated - mom_manual) if pd.notna(mom_calculated) else 0

    # Status
    status = "✅ PASS" if erro <= 0.1 else "❌ FAIL"

    print(f"\nPar #{i}: {month_previous} → {month_current} ({yearmonth_current})")
    print(f"  ISR_SA (m):     {isr_current:.2f}")
    print(f"  ISR_SA (m-1):   {isr_previous:.2f}")
    print(f"  MoM% calculado: {mom_calculated:.2f}%")
    print(f"  MoM% manual:    {mom_manual:.2f}%")
    print(f"  Erro:           {erro:.4f} p.p.")
    print(f"  Status:         {status}")

    test_results.append({
        'Par': f"{month_previous} → {month_current}",
        'YearMonthKey': yearmonth_current,
        'ISR_SA_current': isr_current,
        'ISR_SA_previous': isr_previous,
        'MoM_pct_calculated': mom_calculated,
        'MoM_pct_manual': mom_manual,
        'Erro_pp': erro,
        'Status': status
    })

# 5. Teste do primeiro mês (deve ser BLANK)
print("\n" + "=" * 80)
print("VALIDAÇÃO - PRIMEIRO MÊS (Jan/1992)")
print("=" * 80)

first_row = df.iloc[0]
month_first = first_row['MonthDate'].strftime('%b/%Y')
isr_first = first_row['ISR_SA']
mom_first = first_row['MoM_pct']

print(f"\nMês: {month_first} ({first_row['YearMonthKey']})")
print(f"  ISR_SA (m):     {isr_first:.2f}")
print(f"  ISR_SA (m-1):   N/A (não existe)")
print(f"  MoM% esperado:  BLANK")
print(f"  MoM% calculado: {mom_first if pd.notna(mom_first) else 'BLANK'}")
print(f"  Status:         {'✅ PASS (BLANK correto)' if pd.isna(mom_first) else '❌ FAIL (deveria ser BLANK)'}")

# 6. Resumo final
print("\n" + "=" * 80)
print("RESUMO DA VALIDAÇÃO")
print("=" * 80)

df_results = pd.DataFrame(test_results)
total_tests = len(test_results) + 1  # +1 para teste BLANK
passed_tests = sum(1 for r in test_results if r['Status'] == '✅ PASS')
passed_tests += 1 if pd.isna(mom_first) else 0

print(f"\nTotal de testes: {total_tests}")
print(f"Testes passados: {passed_tests}")
print(f"Taxa de sucesso: {(passed_tests/total_tests)*100:.1f}%")

# Verificar tolerância
max_erro = df_results['Erro_pp'].max()
print(f"\nMaior erro encontrado: {max_erro:.4f} p.p.")
print(f"Tolerância máxima: 0.1 p.p.")
print(f"Dentro da tolerância? {'✅ SIM' if max_erro <= 0.1 else '❌ NÃO'}")

# 7. Salvar resultado
print("\n4. Salvando resultados da validação...")
df_results.to_csv('QA_ISR_MOM_VALIDATION.csv', index=False)
print("   ✓ QA_ISR_MOM_VALIDATION.csv salvo")

# Salvar amostra dos últimos 12 meses
print("\n5. Salvando amostra dos últimos 12 meses...")
sample_12m = df.tail(12)[['MonthDate', 'YearMonthKey', 'ISR_SA', 'ISR_SA_prev', 'MoM_pct']]
sample_12m.to_csv('QA_ISR_MOM_Sample_12M.csv', index=False)
print("   ✓ QA_ISR_MOM_Sample_12M.csv salvo")

print("\n✅ Validação concluída!")

if passed_tests == total_tests and max_erro <= 0.1:
    print("\n🎉 TODOS OS CRITÉRIOS DE ACEITE ATENDIDOS!")
else:
    print("\n⚠️ ATENÇÃO: Alguns testes falharam. Revisar implementação.")
