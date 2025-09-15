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