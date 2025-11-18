# DAX - ISR (NSA) - Overlay/Toggle de Sazonalidade

**KPI:** ISR Not Seasonally Adjusted (Overlay)
**Nome Técnico:** `kpi_isr_nsa`
**Pilar:** B (Macro/Estratégico)
**Data:** 2025-11-18

---

## 1. Objetivo

Exibir a série **não ajustada sazonalmente** (NSA) como overlay/toggle sobre a série SA, permitindo visualizar a sazonalidade explícita do ISR.

---

## 2. Fórmula Matemática

```
ISR (NSA) = RETAILIRNSA
```

**Onde:**
- `RETAILIRNSA` = Inventories-to-Sales Ratio (Not Seasonally Adjusted)
- Valor direto da série FRED RETAILIRNSA

**Interpretação:**
- ISR_NSA reflete padrões sazonais naturais
- Comparação SA vs NSA revela intensidade da sazonalidade
- Picos/vales em NSA indicam períodos sazonais (ex: Natal, Back-to-School)

---

## 3. Fórmula DAX (Power BI)

```dax
ISR (NSA) =
VAR CurrentISR_NSA = SUM(FactISRSeasonalGap[ISR_NSA])
RETURN
    IF(
        ISBLANK(CurrentISR_NSA),
        BLANK(),
        CurrentISR_NSA
    )
```

**Componentes:**
- `FactISRSeasonalGap[ISR_NSA]`: Coluna com valores NSA
- `SUM`: Agregação (única linha por mês, então SUM = valor)
- `IF/ISBLANK`: Regra de BLANK para meses sem dados

---

## 4. Características

| Propriedade | Valor |
|-------------|-------|
| **Tipo** | Medida base (overlay/toggle) |
| **Unidade** | Razão (número decimal) |
| **Formato** | Número, 2 casas decimais |
| **Grão** | Mês (série nacional) |
| **Período** | Jan/1992 - Jul/2025 (403 meses) |
| **Uso** | Overlay sobre ISR (SA) - NÃO é série padrão |
| **Toggle** | Desligado por padrão, ligado sob demanda |

---

## 5. Regras de BLANK

| Condição | Resultado |
|----------|-----------|
| Mês sem ISR_NSA | BLANK |
| Mês com ISR_NSA | Valor do ISR_NSA |

**Exemplo:**
- ISR_NSA = 1.37 → Exibir 1.37
- ISR_NSA = BLANK → BLANK

---

## 6. Fontes de Dados

### Tabelas
- **FactISRSeasonalGap**: Fonte única (contém SA e NSA)

### Colunas
- `FactISRSeasonalGap[ISR_NSA]`

### Relacionamentos
- **dimmonth[YearMonthKey] → FactISRSeasonalGap[YearMonthKey]** (ATIVO)

### Origem Externa
- **FRED** (Federal Reserve Economic Data)
- **Série**: RETAILIRNSA
- **Descrição**: Retail Inventories to Sales Ratio (Not Seasonally Adjusted)

---

## 7. Interpretação de Valores

| ISR (NSA) | Interpretação | Contexto Sazonal |
|-----------|---------------|------------------|
| > ISR (SA) | Sazonalidade positiva | Estoque alto para a época |
| = ISR (SA) | Sem sazonalidade | Ajuste sazonal neutro |
| < ISR (SA) | Sazonalidade negativa | Estoque baixo para a época |

**Exemplo prático:**
- **Dezembro:** ISR_NSA = 1.45, ISR_SA = 1.37
  - Gap = +0.08 (sazonalidade positiva)
  - Interpretação: Estoque naturalmente mais alto no Natal

---

## 8. Estatísticas da Série (Jan/1992 - Jul/2025)

| Métrica | Valor | Mês |
|---------|-------|-----|
| **Mínimo** | 1.08 | Jun/2021 |
| **Máximo** | 1.85 | Dez/1992 |
| **Média** | 1.51 | - |
| **Mediana** | 1.51 | - |
| **Último (Jul/2025)** | 1.28 | - |

**Comparação SA vs NSA:**
- ISR_SA médio: 1.49
- ISR_NSA médio: 1.51
- Gap médio: +0.02 (NSA ligeiramente maior)

---

## 9. Formatação no Power BI

### Card/Visual Principal
```
Formato: Número
Casas decimais: 2
Sem sufixo
Exemplo: 1.37
```

### Rótulo
```
ISR (razão) — NSA
```

### Tooltip
```
ISR (NSA): 1.37
Mês: Jul/2025

Série não ajustada sazonalmente
Reflete padrões sazonais naturais
```

---

## 10. Implementação de Toggle/Overlay

### Opção 1: Slicer de Toggle
```
1. Criar Tabela de Dimensão:
   Toggle_ISR = {("SA"), ("NSA"), ("Ambos")}

2. Medida Dinâmica:
   ISR Dinâmico =
   VAR Selection = SELECTEDVALUE(Toggle_ISR[Tipo], "SA")
   RETURN
       SWITCH(Selection,
           "SA", [ISR (SA)],
           "NSA", [ISR (NSA)],
           "Ambos", [ISR (SA)]  // ou ambos no visual
       )
```

### Opção 2: Duas Séries no Visual
```
- Série 1: ISR (SA) - Linha sólida, azul
- Série 2: ISR (NSA) - Linha tracejada, cinza (oculta por padrão)
- Usuário liga/desliga série NSA via legenda
```

### Opção 3: Botão de Bookmark
```
- Bookmark 1: Apenas SA visível
- Bookmark 2: SA + NSA visíveis
- Botão toggle entre bookmarks
```

---

## 11. Caso de Uso

### Exemplo de Gráfico de Linha

```
ISR ao Longo do Tempo
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1.8 │                    ╱╲  ← NSA (tracejada)
1.7 │        ╱╲         ╱  ╲
1.6 │    ╱╲╱  ╲   ╱╲  ╱    ╲
1.5 │   ╱       ╲╱  ╲╱      ╲  ← SA (sólida)
1.4 │  ╱                     ╲
1.3 │ ╱                       ╲
    └────────────────────────────────
     J F M A M J J A S O N D (2024)

Legenda:
━━━━ ISR (SA) - Ajustado sazonalmente
- - - ISR (NSA) - Não ajustado (toggle OFF por padrão)
```

---

## 12. Validação QA

### Critérios de Aceite:
- ✅ Fórmula: ISR_NSA = valor direto do CSV
- ✅ Unidade: razão (não percentual)
- ✅ Regra BLANK: mês ausente → BLANK
- ✅ Toggle: desligado por padrão
- ✅ 3 pontos conferidos: valor idêntico ao CSV
- ✅ Overlay visível quando toggle ON

### Script de Validação:
`QA_ISR_NSA_VALIDATION.py`

---

## 13. Comparação SA vs NSA

### Gap Sazonal Típico por Mês

| Mês | Gap Típico | Interpretação |
|-----|------------|---------------|
| Jan | Negativo | Pós-Natal: estoque baixo |
| Fev | Negativo | Início de ano: estoque reduzido |
| Mar | Neutro | Equilíbrio |
| Abr | Neutro | Equilíbrio |
| Mai | Neutro | Equilíbrio |
| Jun | Neutro | Pré-verão |
| Jul | Positivo | Verão: preparação back-to-school |
| Ago | Positivo | Back-to-school: estoque alto |
| Set | Neutro | Pós-back-to-school |
| Out | Neutro | Pré-feriados |
| Nov | Positivo | Black Friday: estoque alto |
| Dez | **Muito Positivo** | Natal: pico de estoque |

---

## 14. Quando Usar NSA

### ✅ Usar NSA para:
- Identificar padrões sazonais recorrentes
- Planejar compras sazonais
- Validar ajustes sazonais (SA vs NSA)
- Análise de sazonalidade específica do varejo

### ❌ NÃO usar NSA para:
- Comparações ano-a-ano diretas
- Tendências de longo prazo
- Análise de políticas monetárias
- KPIs principais do dashboard

**Regra geral:** SA para análise, NSA para contexto sazonal

---

## 15. Relação com Outros KPIs

### Complementaridade:

| KPI | Relação com NSA |
|-----|-----------------|
| **ISR (SA)** | Base de comparação |
| **Seasonal Gap (abs)** | SA - NSA = Gap absoluto |
| **Seasonal Gap (%)** | (SA - NSA) / NSA × 100 |
| **ISR MoM %** | Usar SA para eliminar sazonalidade |
| **ISR YoY %** | Usar SA ou NSA (NSA compara sazonalidades) |

---

## 16. Dependências

### Medidas DAX:
- Nenhuma (medida independente)

### Tabelas:
- `FactISRSeasonalGap` - Fonte de ISR_NSA
- `dimmonth` - Calendário mensal

### Relacionamentos:
- `dimmonth[YearMonthKey] → FactISRSeasonalGap[YearMonthKey]` (ATIVO)

---

## 17. Arquivos Relacionados

| Arquivo | Descrição |
|---------|-----------|
| `FactISRSeasonalGap.csv` | Dados processados (403 meses, SA + NSA) |
| `DAX_ISR_SA.md` | Documentação da série ajustada |
| `DAX_ISR_SEASONAL_GAP.md` | Documentação do gap sazonal |
| `QA_ISR_NSA_VALIDATION.py` | Script de validação QA |
| `kpi_dictionary_pillar-B.md` | Dicionário de KPIs Pilar B |

---

## 18. Observações Importantes

### ⚠️ NSA como Overlay (NÃO série principal):

1. **Desligado por padrão**: NSA não deve ser a visualização padrão
2. **Contexto adicional**: Use para revelar sazonalidade, não para análise principal
3. **Comparação com SA**: Sempre mostre SA quando NSA estiver visível
4. **Legenda clara**: Diferenciar visualmente SA (principal) vs NSA (contexto)

### 📊 Uso Recomendado:

- Gráfico de linha com SA principal (linha sólida, destaque)
- NSA como linha secundária (tracejada, cor neutra)
- Toggle/slicer para mostrar/ocultar NSA
- Tooltip explicando diferença entre SA e NSA

---

**Última atualização:** 2025-11-18
**Versão:** 1.0
**Autor:** Dashboard E-Commerce Brasil - CEUB
