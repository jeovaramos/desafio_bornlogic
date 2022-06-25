from streamlit_lottie import st_lottie
import streamlit as st
import requests

class Sections():
    def __init__(self) -> None:
        pass

    def load_lottieurl(self, url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None

        return r.json()

    def header(self):

        lottie_book = self.load_lottieurl(
            'https://assets10.lottiefiles.com/packages/lf20_i9mtrven.json')
        st_lottie(lottie_book, speed=1, height=200, key="initial")

        return None

    def hello_card():
        row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns(
            (.1, 2, .2, 1, .1))

        row0_1.title("Desafio Bornlogic")
        with row0_2:
            st.write('')

        row0_2.subheader(
            'A Web App by [Jeová Ramos](https://github.com/jeovaramos)')

        col1_spacer1, row1_1, row1_spacer2 = st.columns((3.0, 3.2, .1))

        col1_spacer1.markdown(
            "Oi, tudo bem? Este é o produto de dados, resultado da solução "
            "do desafio. Aqui estou trazendo os principais resultados. "
            "Não deixe de conferir o relatório completo neste [link]"
            "(https://docs.google.com/document/d/1-"
            "fdSSZdLONQsEqbWauxyfFhzOCtKa0i2Ru-Gi43Pzzc/edit?usp=sharing). "
            "Confira também o relatório de atividades e o repositório do "
            "projeto.")
        col1_spacer1.markdown(
            "If you want to keep in touch or just see other things "
            "I'm working in, please consider click in the link above "
            "with my name on it.")
        col1_spacer1.markdown(
            "**I hope you enjoy it.** Best regards.")

        return None
