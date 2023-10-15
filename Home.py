import streamlit as stm
from streamlit_extras.app_logo import add_logo
import time
from datetime import timedelta, date
import datetime
from api.api_handler import APIHandler
import pandas as pd
import os
from main import main
import webbrowser

api = APIHandler()

stm.set_page_config(page_title="EDEKA - Wir lieben Lebensmittel", page_icon="assets/favicon.png", layout="wide")
club = ''

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
#add_logo("assets/logoFinalInvert_200.png", height=75)
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
stm.title("Starte deinen Planungsprozess")


tab1, tab2, tab3 = stm.tabs(["Allgemein", "Parameter", "Sonstiges"])
with tab1:
    with stm.container():
        col1, col2 = stm.columns(2)
        with col1:
            # Calender
            # day_of_prediction = stm.date_input("Which day do you like to predict?", value=date.today())
            time_range = stm.date_input("Welchen Zeitraum willst du vorhergesagt bekommen?",
                                        (datetime.datetime.strptime("2021/04/15", '%Y/%m/%d'),datetime.datetime.strptime("2021/04/15", '%Y/%m/%d')),
                                        datetime.datetime.strptime("2021/04/15", '%Y/%m/%d'),
                                        datetime.datetime.strptime("2021/04/20", '%Y/%m/%d'), format="DD.MM.YYYY")
            # if day_of_prediction > (date.today() + timedelta(days=5)):
            #    stm.write("Day is to far in futur!")
            if len(time_range) == 2:
                date_str1 = time_range[0].strftime("%Y-%m-%d")
                date_str2 = time_range[1].strftime("%Y-%m-%d")
                print(date_str1, date_str2)
        with col2:
            plz = stm.text_input('Postleitzahl', '77652')
            city, state, state_code = api.get_data_from_PostcodeAPI(plz)
            stm.write("Stadt: {}, Bundesland: {} ({})".format(city, state, state_code))
            print(city, state)

        # import product range csv
        raw_product_range = pd.read_csv('data/gui/artikelnummer_produkt.csv', sep=',')
        products_lst_tp = [tuple(x) for x in raw_product_range.values]
        product_range = {}
        for tpl in products_lst_tp:
            product_range[tpl[2]] = tpl[1]

        options = stm.multiselect(
            'Für welches Produkt soll ein Forecast erstellt werden?',
            [i for i in product_range.keys()] + [j for j in product_range.values()]
        )

    # Calender

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
            weather_toggle = stm.toggle('Wetter', value=False)
            if weather_toggle :
                weather_weight = stm.slider('Relevanz des Wetters - 1 = unwichtig, 10 = sehr wichtig', 1, 10, 5, 1)
        with col2:
            stm.caption("Wetter")
            stm.markdown("Hat das Wetter hat einen Einfluss auf das Kaufverhalten der Kunden?")
    with stm.container():
        col1, col2 = stm.columns(2)
        with col1:
            football_toggle  = stm.toggle('Fussballspiele', value=False)
            if football_toggle :
                club = stm.text_input('Fussballverein', '')
                if club != '':
                    stm.toast('Eingabe erfolgreich!', icon='😍')
                football_weight = stm.slider('Relevanz von Fussball', 1, 10, 5, 1)
        with col2:
            stm.caption("Fussballspiele")
            stm.markdown(
                "Gibt es relevante Fussballspiele in der Nähe, weshalb ein vergroessertes Kundenaufkommen geschieht?")
    with stm.container():
        col1, col2 = stm.columns(2)

        with col1:
            feiertage_toggle = stm.toggle('Feiertage', value=False)
            if feiertage_toggle:
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
            holidays_toggle = stm.toggle('Ferien', value=False)
            if holidays_toggle:
                holidays_weight = stm.slider('Relevanz der Ferien - 1 = unwichtig, 10 = sehr wichtig', 1, 10, 5, 1)
        with col2:
            stm.caption("Ferien")
            stm.markdown("Wird das Kaufverhalten der Kunden durch Sschulferien beinflusst? Beispiel: Bäckerei liegt "
                         "benachbart zu einer Schule.")

if stm.button(":bread: Erzeugen",key="button1"):
    with stm.status("Analyzing Data ...", expanded=True) as status:
        if plz == '':
            stm.toast("Bitte PLZ eingeben")
            stm.stop()
        if club == '' and football_toggle:
            stm.toast("Bitte Fussballverein eingeben")
            stm.stop()
        stm.write("Herunterladen der Parameter Daten :hourglass_flowing_sand:")
        time.sleep(2)
        if weather_toggle:
            weather = api.get_data_from_WeatherAPI_History(plz, date_str1, date_str2)
            print(weather)
        if football_toggle:
            football = api.get_data_from_OpenLigaDB(club, 0, 1)
            print(football)
        if feiertage_toggle:
            feiertage = api.get_data_from_FeiertageAPI(2021, state)
            print(feiertage)
        if holidays_toggle:
            holidays = api.get_data_from_FerienAPI(state_code, 2021)
            print(holidays)
        stm.write("Speichere Parameter Daten :floppy_disk:")
        weather_file = 'weather.csv'
        football_file = 'football.csv'
        feiertage_file = 'feiertage.csv'
        holidays_file = 'holidays.csv'

        # Verzeichnis, in dem die Dateien liegen
        directory = 'data/gui'

        # Liste der Dateinamen
        files = (weather_file, football_file, feiertage_file, holidays_file)

        # Überprüfen und Löschen der Dateien
        for filename in files:
            file_path = os.path.join(directory, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f'Datei {filename} wurde gelöscht.')
            else:
                print(f'Datei {filename} existiert nicht.')

        if weather_toggle:
            file_path = os.path.join(directory, weather_file)
            weather.to_csv(file_path, encoding='utf-8', index=False)
        if football_toggle:
            file_path = os.path.join(directory, football_file)
            football.to_csv(file_path, encoding='utf-8', index=False)
        if feiertage_toggle:
            file_path = os.path.join(directory, feiertage_file)
            feiertage.to_csv(file_path, encoding='utf-8', index=False)
        if holidays_toggle:
            file_path = os.path.join(directory, holidays_file)
            holidays.to_csv(file_path, encoding='utf-8', index=False)
        stm.write("Generiere Forecast :chart_with_upwards_trend:")
        # run pipeline
        products_to_predict: int = []
        for i in options:
            if i in product_range.keys():
                products_to_predict += [product_range[i]]
            if i in product_range.values():
                products_to_predict += [i]
        if len(options) == 0:
            products_to_predict = [i for i in product_range.values()]
        # send products_to_predict and day_of_prediction
        live_predict = main(products_to_predict, date_str1, date_str2)
        stm.write("Forecast aufbereiten :memo:")

        prediction_data = []
        for key, value in live_predict.items():
            if 'Prediction-Date' in value:
                prediction_dates = [date.strftime('%Y-%m-%d') for date in value['Prediction-Date']]
                name = value['Name']
                id_ = str(value['ID'])  # Konvertiere ID in einen String
                prediction = value['Prediction']
                for date, pred in zip(prediction_dates, prediction):
                    prediction_data.append((name, id_, date, pred))

        # Erstelle ein gemeinsames DataFrame aus den extrahierten Daten
        forecast_df = pd.DataFrame(prediction_data, columns=['Name', 'ID', 'Prediction-Date', 'Prediction'])

        # Anzeigen des DataFrames
        print(forecast_df)
        stm.write("Speichere Forecast :floppy_disk:")
        forecast_file = 'forecast.csv'
        file_path = os.path.join(directory, forecast_file)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f'Datei {filename} wurde gelöscht.')
        else:
            print(f'Datei {filename} existiert nicht.')
        file_path = os.path.join(directory, forecast_file)
        forecast_df.to_csv(file_path, encoding='utf-8', index=False)
        status.update(label=":100: Data generiert", state="complete", expanded=False)

    URL_STRING = "http://localhost:8501/Resultate"

    stm.markdown(
        f'<a target="_self" href="{URL_STRING}" style="display: inline-block; padding: 12px 20px; background-color: #4CAF50; color: white; text-align: center; text-decoration: none; font-size: 16px; border-radius: 4px;">Daten anzeigen :heart:</a>',
        unsafe_allow_html=True
    )
