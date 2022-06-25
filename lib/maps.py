import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
from plotly.graph_objs._figure import Figure
from lib.toolkit import DSToolKit
from typing import List

class Mapping:
    def __init__(self):
        self.toolkit = DSToolKit()

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

    @st.cache(allow_output_mutation=True)
    def get_df_average(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self.toolkit.rename_columns(df=df.copy())
        df_average = df.groupby(
            ["year", "regional_indicator"]
        ).median().sort_values("year").reset_index()

        return df_average

    def regional_average(self, df: pd.DataFrame) -> List[Figure]:
        df_average = self.get_df_average(df)

        figures = list()
        for var in ["positive_affect", "negative_affect"]:
            fig = self.regional_figure(df_average, var)
            figures.append(fig)

        return figures

    def regional_figure(self, df_average: pd.DataFrame, var: str) -> Figure:
        var_pretty = self.toolkit.snake_to_text(var)
        fig = px.line(
            df_average, x="year", y=var, markers=True,
            facet_col="regional_indicator",
            facet_col_wrap=5,
            title=f"Annual regional average of {var_pretty}")

        var_mean = df_average[var].mean()
        fig = fig.add_hline(
            y=var_mean, line_dash="dot",
            annotation_text="Global average",
            annotation_position="bottom right")

        fig = fig.add_vrect(
            x0=2019.5, x1=2020.5,
            annotation_text="Pandemic", annotation_position="top left",
            fillcolor="green", opacity=0.25, line_width=0)

        fig = fig.for_each_annotation(
            lambda a: a.update(text=a.text.split("=")[-1]))

        return fig

    def get_anomaly_metrics(
        self, df_average: pd.DataFrame, region: str, var: str,
        n_years: int = 5, std_thresh: float = 2.0
    ) -> dict:

        idx = -(n_years + 1)
        print(idx)

        point_2020 = df_average[
            df_average["regional_indicator"]
            == region][var].values[-1]
        mean_years = df_average[df_average[
            "regional_indicator"]
            == region][var].values[idx:-1].mean()
        std_5years = df_average[
            df_average["regional_indicator"]
            == region][var].values[idx:-1].std()

        anomaly = point_2020 - mean_years
        impact = np.abs(anomaly) > std_thresh * std_5years
        relative_anomaly = (point_2020 / mean_years) - 1

        results = {
            "Region": region, "Variable": var, "Anomaly": anomaly,
            "Relative Anomaly": relative_anomaly, "Impact": impact
        }
        return results

    def anomaly_data_frame(
        self, df: pd.DataFrame, n_years: int = 5, std_thresh: float = 2.0
    ) -> pd.DataFrame:

        df_average = self.get_df_average(df)
        anomaly_data = list()
        for region in df_average["regional_indicator"].unique():
            for var in ["positive_affect", "negative_affect"]:
                results = self.get_anomaly_metrics(
                    df_average, region, var, n_years, std_thresh)
                anomaly_data.append(results)

        return pd.DataFrame(anomaly_data).round(2)

    def plot_anomaly(
        self, df: pd.DataFrame,
        n_years: int = 5, std_thresh: float = 2.0
    ) -> Figure:

        df_anomaly = self.anomaly_data_frame(df, n_years, std_thresh)
        fig = px.bar(
            df_anomaly, x="Variable", y="Relative Anomaly", color="Impact",
            facet_col="Region",
            facet_col_wrap=5, range_y=(-0.3, 0.3),
            title=f"Last {n_years} years Relative Anomaly")

        fig = fig.for_each_annotation(
            lambda a: a.update(text=a.text.split("=")[-1]))

        return fig


if __name__ == "__main__":
    pass
