import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

def plot_validation_rate(df):
    df = df.sort_values("validation_rate", ascending=True)

    ax = df.plot(
        kind="barh",
        x="model",
        y="validation_rate",
        legend=False,
        color="#4e79a7",
        figsize=(8,6)
    )
    ax.set_xlabel("Validation rate")
    ax.set_ylabel("Model")
    ax.set_title("Validation rate per model")
    plt.xlim(0, 1)

    for i, v in enumerate(df["validation_rate"]):
        ax.text(v + 0.01, i, f"{v:.0%}", va="center")

    plt.tight_layout()
    plt.show()

def plot_failures(df, scale: int):
    failure_cols = [col for col in df.columns if col.endswith("_failure")]
    
    df_plot = df.set_index("model")[failure_cols]
    
    df_plot = df_plot.loc[:, (df_plot != 0).any(axis=0)]

    df_plot = df_plot[df_plot.sum().sort_values(ascending=False).index]

    ax = df_plot.plot(
        kind="bar",
        stacked=True,
        figsize=(10, 6)
    )

    plt.ylabel("Failure Value")
    plt.title("Failures by Model")
    plt.xticks(rotation=45, ha="right")
    plt.ylim(0, scale)
    plt.legend(title="Failure Type", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.show()