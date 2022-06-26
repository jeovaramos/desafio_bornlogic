import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn import decomposition, ensemble, preprocessing
from sklearn.manifold import TSNE

PXChart = px._chart_types


class DSToolKit:
    def __init__(self) -> None:
        self.reducer = TSNE(random_state=42, n_jobs=-1)

    @st.cache(allow_output_mutation=True, suppress_st_warning=True)
    def load_datasets(self):
        data_metrics = pd.read_excel("data/Data_2021.xls")
        data_historic = pd.read_excel("data/Historic_data.xls")

        data_historic = self.fill_na_historic(data_historic)
        data_historic = self.create_regional_column(
            data_historic, data_metrics
        )
        data_historic = self.filter_historic(data_historic)

        return data_metrics, data_historic

    def snake_to_text(self, string: str) -> str:
        return string.capitalize().replace("_", " ")

    def rename_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        df.columns = [name.lower().replace(" ", "_") for name in df.columns]

        return df

    def fill_na_historic(self, df: pd.DataFrame) -> pd.DataFrame:
        for column in df.columns[1:]:
            df[column].fillna(df[column].median(), inplace=True)

        return df

    def get_region(self, df_metrics: pd.DataFrame, country: str) -> str:
        try:
            region = df_metrics[df_metrics["Country name"] == country][
                "Regional indicator"
            ].values[0]

        except IndexError:
            region = "NOT_DEFINED"

        return region

    def create_regional_column(
        self, df_historic: pd.DataFrame, df_metrics: pd.DataFrame
    ) -> pd.DataFrame:

        regional_column = list()
        for ii in range(len(df_historic)):
            country = df_historic["Country name"][ii]
            region = self.get_region(df_metrics, country)

            regional_column.append(region)

        df_historic["Regional indicator"] = regional_column

        return df_historic

    def filter_historic(self, df: pd.DataFrame) -> pd.DataFrame:
        return df[df["Regional indicator"] != "NOT_DEFINED"]

    def data_preparation(self, df: pd.DataFrame) -> pd.DataFrame:
        mm = preprocessing.MinMaxScaler()

        for variable in df.columns[1:-1]:  # Numerical columns
            df[variable] = mm.fit_transform(df[[variable]])

        df["regional_indicator"] = preprocessing.LabelEncoder().fit_transform(
            df[["regional_indicator"]].values.ravel()
        )

        return df

    def run_pca(self, df_prep: pd.DataFrame) -> pd.DataFrame:
        df_prep = self.data_preparation(df_prep.copy())
        X = df_prep.drop(columns=["regional_indicator"], axis=1)

        pca = decomposition.PCA(n_components=X.shape[1])
        principal_components = pca.fit_transform(X)

        # pca component
        return pd.DataFrame(principal_components)

    def run_forest(self, df_prep: pd.DataFrame) -> pd.DataFrame:
        df_prep = self.data_preparation(df_prep.copy())
        X = df_prep.drop(columns=["regional_indicator"], axis=1)
        y = df_prep["regional_indicator"]

        rf_model = ensemble.RandomForestRegressor(
            n_estimators=100, random_state=42
        )
        rf_model.fit(X, y)

        # leaf embedding space
        return pd.DataFrame(rf_model.apply(X))

    @st.cache(allow_output_mutation=True, suppress_st_warning=True)
    def plot_embedding(self, name: str) -> pd.DataFrame:

        df_tsne = pd.read_csv(f"data/{name}.csv")

        fig = px.scatter(
            df_tsne,
            x="embedding_x",
            y="embedding_y",
            color="regional_indicator",
            title="[METRICS] PCA Embedding Space",
        )

        return fig

    def tsne_reduction(
        self, df_to_reduce: pd.DataFrame, df: pd.DataFrame
    ) -> pd.DataFrame:

        embedding = self.reducer.fit_transform(df_to_reduce)

        df_tsne = pd.DataFrame()
        df_tsne["regional_indicator"] = df["regional_indicator"]
        df_tsne["embedding_x"] = embedding[:, 0]
        df_tsne["embedding_y"] = embedding[:, 1]

        return df_tsne


if __name__ == "__main__":
    pass
