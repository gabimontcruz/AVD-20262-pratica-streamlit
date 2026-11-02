# Campus Insights — desempenho acadêmico | AVD Aulas 21–23

Dashboard Streamlit de análise dos hábitos de estudo e desempenho acadêmico de 1.000 estudantes. Trabalho de Análise e Visualização de Dados — Cesar School, 2026.2.

**Aplicação pública:** `COLE_AQUI_O_LINK_DO_STREAMLIT_APOS_O_DEPLOY`  
**Repositório público:** `COLE_AQUI_O_LINK_DO_SEU_REPOSITORIO`

## Painéis

- **Dashboard 1 — análise exploratória:** escolha de variáveis quantitativas, filtros de intervalo, correlação de Pearson (heatmap) e distribuição (histograma + boxplot); aceita seleções de 0, 1 ou várias variáveis.
- **Dashboard 2 — desempenho:** filtros por status, tempo de estudo e frequência; quatro métricas dinâmicas e três visuais (dispersão, média por status e faixas de estudo).
- **Fonte:** notebook de EDA em `notebooks/`, dados tratados em `data/clean/dataset.csv`; dados brutos ignorados no Git.

## Instalação e execução (Windows / PowerShell)

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Para ativação bloqueada pelo PowerShell: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`.

## Como publicar no Streamlit Community Cloud

1. Publique este projeto no GitHub em um repositório público, com `app.py`, `requirements.txt`, `.streamlit/config.toml` e `data/clean/dataset.csv`.
2. Entre em https://streamlit.io/cloud com a conta GitHub correta, selecione **Create app** e o repositório.
3. Configure branch `main` e arquivo principal `app.py`. Nas configurações avançadas, selecione Python 3.12 (ou versão compatível).
4. Clique em **Deploy**. Depois de obter a URL pública, substitua o placeholder acima pelo link real, faça commit/push.
5. Abra o link em janela anônima e confira abas, filtros, indicadores e todos os três gráficos; veja logs em **Manage app** se houver falha.

## Estrutura de entrega

- `app.py` — aplicação com dois dashboards.
- `data/clean/dataset.csv` — dataset tratado e versionável.
- `notebooks/` — notebooks de EDA, incluindo o original.
- `entregas/` — dois rascunhos digitais das telas e justificativa dos KPIs.
- `prompts/declaracao-uso-ia.md` — declaração transparente de apoio da IA.
- `.streamlit/config.toml` — identidade visual.

**Atenção:** os rascunhos fornecidos são digitais; se você desenhar no Paint ou em papel, pode substituí-los. A publicação no GitHub e o deploy precisam ser concluídos por você.
