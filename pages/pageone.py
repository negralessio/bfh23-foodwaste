import streamlit as stm
from streamlit_extras.app_logo import add_logo
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
add_logo("assets/edeka_logo.png", height=200)


# Main content
stm.title("Starte deinen Planungsprozess")

tab1, tab2, tab3 = stm.tabs(["Allgemein", "Parameter", "Sonstiges"])
with tab1:
    pass
with tab2:
    with stm.container():
        col1, col2 = stm.columns(2)
        with col1:
            stm.header("Parameter")
            stm.markdown("Wähle die Parameter aus, die für deine Planung relevant sind. Die Relevanz kannst du hierbei "
                         "mit dem Slider einstellen.")
        with col2:
            stm.header("Beschreibung")
            stm.markdown("Hier kannst du nachlesen, wieso diese Parameter relevant sein könnten.")

    # Einzelne Parameter Selektion
    with stm.container():
        col1, col2 = stm.columns(2)
        with col1:
            weather = stm.toggle('Wetter', value=False)
            if weather:
                weather_weight = stm.slider('Relevanz des Wetters - 1 = unwichtig, 10 = sehr wichtig', 1, 10, 5, 1)
        with col2:
            stm.caption("Wetter")
            stm.markdown("Hat das Wetter hat einen Einfluss auf das Kaufverhalten der Kunden?")
    with stm.container():
        col1, col2 = stm.columns(2)
        with col1:
            football = stm.toggle('Fussballspiele', value=False)
            if football:
                club = stm.text_input('Fussballverein', '')
                if club != '':
                    stm.toast('Eingabe erfolgreich!', icon='😍')
                football_weight = stm.slider('Relevanz von Fussball', 1, 10, 5, 1)
        with col2:
            stm.caption("Fussballspiele")
            stm.markdown("Gibt es relevante Fussballspiele in der Nähe, weshalb ein vergroessertes Kundenaufkommen geschieht?")
    with stm.container():
        col1, col2 = stm.columns(2)

        with col1:
            feiertage = stm.toggle('Feiertage', value=False)
            if feiertage:
                feiertage_weight = stm.slider('Relevanz der Feiertage - 1 = unwichtig, 10 = sehr wichtig', 1, 10, 5, 1)
        with col2:
            stm.caption("Feiertage")
            stm.markdown("Hat die Bäckerei an einem Feiertag geöffnet und beinflusst dies das Kaufverhalten?")
            # Warum Feiertage sehr relevant sein koennen: Bäckerei hat an Feiertagen geöffnet, wo andere ggf.
            # geschlossen haben. Wichtig ist dabei, dass bspw. in BW oder BY Bäckereien maximal 3h geöffnet haben
            # dürfen.
    with stm.container():
        col1, col2 = stm.columns(2)

        with col1:
            holidays = stm.toggle('Ferien', value=False)
            if holidays:
                holidays_weight = stm.slider('Relevanz der Feiertage - 1 = unwichtig, 10 = sehr wichtig', 1, 10, 5, 1)
        with col2:
            stm.caption("Ferien")
            stm.markdown("Wird das Kaufverhalten der Kunden durch Sschulferien beinflusst? Beispiel: Bäckerei liegt "
                         "benachbart zu einer Schule.")




if stm.button(":bread: Generate"):
    with stm.status("Downloading data...", expanded=True) as status:
        stm.write("Searching for data...")
        time.sleep(2)
        stm.write("Found URL.")
        time.sleep(1)
        stm.write("Downloading data...")
        time.sleep(1)
        status.update(label=":100: Data Generated", state="complete", expanded=False)
