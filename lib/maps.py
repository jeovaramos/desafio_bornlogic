import pandas as pd
import streamlit as st
import plotly.express as px
from plotly.graph_objs._figure import Figure


class Mapping:
    def __init__(self):
        pass

    def globe_figure(self, df: pd.DataFrame, variable: str = "Ladder score") -> Figure:
        variable = "Ladder score" if variable is None else variable
        df_mean = df.groupby(
            ['Country name']).mean([variable]).reset_index()

        fig = px.choropleth(
            df_mean, locations='Country name', locationmode="country names",
            color=variable, projection='orthographic',
            color_continuous_scale=px.colors.sequential.Viridis,
            title="Positive affect index",
        )

        return fig

    def mundi_figure(self, df: pd.DataFrame, variable: str) -> Figure:
        df_sorted = df.sort_values("year").reset_index()
        if variable == "Generosity":
            color_scale = px.colors.diverging.BrBG
            mid_point = 0

        else:
            color_scale = px.colors.sequential.Viridis
            mid_point = None

        fig = px.choropleth(
            df_sorted, locations='Country name', locationmode="country names",
            color=variable, animation_frame='year',
            color_continuous_scale=color_scale,
            color_continuous_midpoint=mid_point,
            # range_color=[0.4, 1],
            title=f'{variable.capitalize()} time evolution'
        )

        return fig


if __name__ == "__main__":
    pass
