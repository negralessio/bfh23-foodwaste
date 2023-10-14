
import pandas as pd

import src.data_loader as data_loader
import src.preprocessing as preprocessing
import src.modelling as modelling
import src.utils as utils


# Global constants
_DATA_PATH = "data/raw/ABSCHRIFTEN14102023125147047.xlsx"

def main(IDs: list, date: str, plot_foodwasters: bool = False, top_k_foodwasters = None):
    # Read Data
    df = data_loader.read_data(_DATA_PATH)

    # Preprocess raw data
    df = preprocessing.clean_df(df)

    # Optional: Not Relevant for Pipeline
    if plot_foodwasters:
        top_k_foodwasters_df, top_k_foodwasters, top_k = analyze_top_k_foodwasters(master_df=df, top_k=top_k_foodwasters)
        utils.plot_top_k_foodwasters(top_k, top_k_foodwasters_df, top_k_foodwasters)

    # Train model for the given IDs and to point estimate given by date
    predictions = modelling.train_and_inference(master_df = df, ids=IDs, date=date,
                                                test_split_size=0.1, plot_results=False, verbosity=1)

    print(predictions)


def analyze_top_k_foodwasters(master_df: pd.DataFrame, top_k: int):
    # Get top k foodwasters with key (Artikelbeschreibung) and as value the sum of 'Abschriften Menge'
    top_k_foodwasters: pd.Series = preprocessing.get_top_k_foodwasters(master_df, k=top_k)
    # Get list of Artikelbeschreibung of the top k foodwaster
    top_k_foodwasters_list = list(top_k_foodwasters.index)
    # Get df of the top k foodwasters
    top_k_foodwasters_df = master_df[master_df["Artikelbeschreibung"].isin(top_k_foodwasters_list)]

    return top_k_foodwasters_df, top_k_foodwasters, top_k


if __name__ == "__main__":
    main(IDs=[794366005], date="2021-03-15", plot_foodwasters=False, top_k_foodwasters=10)