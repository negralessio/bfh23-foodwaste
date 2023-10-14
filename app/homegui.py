import streamlit as stm
from streamlit_extras.app_logo import add_logo

# Hide the default footer and set Basic Settings
stm.set_page_config(page_title="Edeka Suedwest", page_icon="🍎", layout="wide")
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
stm.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Configure the sidebar
stm.sidebar.title("Navigation")
add_logo("assets/edeka_logo.png", height=200)

stm.title("This is the Home Page")