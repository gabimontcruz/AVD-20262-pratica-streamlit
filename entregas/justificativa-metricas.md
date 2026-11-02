# Justificativa das métricas — Dashboard 2

**Base:** `data/clean/dataset.csv`, 1.000 registros de estudantes. Os indicadores são recalculados com todos os filtros aplicados. Público-alvo: equipe pedagógica, coordenação e analistas educacionais.

## 1. Média de horas de estudo
- **Variável:** `study_time_hours`.
- **O que mede:** média de horas de estudo dos estudantes selecionados.
- **Por que foi escolhida:** sintetiza um hábito acadêmico potencialmente associado ao desempenho.
- **Público-alvo:** coordenação e equipe pedagógica.
- **Decisão apoiada:** avaliar necessidade de ações de orientação sobre planejamento de estudos.
- **O que comunica:** intensidade média de dedicação nos grupos comparados.

## 2. Frequência média
- **Variável:** `attendance_percent`.
- **O que mede:** média percentual de presença.
- **Por que foi escolhida:** a frequência é um indicador de participação nas aulas.
- **Público-alvo:** professores e coordenação.
- **Decisão apoiada:** planejar acompanhamento de assiduidade.
- **O que comunica:** participação média dos estudantes filtrados.

## 3. Nota média final
- **Variável:** `final_exam_score`.
- **O que mede:** média das notas da avaliação final.
- **Por que foi escolhida:** oferece resumo direto do resultado acadêmico.
- **Público-alvo:** professores, coordenação e analistas.
- **Decisão apoiada:** identificar segmentos com necessidade de reforço acadêmico.
- **O que comunica:** desempenho médio do grupo selecionado.

## 4. Taxa de aprovação
- **Variável:** `status_aprovacao` (categoria já presente no dado tratado).
- **O que mede:** número de registros `Aprovado` dividido pelo total de registros filtrados, multiplicado por 100.
- **Por que foi escolhida:** resume a proporção de sucesso acadêmico do grupo.
- **Público-alvo:** gestão pedagógica.
- **Decisão apoiada:** priorizar investigações e acompanhamento de segmentos de maior reprovação.
- **O que comunica:** participação de aprovados no conjunto filtrado.

## Justificativa das três visualizações

1. **Dispersão (horas de estudo x nota final):** observa associação, concentração e valores extremos, diferenciando status.
2. **Barras (nota média por status):** compara objetivamente médias entre as categorias; a comparação é descritiva.
3. **Barras por faixa de estudo e status:** discretiza o tempo de estudo em quatro faixas e compara quantidades de aprovados e reprovados.

> Os gráficos apresentam associações observadas na amostra e não permitem conclusões causais. As métricas representam somente os registros disponíveis e filtrados.
