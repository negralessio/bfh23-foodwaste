import os

import numpy as np
import pandas as pd
import streamlit as stm
import time

stm.set_page_config(page_title="EDEKA - Wir lieben Lebensmittel", page_icon="assets/favicon.png", layout="wide")

# Custom CSS
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
stm.markdown(hide_streamlit_style, unsafe_allow_html=True)
background_image_style = """
            <style>
            [data-testid=stSidebar] {
                background-image: url("https://www.edeka.de/edeka-ui-assets/images/bg-dark.jpg");
                background-size: cover;
            }
            </style>
            """
stm.markdown(background_image_style, unsafe_allow_html=True)

# Configure the sidebar
with stm.sidebar:
    stm.image("assets/claim-grunge-650.png", use_column_width=True)
    stm.text("Made with ❤️ by DataPilots")
stm.markdown(
        f"""
        <style>
            [data-testid="stSidebarNav"] {{
                background-image: url("https://i.imgur.com/mPqEtdf.png");
                background-repeat: no-repeat;
                padding-top: {75 - 40}px;
                background-position: 20px 20px;
                background-size: 88%;
            }}
        </style>
        """,
        unsafe_allow_html=True,)

# Main content

# Import .csv to DataFrames
weather_file = 'weather.csv'
football_file = 'football.csv'
feiertage_file = 'feiertage.csv'
holidays_file = 'holidays.csv'
forecast_file = 'forecast.csv'

if os.path.exists("data/gui/" + weather_file):
    weather_df = pd.read_csv("data/gui/" + weather_file)
if os.path.exists("data/gui/" + football_file):
    football_df = pd.read_csv("data/gui/" + football_file)
if os.path.exists("data/gui/" + feiertage_file):
    feiertage_df = pd.read_csv("data/gui/" + feiertage_file)
if os.path.exists("data/gui/" + holidays_file):
    holidays_df = pd.read_csv("data/gui/" + holidays_file)
if os.path.exists("data/gui/" + forecast_file):
    forecast_df = pd.read_csv("data/gui/" + forecast_file)
    forecast_df['ID'] = forecast_df['ID'].astype(str)
    forecast_df['Prediction'] = np.ceil(forecast_df['Prediction'])
    # DataFrame Reihenfolge ändern
    forecast_df = forecast_df[['Prediction-Date', 'ID', 'Name', 'Prediction']]

# Tabelle erstellen, falls Forecast vorhanden
if os.path.exists("data/gui/" + forecast_file):
    stm.dataframe(forecast_df, use_container_width=True)
else:
    stm.write("Bitte zuerst Forecast erzeugen lassen!")

