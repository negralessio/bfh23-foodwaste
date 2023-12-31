import requests
import pandas as pd
import pgeocode


class APIHandler:
    def __init__(self):
        # Hier API-Key eintragen etc. eintragen oder erweitern
        self.api_key = None

    def get_data_from_OpenLigaDB(self, team, weekCountPast, weekCountFuture):
        # Getting Matches for a certain Team based on count last Weeks and future Weeks
        url = "https://api.openligadb.de/getmatchesbyteam/{}/{}/{}".format(team, weekCountPast, weekCountFuture)
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # Die JSON-Daten bearbeiten, um die gewünschten Werte zu extrahieren
            formatted_data = [{
                "Datum": item["matchDateTime"],
                "LeagueName": item["leagueName"],
                "Team1": item["team1"]["teamName"],
                "Team2": item["team2"]["teamName"],
                "Team1Icon": item["team1"]["teamIconUrl"],
                "Team2Icon": item["team2"]["teamIconUrl"]
            } for item in data]
            # DataFrame erstellen
            df = pd.DataFrame(formatted_data)
            filtered_df = df[df['Team1'].str.contains('Freiburg')]
            return filtered_df
        else:
            return None

    def get_data_from_WeatherAPI_History(self, plz, start_date, end_date):
        nomi = pgeocode.Nominatim('de')
        location = nomi.query_postal_code(plz)
        url = "https://archive-api.open-meteo.com/v1/archive?latitude={}&longitude={}&start_date={}&end_date={}&hourly=temperature_2m,rain,snowfall&timezone=Europe%2FBerlin".format(
            location.latitude, location.longitude, start_date, end_date)
        print(url)
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            hourly_data = {
                "time": data["hourly"]["time"],
                "temperature_2m": data["hourly"]["temperature_2m"],  # Celsius
                "rain": data["hourly"]["rain"],  # mm
                "snowfall": data["hourly"]["snowfall"]  # cm
            }
            # DataFrame erstellen
            df = pd.DataFrame(hourly_data)
            return df
        else:
            return None

    def get_data_from_FeiertageAPI(self, year, state_code):
        url = "https://feiertage-api.de/api/?jahr={}&nur_land={}".format(year, state_code)
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data).T
            return df
        else:
            return None

    def get_data_from_FerienAPI(self, state_code, year):
        url = "https://ferien-api.de/api/v1/holidays/{}/{}".format(state_code, year)
        print(url)
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            return df
        else:
            return None

    def get_data_from_PostcodeAPI(self, plz):
        nomi = pgeocode.Nominatim('de')
        location = nomi.query_postal_code(plz)
        return location.place_name, location.state_name, location.state_code
    def list_available_apis(self):
        api_methods = [func for func in dir(self) if callable(getattr(self, func)) and not func.startswith("__")]
        return api_methods


"""if __name__ == '__main__':
    my_api = APIHandler()

    weather, plz, place_name, state_name, state_code = my_api.get_data_from_WeatherAPI_History(77652, "2023-10-05", "2023-10-05")
    print(weather)

    feiertage = my_api.get_data_from_FeiertageAPI(2023, state_code)
    print(feiertage)

    ferien = my_api.get_data_from_FerienAPI(state_code, 2023)
    print(ferien)

    print("Verfügbare API-Funktionen:")
    available_apis = my_api.list_available_apis()
    for api in available_apis:
        print(api)

    # 77652 (Offenburg)"""
