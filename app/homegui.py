import streamlit as stm
from streamlit_extras.app_logo import add_logo

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