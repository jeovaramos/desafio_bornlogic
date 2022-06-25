import pandas as pd
import datetime as dt
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="Jeová - Bornlogic",
    page_icon=":brain:",
    layout="wide",
    initial_sidebar_state="collapsed"
)


@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def load_datasets():
    data_metrics = pd.read_excel("data/Data_2021.xls")
    data_historic = pd.read_excel("data/Historic_data.xls")

    return data_metrics, data_historic


def main():
    st.title("Desafio Bornlogic")
    st.subheader("Jeová Ramos")
    st.write("Hello, world.")


if __name__ == "__main__":
    main()
