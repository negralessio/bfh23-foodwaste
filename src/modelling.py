import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

import xgboost as xgb

from sklearn.metrics import mean_squared_error, mean_absolute_error

import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')


def get_product_df(master_df: pd.DataFrame, id: int) -> pd.DataFrame:
    """ Gets for the product with input ID specified dataframe for training of the model

    :param master_df: pd.DataFrame -- Master df
    :param id: int -- Identification of the product (Artikelnummer)
    :return: pd.DataFrame -- For the product specified dataframe
    """
    return master_df[master_df.Artikelnummer == id]


def get_name_of_product_by_id(master_df: pd.DataFrame, id: int) -> str:
    """ Returns the name of the product given the ID

    :param master_df: pd.DataFrame -- Master df
    :param id: int -- Identification of the product (Artikelnummer)
    :return: str -- Name of the product specified by ID
    """
    return master_df[master_df["Artikelnummer"] == id]["Artikelbeschreibung"].values[0]


def visualize_product_df(product_df: pd.DataFrame) -> None:
    """ Plots line plot of the product df

    :param product_df: pd.DataFrame
    :return: None
    """
    # Get name of artikel
    name = product_df["Artikelbeschreibung"].values[0]
    id = product_df["Artikelnummer"].values[0]

    plt.figure(figsize=(15, 3))
    plt.title(f"{name} (ID: {id})", fontweight="bold", size=12)
    sns.lineplot(data=product_df, x="Kalendertag", y="Abschriften Menge")
    plt.show()


def prepare_df(product_df: pd.DataFrame, target: str = "Abschriften Menge") -> pd.DataFrame:
    """ Sets Kalendertag / date as index and drops all other columns except the target / label

    :param product_df: pd.DataFrame -- DataFrame containing only the data for one specific product
    :param target: str -- Name of the target / label
    :return: product_df: pd.DataFrame -- For Training prepared dataframe, contains only label as values and date as keys
    """
    # Set Kalendertag as index
    product_df = product_df.reset_index(drop=True)
    product_df.index = product_df.Kalendertag
    # Keep only target
    product_df = product_df[target]

    return pd.DataFrame(product_df)


def train_test_split(df: pd.DataFrame, last_k_percent = 0.1) -> tuple[pd.DataFrame, pd.DataFrame, int]:
    """ Differentiate between absolute or relative last k values. Then splits data based on that.

    :param df: pd.DataFrame -- Product specific df
    :param last_k_percent: float or int -- Number of test samples (last k)
    :return:
    """
    # Get total number of samples
    N = len(df)
    if isinstance(last_k_percent, float):
        # Get last k percent as absolute value
        k = int(N * last_k_percent)
    else:
        k = last_k_percent

    # Get first N-k values, e.g. first 250 values
    X_train = df.iloc[:(N-k), :]
    # Get last k values, e.g. last 50 values
    X_test = df.iloc[-k:, :]

    return X_train, X_test, k


def create_time_features(df):
    """ Create time features from date index

    :param df: pd.DataFrame -- Dataframe that has an date index
    :return: df: pd.DataFrame -- With time features populated df
    """
    df = df.copy()
    df['dayofmonth'] = df.index.day
    df['dayofweek'] = df.index.dayofweek
    df['quarter'] = df.index.quarter
    df['month'] = df.index.month
    df['year'] = df.index.year
    df['dayofyear'] = df.index.dayofyear

    return df


def get_features_and_labels(train_df, test_df, target: str = "Abschriften Menge") -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """ Returns feature matrix and labels for train and test splits

    :param train_df: pd.DataFrame -- Train dataframe
    :param test_df: pd.DataFrame -- Test Dataframe
    :param target: str -- Label name
    :return:
        X_train: pd.DataFrame -- Feature Matrix of Train Data
        y_train: pd.DataFrame -- Label vector of Train Data
        X_test: pd.DataFrame -- Feature Matrix of Test Data
        y_test: pd.DataFrame -- Label vector of Test Data
    """
    X_train = train_df.drop(target, axis =1)
    y_train = pd.DataFrame(train_df[target])

    X_test = test_df.drop(target, axis =1)
    y_test = pd.DataFrame(test_df[target])

    return X_train, y_train, X_test, y_test


def make_prediction(X_test, regressor, target: str = "Abschriften Menge", verbosity: int = 1) -> pd.DataFrame:
    """ Makes prediction given the fitted model object and Test data

    :param X_test: pd.DataFrame -- Test Data
    :param regressor: Fitted Model object, e.g. XGBRegressor
    :param target: str -- Label name
    :param verbosity: int -- Level of verbosity
    :return: pd.DataFrame -- y_pred, i.e. prediction
    """
    if verbosity > 0:
        print("Making predictions ...")

    # Make prediction
    y_pred = regressor.predict(X_test)
    # Convert to dataframe with index / dates from input features X_test
    y_pred = pd.DataFrame(y_pred, index=X_test.index, columns=[target])
    return y_pred


def concat_data_with_prediction(y_train: pd.DataFrame, y_pred: pd.DataFrame) -> pd.DataFrame:
    """ Adds flags to provided y_train and y_pred dataframes and concatenates them on axis 0, i.e. stacks the vertically.

    :param y_train: pd.DataFrame -- Dataframe containing the y_train
    :param y_pred: pd.DataFrame -- Dataframe containing the y_pred
    :return: df_concat: pd.DataFrame -- Concatenated Dataframe with flag column
    """
    y_train["flag"] = "train"
    y_pred["flag"] = "test"

    df_concat = pd.concat([y_train, y_pred], axis=0)
    return df_concat


def visualize_predictions(df_concat, test_df, product_name, mse, mae, target: str = "Abschriften Menge") -> None:
    """ Visualizes prediction and highlights train and test samples

    :param df_concat: pd.DataFrame -- Concatenated train and test data with flags
    :param test_df: pd.DataFrame -- Dataframe of test data
    :param product_name: str -- Name of the product
    :param mse: np.array -- Mean Squared Error
    :param mae: np.array -- Mean Absolute Error
    :param target: str -- Name of the target / label
    :return:
    """
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15,3))
    ax.set_title(f"Predicted food waste for Product '{product_name}' (MSE = {mse:.2f}, MAE = {mae:.2f})", fontweight="bold", size=14)
    sns.lineplot(data=df_concat, x="Kalendertag", y=target, hue="flag", ax=ax)
    sns.lineplot(data=test_df, x="Kalendertag", y=target, color="black", ax=ax, label="true", alpha=0.8, linestyle="--")
    plt.show()


def prepare_inference_sample(TEST_DATE: str) -> pd.DataFrame:
    """ Puts input Date into right format that model expects

    :param TEST_DATE: str -- Test date
    :return: test_sample: pd.DataFrame -- Dataframe ready to feed to the model
    """
    test_sample = pd.DataFrame({"date": pd.date_range(start=TEST_DATE, end=TEST_DATE)})
    test_sample.index = test_sample["date"]
    test_sample = create_time_features(test_sample)
    test_sample.drop("date", axis=1, inplace=True)
    return test_sample

def train_and_inference(master_df: pd.DataFrame, ids: list, date: str, test_split_size = 0.1,
                        plot_results: bool = False, verbosity: int = 1) -> dict:
    # Make predictions
    predictions: dict = {}

    for id in set(ids):
        # Get Train data of the product specified by ID and do minor preprocessing
        product_name = get_name_of_product_by_id(master_df=master_df, id=id)
        product_df = get_product_df(master_df=master_df, id=id)
        product_df = prepare_df(product_df)

        # Perform train test split on specified dataframe
        train_df, test_df, k = train_test_split(product_df, last_k_percent=test_split_size)
        train_df = create_time_features(train_df)
        test_df = create_time_features(test_df)

        # Get Features and Labels of Train and Test
        X_train, y_train, X_test, y_test = get_features_and_labels(train_df, test_df)

        if verbosity > 0:
            print(f"Making prediction for '{product_name}' ...")

        # Fit Model
        reg = xgb.XGBRegressor(n_estimators=1000)
        reg.fit(X_train, y_train, verbose = False)

        # Get y_pred
        y_pred: pd.DataFrame = make_prediction(X_test, regressor=reg, verbosity=0)
        # Evaluate
        mse = mean_squared_error(y_true=y_test, y_pred=y_pred)
        mae = mean_absolute_error(y_true=y_test, y_pred=y_pred)

        # Inference Sample Test
        test_sample = prepare_inference_sample(date)
        y_pred_sample = reg.predict(test_sample)

        if plot_results:
            # Concat results for plotting
            df_concat = concat_data_with_prediction(y_train=y_train, y_pred=y_pred)
            visualize_predictions(df_concat, test_df, product_name, mse, mae)

        predictions[id] = {"Name": product_name,
                           "ID": id,
                           "Fitted-XGBR": reg,
                           "Test MSE":mse,
                           "Test MAE": mae,
                           "Test Size": k,
                           "Prediction-Date": date,
                           "Prediction": np.float32(y_pred_sample)}

    return predictions




