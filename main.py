import pandas as pd

import src.data_loader as data_loader
import src.preprocessing as preprocessing
import src.modelling as modelling
import src.utils as utils

# Global constants
_DATA_PATH = "data/raw/ABSCHRIFTEN14102023125147047.xlsx"


def main(IDs: list, date: str, date2:str, refit_model: bool = True, plot_foodwasters: bool = False, top_k=None, verbosity = 1):
    """ Main pipeline executing the train process and inference

    First loads master_df from data/raw. Then does some preprocessing on the data, e.g. flipping values, replacing values.
    Optionally plots the results of the top k food wasters (not actually part of the ML Pipeline).
    Model than trains on train and evaluates und test split. Afterward, does refitting on whole training and predicts
    for the input time range specified by [date, date2] (if refit_model == True).
    Main pipeline returns then the details about the ML Run for each ID / Product.

    :param IDs: list -- List of Product IDs (Artikelnummer), e.g. [794366005]
    :param date: str -- First interval bound of date prediction, e.g. "2021-04-16"
    :param date2: -- Last interval bound of date prediction, e.g. "2021-04-19"
    :param refit_model: bool -- Whether to refit model after evaluation on 100% Train data (default: True)
    :param plot_foodwasters: bool -- Whether to plot the top k food wasters
    :param top_k: bool -- Number of top k food wasters to show / Analyse, e.g. k = 20
    :param verbosity: int -- Level of verbosity (default: 1)
    :return: predictions: dict[dict] -- Dictionary of dicts with ID as key and run details as Values
    """
    # Read Data
    df = data_loader.read_data(_DATA_PATH)

    # Preprocess raw data
    df = preprocessing.clean_df(df)

    # Optional: Not Relevant for Pipeline
    if plot_foodwasters:
        assert top_k is not None, "ERROR: Input param 'top_k' must be an integer!"
        # Get data about top k foodwasters and plot them
        top_k_foodwasters_df, top_k_foodwasters, top_k = analyze_top_k_foodwasters(master_df=df, top_k=top_k)
        utils.plot_top_k_foodwasters(top_k, top_k_foodwasters_df, top_k_foodwasters)

    # Train model for the given IDs and to point estimate given by date
    predictions = modelling.train_and_inference(master_df=df, ids=IDs, date=date, date2=date2,
                                                test_split_size=0.1, refit_model=refit_model,
                                                plot_results=False, verbosity=verbosity)

    return predictions


def analyze_top_k_foodwasters(master_df: pd.DataFrame, top_k: int) -> tuple[pd.DataFrame, pd.Series, int]:
    """ Plots top k foodwaster distribution and barplot (sum)

    :param master_df: pd.DataFrame -- Master df, i.e. data/raw/...
    :param top_k: int -- Number of top k foodwasters to plot
    :return:
        top_k_foodwasters_df: pd.DataFrame -- Dataframe of the top k food wasters
        top_k_foodwasters: pd.Series -- Aggregation (sum) of top k food wasters
        top_k: int -- Number of k foodwasters that has been analyzed
    """
    # Get top k foodwasters with key (Artikelbeschreibung) and as value the sum of 'Abschriften Menge'
    top_k_foodwasters: pd.Series = preprocessing.get_top_k_foodwasters(master_df, k=top_k)
    # Get list of Artikelbeschreibung of the top k foodwasters
    top_k_foodwasters_list = list(top_k_foodwasters.index)
    # Get df of the top k foodwasters
    top_k_foodwasters_df = master_df[master_df["Artikelbeschreibung"].isin(top_k_foodwasters_list)]

    return top_k_foodwasters_df, top_k_foodwasters, top_k


if __name__ == "__main__":
    predictions = main(IDs=[794366005], date="2021-04-16", date2="2021-04-18", refit_model=True, plot_foodwasters=False, top_k=None)
    print(predictions)
