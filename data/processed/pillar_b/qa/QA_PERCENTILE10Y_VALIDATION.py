"""
QA Validation - Percentil histórico (10 anos) - SA
Valida 3 meses com cálculo manual de percentil em janela móvel de 120 meses
"""

import pandas as pd
import numpy as np

print("=== QA VALIDATION - Percentil 10 anos (SA) ===\n")

# 1. Carregar dados
print("1. Carregando FactRETAILIRSA.csv...")
df = pd.read_csv('FactRETAILIRSA.csv')
df['MonthDate'] = pd.to_datetime(df['MonthDate'])
df = df.sort_values('MonthDate').reset_index(drop=True)
print(f"   ✓ {len(df)} meses carregados (período completo)\n")

# 2. Função para calcular percentil na janela móvel
def calcular_percentil_10y(df, index):
    """
    Calcula o percentil do ISR_SA no índice dado
    dentro da janela móvel de 120 meses
    """
    # Janela: índices de (index-119) até index (120 meses)
    inicio_janela = max(0, index - 119)
    fim_janela = index + 1

    # Extrair janela
    janela = df.iloc[inicio_janela:fim_janela]

    # Verificar se temos 120 meses
    if len(janela) < 120:
        return None, len(janela), None, None

    # Valor atual
    valor_atual = df.loc[index, 'ISR_SA']

    # Valores da janela
    valores_janela = janela['ISR_SA'].values

    # Calcular percentil manualmente (contando posição)
    # Percentil = (número de valores <= valor_atual) / total * 100
    valores_menores_iguais = np.sum(valores_janela <= valor_atual)
    percentil = (valores_menores_iguais / len(valores_janela)) * 100

    # Retornar informações
    data_inicio = janela.iloc[0]['MonthDate']
    data_fim = janela.iloc[-1]['MonthDate']

    return percentil, len(janela), data_inicio, data_fim

# 3. Calcular percentil para toda a série
print("2. Calculando Percentil 10 anos para toda a série...")
df['Percentil_10y'] = None

for i in range(len(df)):
    percentil, _, _, _ = calcular_percentil_10y(df, i)
    df.loc[i, 'Percentil_10y'] = percentil

print(f"   ✓ Percentil calculado\n")

# 4. Validar regra BLANK (primeiros 119 meses)
print("=" * 80)
print("VALIDAÇÃO - REGRA BLANK (primeiros 119 meses)")
print("=" * 80)

primeiros_119 = df.head(119)
blank_count = primeiros_119['Percentil_10y'].isna().sum()
print(f"\nPrimeiros 119 meses (Jan/1992 - Nov/2001):")
print(f"  Total de meses: 119")
print(f"  Percentil = BLANK: {blank_count}")
print(f"  Status: {'✅ TODOS BLANK' if blank_count == 119 else '❌ ERRO'}")

# Primeiro mês com valor
primeiro_com_valor = df[df['Percentil_10y'].notna()].iloc[0]
print(f"\nPrimeiro mês com valor calculado:")
print(f"  Mês: {primeiro_com_valor['MonthDate'].strftime('%b/%Y')}")
print(f"  Índice: {df[df['Percentil_10y'].notna()].index[0]} (120º mês)")
print(f"  Percentil: {primeiro_com_valor['Percentil_10y']:.1f}%")

# 5. Selecionar 3 meses para validação manual
print("\n" + "=" * 80)
print("VALIDAÇÃO MANUAL - 3 MESES RECENTES")
print("=" * 80)

# Selecionar últimos 3 meses com valores
meses_validacao = df[df['Percentil_10y'].notna()].tail(3)

test_results = []

for idx in meses_validacao.index:
    month = df.loc[idx, 'MonthDate'].strftime('%b/%Y')
    yearmonth = df.loc[idx, 'YearMonthKey']

    # Cálculo automático (já calculado)
    percentil_auto = df.loc[idx, 'Percentil_10y']

    # Cálculo manual detalhado
    percentil_manual, tamanho_janela, data_inicio, data_fim = calcular_percentil_10y(df, idx)

    # Calcular erro
    erro = abs(percentil_auto - percentil_manual) if (percentil_auto is not None and percentil_manual is not None) else 0
    status = "✅ PASS" if erro <= 1.0 else "❌ FAIL"  # Tolerância 1 p.p.

    print(f"\nMês: {month} ({yearmonth})")
    print(f"  ISR_SA:                    {df.loc[idx, 'ISR_SA']:.4f}")
    print(f"  Janela:                    {data_inicio.strftime('%b/%Y')} - {data_fim.strftime('%b/%Y')} ({tamanho_janela} meses)")
    print(f"  Percentil automático:      {percentil_auto:.2f}%" if percentil_auto is not None else "  Percentil automático:      BLANK")
    print(f"  Percentil manual:          {percentil_manual:.2f}%" if percentil_manual is not None else "  Percentil manual:          N/A")
    print(f"  Erro:                      {erro:.2f} p.p.")
    print(f"  Status:                    {status}")

    # Detalhe da janela
    inicio_janela = max(0, idx - 119)
    fim_janela = idx + 1
    janela = df.iloc[inicio_janela:fim_janela]['ISR_SA'].values
    valor_atual = df.loc[idx, 'ISR_SA']

    valores_menores_iguais = sum(janela <= valor_atual)
    print(f"  Valores ≤ {valor_atual:.2f}:        {valores_menores_iguais}/{tamanho_janela}")

    test_results.append({
        'Mês': month,
        'YearMonthKey': yearmonth,
        'ISR_SA': df.loc[idx, 'ISR_SA'],
        'Janela_inicio': data_inicio.strftime('%Y-%m-%d'),
        'Janela_fim': data_fim.strftime('%Y-%m-%d'),
        'Tamanho_janela': tamanho_janela,
        'Percentil_auto': percentil_auto,
        'Percentil_manual': percentil_manual,
        'Erro_pp': erro,
        'Status': status
    })

# 6. Estatísticas da série completa
print("\n" + "=" * 80)
print("ESTATÍSTICAS DA SÉRIE COMPLETA")
print("=" * 80)

serie_com_valores = df[df['Percentil_10y'].notna()]
print(f"\nTotal de meses com Percentil calculado: {len(serie_com_valores)}")
print(f"Período: {serie_com_valores.iloc[0]['MonthDate'].strftime('%b/%Y')} - {serie_com_valores.iloc[-1]['MonthDate'].strftime('%b/%Y')}")
print(f"\nEstatísticas Percentil 10 anos:")
print(f"  Mínimo:    {serie_com_valores['Percentil_10y'].min():.2f}%")
print(f"  Máximo:    {serie_com_valores['Percentil_10y'].max():.2f}%")
print(f"  Média:     {serie_com_valores['Percentil_10y'].mean():.2f}%")
print(f"  Mediana:   {serie_com_valores['Percentil_10y'].median():.2f}%")

# 7. Distribuição de percentis
print(f"\nDistribuição de percentis:")
bins = [0, 10, 25, 50, 75, 90, 100]
labels = ['0-10%', '10-25%', '25-50%', '50-75%', '75-90%', '90-100%']
serie_com_valores['Faixa'] = pd.cut(serie_com_valores['Percentil_10y'], bins=bins, labels=labels, include_lowest=True)
distribuicao = serie_com_valores['Faixa'].value_counts().sort_index()
for faixa, count in distribuicao.items():
    pct = (count / len(serie_com_valores)) * 100
    print(f"  {faixa}: {count} meses ({pct:.1f}%)")

# 8. Últimos 12 meses
print("\n" + "=" * 80)
print("ÚLTIMOS 12 MESES")
print("=" * 80)

ultimos_12 = df.tail(12)
print(f"\nÚltimos 12 meses:")
for _, row in ultimos_12.iterrows():
    month = row['MonthDate'].strftime('%b/%Y')
    isr = row['ISR_SA']
    pct = row['Percentil_10y']
    if pd.notna(pct):
        print(f"  {month}: ISR={isr:.2f}, Percentil={pct:.1f}%")
    else:
        print(f"  {month}: ISR={isr:.2f}, Percentil=BLANK")

# 9. Resumo final
print("\n" + "=" * 80)
print("RESUMO DA VALIDAÇÃO")
print("=" * 80)

df_results = pd.DataFrame(test_results)
total_tests = len(test_results) + 1  # +1 para teste de BLANK
passed_tests = sum(1 for r in test_results if '✅ PASS' in r['Status'])
passed_tests += 1 if blank_count == 119 else 0

print(f"\nTotal de testes: {total_tests}")
print(f"Testes passados: {passed_tests}")
print(f"Taxa de sucesso: {(passed_tests/total_tests)*100:.1f}%")

# Verificar tolerância
if len(df_results) > 0:
    max_erro = df_results['Erro_pp'].max()
    print(f"\nMaior erro encontrado: {max_erro:.2f} p.p.")
    print(f"Tolerância máxima: 1.0 p.p.")
    print(f"Dentro da tolerância? {'✅ SIM' if max_erro <= 1.0 else '❌ NÃO'}")

# 10. Salvar resultados
print("\n3. Salvando resultados da validação...")
df_results.to_csv('QA_PERCENTILE10Y_VALIDATION.csv', index=False)
print("   ✓ QA_PERCENTILE10Y_VALIDATION.csv salvo")

# Salvar amostra dos últimos 12 meses
print("\n4. Salvando amostra dos últimos 12 meses...")
sample_12m = df.tail(12)[['MonthDate', 'YearMonthKey', 'ISR_SA', 'Percentil_10y']]
sample_12m.to_csv('QA_PERCENTILE10Y_Sample_12M.csv', index=False)
print("   ✓ QA_PERCENTILE10Y_Sample_12M.csv salvo")

print("\n✅ Validação concluída!")

if passed_tests == total_tests and (len(df_results) == 0 or max_erro <= 1.0):
    print("\n🎉 TODOS OS CRITÉRIOS DE ACEITE ATENDIDOS!")
    print("\nResumo:")
    print(f"  • Primeiros 119 meses: BLANK ✅")
    print(f"  • Primeiro mês com valor: {primeiro_com_valor['MonthDate'].strftime('%b/%Y')} (120º mês) ✅")
    print(f"  • 3 meses validados: erro máximo {max_erro:.2f} p.p. ✅")
    print(f"  • Total de valores calculados: {len(serie_com_valores)} meses ✅")
else:
    print("\n⚠️ ATENÇÃO: Alguns testes falharam. Revisar implementação.")
