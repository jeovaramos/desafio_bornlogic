from json import tool
import pandas as pd
import datetime as dt
import streamlit as st
import plotly.express as px
from lib.toolkit import DSToolKit
from lib.maps import Mapping

st.set_page_config(
    page_title="Jeová - Bornlogic",
    page_icon=":brain:",
    layout="wide",
    initial_sidebar_state="collapsed"
)

toolkit = DSToolKit()
mapping = Mapping()


def pergunta_1(df_metrics, df_historic):
    st.subheader("Pergunta 1 - Visualizações das métricas de desenvolvimento humano")
    column1, column2 = st.columns(2)

    variable_globe = column1.selectbox("Variable", df_metrics.columns[2:])
    globe_fig = mapping.globe_figure(df_metrics, variable_globe)
    column1.plotly_chart(globe_fig, use_container_width=True)

    variable_mundi = column2.selectbox("Variable", df_historic.columns[2:])
    mundi_fig = mapping.mundi_figure(df_historic, variable_mundi)
    column2.plotly_chart(mundi_fig, use_container_width=True)


def main():
    # column_head_1, column_head_2 = st.columns(2)
    # column_head_1.image("figures/bornlogic_logo.jpeg")
    st.title("Desafio Bornlogic")
    st.subheader("Jeová Ramos")

    df_metrics, df_historic = toolkit.load_datasets()

    pergunta_1(df_metrics, df_historic)

    st.subheader("Pergunta 2 - Identificação da região do mundo")
    fig_metrics_pca = toolkit.pca_embedding(df_metrics)
    st.plotly_chart(fig_metrics_pca,  use_container_width=True)

    fig_historic_pca = toolkit.pca_embedding(df_historic)
    st.plotly_chart(fig_metrics_pca,  use_container_width=True)


if __name__ == "__main__":
    main()
