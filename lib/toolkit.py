import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import pymc3 as pymc


PXChart = px._chart_types


def numerical_description(numerical: pd.DataFrame) -> pd.DataFrame:
    description = numerical.describe().T
    description['range'] = description['max'] - description['min']
    description['skew'] = numerical.skew()
    description['kurtosis'] = numerical.kurtosis()

    return description


def plot_histogram(data: pd.DataFrame, column: str) -> None:
    fig = px.histogram(data, x=column)
    fig = fig.update_layout(
        title_text=f'{snake_to_text(column)} histogram',
        xaxis_title_text='Value',
        yaxis_title_text='Count')
    fig.show()


def plot_xy(data: pd.DataFrame, x_axis: str, y_axis: str, plot_type: PXChart) -> None:
    fig = plot_type(data, x=x_axis, y=y_axis)
    fig = fig.update_layout(
        title_text=f'{snake_to_text(y_axis)}',
        xaxis_title_text=snake_to_text(x_axis),
        yaxis_title_text='Value')
    fig.show()


def snake_to_text(string: str) -> str:
    return string.capitalize().replace("_", " ")


def get_region(data: pd.DataFrame, country: str) -> str:
    try:
        region = data[data["country_name"] ==
                      country]["regional_indicator"].values[0]
    except IndexError:
        region = "NOT_DEFINED"

    return region


def plot_comparison(trace: pymc.backends.base.MultiTrace, title: str, len_data: int) -> None:
    plt.figure(figsize=(5, 5))
    plt.suptitle(title)

    plt.subplot(311)
    plt.hist(trace["lambda_1"], histtype="stepfilled", bins=30, density=True)
    plt.xlim([0, 3])

    plt.subplot(312)
    plt.hist(trace["lambda_2"], histtype="stepfilled", bins=30, density=True)
    plt.xlim([0, 3])

    plt.subplot(313)
    weights = 1.0 / len(trace['tau']) * np.ones_like(trace['tau'])
    plt.hist(trace["tau"], histtype="stepfilled",
             bins=len_data, weights=weights, rwidth=2.)
    plt.xlim([0, len_data])
    plt.ylim([0, 1.0])

    plt.show()


def bayesian_inference(df_average: pd.DataFrame, region: str, variable: str) -> pymc.backends.base.MultiTrace:
    df_regional = df_average[df_average["regional_indicator"] == region]

    response_variable = df_regional[variable].values.ravel()
    len_data = len(response_variable)
    with pymc.Model():

        # Prior
        alpha = 1.0 / response_variable.mean()
        lambda_1 = pymc.Exponential("lambda_1", alpha)
        lambda_2 = pymc.Exponential("lambda_2", alpha)

        tau = pymc.DiscreteUniform("tau", lower=0, upper=len_data - 1)

        # Posterior
        idx = np.arange(len_data)
        lambda_ = pymc.math.switch(tau > idx, lambda_1, lambda_2)
        _ = pymc.Poisson("obs", lambda_, observed=response_variable)

        # Likelihood
        trace = pymc.sample(
            draws=10_000, tune=5_000, step=pymc.Metropolis(),
            return_inferencedata=False)

        return trace, len_data


if __name__ == "__main__":
    pass