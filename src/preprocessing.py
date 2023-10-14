import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt

def clean_df(df) -> pd.DataFrame:
    """ Simple function that corrects the data.
    Function cleans dataframe using the following functions:
        - Flip values from negative to positive
        - Set negative values to 0

    :param df: pd.DataFrame -- DataFrame to clean
    :return: df: pd.DataFrame -- Cleaned Datafream
    """
    # Convert to positive numbers
    df["Abschriften Menge"] = df["Abschriften Menge"] * (-1)
    # Replace negative Values with 0
    df["Abschriften Menge"] = df["Abschriften Menge"].apply(lambda x : x if x > 0 else 0.0)

    return df

def get_top_k_foodwasters(df: pd.DataFrame, k: int = 20) -> pd.Series:
    """ Gets the top 5 foodwaster based on total sum of wasted units

    :param df: pd.DataFrame -- Master df to analyse
    :param k: int -- Number of top k items to keep
    :return: pd.Series -- Series with Key = Names and Values = Sum of total wasted units
    """
    return df[["Artikelbeschreibung", "Abschriften Menge"]].groupby("Artikelbeschreibung").sum().sort_values(by="Abschriften Menge", ascending=False)[:k]

def plot_top_k_foodwaster(TOP_K_FOODWASTERS: int, top_k_foodwasters_df: pd.DataFrame, top_k_foodwasters: pd.Series):
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 5))
    fig.suptitle(f"Analysis of the Top {TOP_K_FOODWASTERS} Foodwaster", fontweight="bold", size=16)
    sns.boxplot(data=top_k_foodwasters_df, x="Abschriften Menge", y="Artikelbeschreibung", hue="Artikelbeschreibung",
                ax=axes[0])
    axes[0].set_title("Distribution of the Top 10 Foodwasters")
    g = sns.barplot(data=pd.DataFrame(top_k_foodwasters), x="Abschriften Menge", y="Artikelbeschreibung", ax=axes[1],
                    edgecolor="black")
    g.bar_label(g.containers[0], padding=-25)
    axes[1].set_title("Sum of wasted amount of the Top 10 Foodwasters")
    fig.tight_layout()
    plt.show()