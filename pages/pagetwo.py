import pandas as pd
import random
import streamlit as stm
from streamlit_extras.app_logo import add_logo

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
            .st-emotion-cache-6qob1r {
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
add_logo("assets/edeka_logo.png", height=200)

# Rankingpage
stm.title("Graph")

# Ranking-Graph
# read csv data
top_20_wasted_food = pd.read_csv('data/processed/top20_foodwasters.csv', sep=',')
top_20_wasted_food_tpl = [tuple(x) for x in top_20_wasted_food.values]
df = pd.DataFrame(
    {
        "name": [top_20_wasted_food_tpl[i][0] for i in range(len(top_20_wasted_food_tpl))],
        "waste": [top_20_wasted_food_tpl[i][1] for i in range(len(top_20_wasted_food_tpl))],
        "views_history": [[random.randint(0, 5000) for _ in range(30)] for _ in range(len(top_20_wasted_food_tpl))],
    }
)
stm.dataframe(
    df,
    column_config={
        "name": "App name",
        "wast": "Wasted food in €",
        "views_history": stm.column_config.LineChartColumn(
            "Views (past 30 days)", y_min=0, y_max=5000
        ),
    },
    hide_index=True,
)

