import pandas as pd

def read_data(path) -> pd.DataFrame:
    """ Reads Excel file to pd.DataFrame

    :param path: str -- Path to the data
    :return: df: pd.DataFrame -- Read Dataframe
    """
    # Read excel file and specify column names
    df = pd.read_excel(path, names=["Kalendertag", "Artikelnummer", "Artikelbeschreibung", "GTIN", "Abschriften Menge"])
    # Convert date column to date type
    df["Kalendertag"] = pd.to_datetime(df["Kalendertag"], dayfirst="True")
    return df
