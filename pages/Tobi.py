import streamlit as stm
import pandas as pd

from streamlit_extras.app_logo import add_logo
from datetime import timedelta, date

stm.set_page_config(page_title="EDEKA - Wir lieben Lebensmittel", page_icon="assets/favicon.png", layout="wide")

#Custom CSS
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
add_logo("assets/edeka_logo.png", height=200)


stm.title("This is the Home Page")

# Calender
day_of_prediction = stm.date_input("Which day do you like to predict?", value=date.today())
if day_of_prediction > (date.today() + timedelta(days=5)):
    stm.write("Day is to far in futur!")

# import product range csv
raw_product_range = pd.read_csv('data/products_unique.csv', sep=',')
products_lst_tp = [tuple(x) for x in raw_product_range.values]
product_range = {}
for tpl in products_lst_tp:
    product_range[tpl[1]] = tpl[2]

# show prediction
else:
    # Searchbox
    options = stm.multiselect(
        'Which product do you want to predict?',
        [i for i in product_range.keys()] + [j for j in product_range.values()]
    )

    if stm.button('compute'):
        # run pipeline
        products_to_predict = [int]
        for i in options:
            if i in product_range.keys():
                products_to_predict += [product_range[i]]
            elif i in product_range.values():
                products_to_predict += [i]
        if len(options) == 0:
            products_to_predict = [i for i in product_range.values()]

        # send products_to_predict and day_of_prediction

        # get data from pipeline
        predicted_data = pd.read_csv('data/prediction/example_prediction.csv', sep=',')
        prediction = [tuple(x) for x in predicted_data.values]

        # dynamic table
        @stm.cache_data
        def load_data():
            return pd.DataFrame(
                {
                    "Date": [prediction[i][0] for i in range(len(prediction))],
                    "Number of product": [str(prediction[i][1]) for i in range(len(prediction))],
                    "Name": [prediction[i][2]for i in range(len(prediction))],
                    "prediction": [prediction[i][3] for i in range(len(prediction))]
                }
            )
        stm.dataframe(load_data(), use_container_width=True)

