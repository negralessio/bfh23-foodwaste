""" Module handles utility functions """
import yaml
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def load_config(config_path) -> dict:
    """
    Loads a YAML configuration file.

    :param config_path: Path to the configuration file
    :type config_path: str

    :return: Configuration dictionary
    :rtype: dict
    """
    try:
        with open(config_path, "r") as ymlfile:
            return yaml.load(ymlfile, yaml.FullLoader)
    except FileNotFoundError:
        raise FileNotFoundError(f"File {config_path} not found!")
    except PermissionError:
        raise PermissionError(f"Insufficient permission to read {config_path}!")
    except IsADirectoryError:
        raise IsADirectoryError(f"{config_path} is a directory!")


def plot_top_k_foodwasters(top_k: int, top_k_foodwasters_df: pd.DataFrame, top_k_foodwasters: pd.Series):
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 5))
    fig.suptitle(f"Analysis of the Top {top_k} Foodwaster", fontweight="bold", size=16)
    sns.boxplot(data=top_k_foodwasters_df, x="Abschriften Menge", y="Artikelbeschreibung", hue="Artikelbeschreibung",
                ax=axes[0])
    axes[0].set_title("Distribution of the Top 10 Foodwasters")
    g = sns.barplot(data=pd.DataFrame(top_k_foodwasters), x="Abschriften Menge", y="Artikelbeschreibung", ax=axes[1],
                    edgecolor="black")
    g.bar_label(g.containers[0], padding=-25)
    axes[1].set_title("Sum of wasted amount of the Top 10 Foodwasters")
    fig.tight_layout()
    plt.show()