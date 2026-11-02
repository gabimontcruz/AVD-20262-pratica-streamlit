
import pandas as pd
import plotly.express as px
import streamlit as st
import altair as alt

from src.data_loader import load_data

st.set_page_config(
    page_title="Campus Insights | Desempenho acadêmico",
    page_icon="🎓",
    layout="wide",
)

df = load_data()

if "status_aprovacao" not in df.columns and "final_exam_score" in df.columns:
    df["status_aprovacao"] = df["final_exam_score"].apply(
        lambda x: "Aprovado" if x >= 60 else "Reprovado"
    )

VARS_QUANT = [
    "study_time_hours",
    "attendance_percent",
    "sleep_hours",
    "previous_grade",
    "final_exam_score",
]

NOMES_VARIAVEIS = {
    "study_time_hours": "Horas de estudo",
    "attendance_percent": "Frequência (%)",
    "sleep_hours": "Horas de sono",
    "previous_grade": "Nota anterior",
    "final_exam_score": "Nota final",
}

tab1, tab2 = st.tabs([
    "01 | Análise exploratória",
    "02 | Desempenho dos estudantes",
])

# DASHBOARD 1

with tab1:

    st.caption("DASHBOARD 01 • ANÁLISE EXPLORATÓRIA")

    st.title("Desempenho acadêmico e hábitos de estudo")

    st.markdown(
        """
        Explore os dados e identifique relações entre os hábitos
        de estudo e o desempenho acadêmico dos estudantes.
        """
    )

    st.divider()

    with st.sidebar:
        st.title("Configurações")
        st.caption("Personalize sua análise.")

        variaveis = st.multiselect(
            "Variáveis quantitativas",
            options=VARS_QUANT,
            default=VARS_QUANT,
            format_func=lambda var: NOMES_VARIAVEIS[var],
            help="Selecione as variáveis que deseja analisar.",
        )

        separar_por_classe = st.toggle(
            "Distinguir por status de aprovação",
            value=False,
        )

        st.divider()
        st.subheader("Intervalos")

        intervalos = {}

        for var in variaveis:
            if pd.api.types.is_integer_dtype(df[var]):
                minimo = int(df[var].min())
                maximo = int(df[var].max())
                passo = 1
            else:
                minimo = float(df[var].min())
                maximo = float(df[var].max())
                passo = 0.1

            intervalos[var] = st.slider(
                f"Intervalo de {NOMES_VARIAVEIS[var]}",
                min_value=minimo,
                max_value=maximo,
                value=(minimo, maximo),
                step=passo,
                key=f"intervalo_{var}",
            )

    df_filtrado = df.copy()

    for var, (inicio, fim) in intervalos.items():
        df_filtrado = df_filtrado[
            df_filtrado[var].between(inicio, fim)
        ]

    st.caption(
        f"Exibindo {len(df_filtrado)} de {len(df)} estudantes "
        "considerando os filtros selecionados."
    )

    st.divider()

    st.subheader("01 | Explorando os dados")

    st.markdown(
        "Investigue a relação entre as variáveis e observe "
        "como os dados estão distribuídos."
    )

    if len(df_filtrado) == 0:
        st.warning(
            "Nenhum estudante encontrado. Ajuste os intervalos dos filtros."
        )

    else:
        col_correlacao, col_distribuicao = st.columns([1.1, 1.3])

        with col_correlacao:
            st.markdown("**Matriz de correlação**")

            if len(variaveis) < 2:
                st.info(
                    "Selecione pelo menos duas variáveis para visualizar "
                    "a matriz de correlação."
                )
            else:
                corr_matrix = df_filtrado[variaveis].corr().round(2)

                corr_matrix = corr_matrix.rename(
                    index=NOMES_VARIAVEIS,
                    columns=NOMES_VARIAVEIS,
                )

                fig_corr = px.imshow(
                    corr_matrix,
                    text_auto=True,
                    color_continuous_scale=[
                        "#EFF6FF",
                        "#93C5FD",
                        "#2563EB",
                    ],
                    aspect="auto",
                    title="Relação entre as variáveis",
                )

                fig_corr.update_layout(
                    margin=dict(l=20, r=20, t=40, b=20),
                )

                st.plotly_chart(
                    fig_corr,
                    use_container_width=True,
                )
                st.caption("Correlação de Pearson: valores próximos de +1/-1 indicam associação linear; não implicam causalidade.")

        with col_distribuicao:
            st.markdown("**Distribuição das variáveis**")

            if variaveis:
                var_selecionada = st.selectbox(
                    "Escolha uma variável:",
                    options=variaveis,
                    index=0,
                    format_func=lambda var: NOMES_VARIAVEIS[var],
                )

                color_col = (
                    "status_aprovacao" if separar_por_classe else None
                )

                fig_hist = px.histogram(
                    df_filtrado,
                    x=var_selecionada,
                    color=color_col,
                    labels=NOMES_VARIAVEIS,
                    marginal="box",
                    barmode=(
                        "overlay" if separar_por_classe else "relative"
                    ),
                    opacity=0.7,
                    color_discrete_map={
                        "Aprovado": "#2563EB",
                        "Reprovado": "#FB7185",
                    },
                    title=(
                        f"Distribuição de "
                        f"{NOMES_VARIAVEIS[var_selecionada]}"
                    ),
                )

                fig_hist.update_layout(
                    xaxis_title=NOMES_VARIAVEIS[var_selecionada],
                    yaxis_title="Quantidade de estudantes",
                    margin=dict(l=20, r=20, t=40, b=20),
                )

                st.plotly_chart(
                    fig_hist,
                    use_container_width=True,
                )
            else:
                st.info(
                    "Selecione ao menos uma variável no menu lateral."
                )


# DASHBOARD 2

with tab2:

    st.caption("DASHBOARD 02 • INDICADORES DE DESEMPENHO")

    st.title("Desempenho dos estudantes")

    st.markdown(
        """
        Acompanhe os indicadores acadêmicos e explore como os
        hábitos de estudo se relacionam com os resultados dos estudantes.
        """
    )

    st.divider()

    st.subheader("Filtros de análise")

    filtro1, filtro2, filtro3 = st.columns(3)

    with filtro1:
        status_selecionado = st.selectbox(
            "Status de aprovação",
            options=["Todos"] + sorted(
                df["status_aprovacao"].dropna().unique().tolist()
            ),
        )

    with filtro2:
        minimo_estudo = float(df["study_time_hours"].min())
        maximo_estudo = float(df["study_time_hours"].max())

        faixa_estudo = st.slider(
            "Horas de estudo",
            min_value=minimo_estudo,
            max_value=maximo_estudo,
            value=(minimo_estudo, maximo_estudo),
        )

    with filtro3:
        minimo_frequencia = float(df["attendance_percent"].min())
        maximo_frequencia = float(df["attendance_percent"].max())

        faixa_frequencia = st.slider(
            "Frequência (%)",
            min_value=minimo_frequencia,
            max_value=maximo_frequencia,
            value=(minimo_frequencia, maximo_frequencia),
        )

    df_dashboard2 = df.copy()

    if status_selecionado != "Todos":
        df_dashboard2 = df_dashboard2[
            df_dashboard2["status_aprovacao"] == status_selecionado
        ]

    df_dashboard2 = df_dashboard2[
        df_dashboard2["study_time_hours"].between(
            faixa_estudo[0],
            faixa_estudo[1],
        )
    ]

    df_dashboard2 = df_dashboard2[
        df_dashboard2["attendance_percent"].between(
            faixa_frequencia[0],
            faixa_frequencia[1],
        )
    ]

    st.divider()

    st.subheader("Indicadores principais")

    if len(df_dashboard2) == 0:
        st.warning(
            "Nenhum estudante encontrado. Ajuste os filtros selecionados."
        )

    else:
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)

        media_estudo = df_dashboard2["study_time_hours"].mean()
        media_frequencia = df_dashboard2["attendance_percent"].mean()
        media_nota_final = df_dashboard2["final_exam_score"].mean()

        taxa_aprovacao = (
            (df_dashboard2["status_aprovacao"] == "Aprovado").sum()
            / len(df_dashboard2)
            * 100
        )

        kpi1.metric(
            "Média de horas de estudo",
            f"{media_estudo:.2f} h",
        )

        kpi2.metric(
            "Frequência média",
            f"{media_frequencia:.1f}%",
        )

        kpi3.metric(
            "Nota média final",
            f"{media_nota_final:.1f} pts",
        )

        kpi4.metric(
            "Taxa de aprovação",
            f"{taxa_aprovacao:.1f}%",
        )

        st.caption(
            f"Indicadores calculados com base em "
            f"{len(df_dashboard2)} estudantes."
        )

        st.divider()

        st.subheader("Análises complementares")

        st.markdown("**Horas de estudo e nota final**")

        grafico_dispersao = alt.Chart(df_dashboard2).mark_circle(
            size=65,
            opacity=0.65,
        ).encode(
            x=alt.X(
                "study_time_hours:Q",
                title="Horas de estudo",
            ),
            y=alt.Y(
                "final_exam_score:Q",
                title="Nota final",
            ),
            color=alt.Color(
                "status_aprovacao:N",
                title="Status",
                scale=alt.Scale(
                    domain=["Aprovado", "Reprovado"],
                    range=["#2563EB", "#FB7185"],
                ),
            ),
            tooltip=[
                alt.Tooltip(
                    "study_time_hours:Q",
                    title="Horas de estudo",
                ),
                alt.Tooltip(
                    "final_exam_score:Q",
                    title="Nota final",
                ),
                alt.Tooltip(
                    "status_aprovacao:N",
                    title="Status",
                ),
            ],
        ).properties(
            height=350,
        ).interactive()

        st.altair_chart(
            grafico_dispersao,
            use_container_width=True,
        )

        st.markdown("**Nota média por status de aprovação**")

        dados_status = (
            df_dashboard2.groupby("status_aprovacao", as_index=False)
            ["final_exam_score"]
            .mean()
        )

        grafico_status = alt.Chart(dados_status).mark_bar(
            cornerRadiusTopLeft=6,
            cornerRadiusTopRight=6,
        ).encode(
            x=alt.X(
                "status_aprovacao:N",
                title="Status de aprovação",
            ),
            y=alt.Y(
                "final_exam_score:Q",
                title="Nota média final",
            ),
            color=alt.Color(
                "status_aprovacao:N",
                title="Status",
                scale=alt.Scale(
                    domain=["Aprovado", "Reprovado"],
                    range=["#2563EB", "#FB7185"],
                ),
                legend=None,
            ),
            tooltip=[
                alt.Tooltip(
                    "status_aprovacao:N",
                    title="Status",
                ),
                alt.Tooltip(
                    "final_exam_score:Q",
                    title="Nota média",
                    format=".2f",
                ),
            ],
        ).properties(
            height=300,
        )

        st.altair_chart(
            grafico_status,
            use_container_width=True,
        )

        st.markdown("**Distribuição de desempenho por faixa de estudo**")
        st.caption(
            "Quantidade de estudantes por faixa de horas de estudo e situação "
            "de aprovação. Passe o mouse sobre as barras para explorar os valores."
        )
        # Calculado com o mesmo dataframe filtrado dos indicadores.
        faixas = pd.cut(
            df_dashboard2["study_time_hours"],
            bins=[-float("inf"), 2, 4, 6, float("inf")],
            labels=["Até 2h", "2–4h", "4–6h", "Acima de 6h"],
            include_lowest=True,
        )
        dados_faixas = (
            df_dashboard2.assign(faixa_de_estudo=faixas)
            .groupby(["faixa_de_estudo", "status_aprovacao"], observed=True)
            .size()
            .reset_index(name="quantidade")
        )
        grafico_faixas = (
            alt.Chart(dados_faixas)
            .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
            .encode(
                x=alt.X(
                    "faixa_de_estudo:N",
                    sort=["Até 2h", "2–4h", "4–6h", "Acima de 6h"],
                    title="Horas de estudo por dia",
                ),
                y=alt.Y("quantidade:Q", title="Número de estudantes"),
                color=alt.Color(
                    "status_aprovacao:N",
                    title="Situação",
                    scale=alt.Scale(
                        domain=["Aprovado", "Reprovado"],
                        range=["#2563EB", "#FB7185"],
                    ),
                ),
                tooltip=[
                    alt.Tooltip("faixa_de_estudo:N", title="Faixa"),
                    alt.Tooltip("status_aprovacao:N", title="Situação"),
                    alt.Tooltip("quantidade:Q", title="Estudantes"),
                ],
            )
            .properties(height=300)
        )
        st.altair_chart(grafico_faixas, use_container_width=True)

        with st.expander("Consultar dados filtrados e definições dos indicadores"):
            st.markdown(
                "**Nota média final**: média de `final_exam_score`.  "
                "**Taxa de aprovação**: proporção de estudantes classificados "
                "como Aprovado no dataset tratado.  "
                "**Frequência média**: média de `attendance_percent`.  "
                "**Horas médias de estudo**: média de `study_time_hours`."
            )
            st.dataframe(
                df_dashboard2[["study_time_hours", "attendance_percent", "final_exam_score", "status_aprovacao"]],
                use_container_width=True,
                hide_index=True,
            )

st.divider()

st.caption(
    "Projeto de análise exploratória e visualização "
    "de dados sobre hábitos de estudo e desempenho acadêmico."
)
