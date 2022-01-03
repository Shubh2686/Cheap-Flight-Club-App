import requests
import pprint
from flight_data import FlightData

endpoint = "https://tequila-api.kiwi.com"
api_key = "qS2LBlI3mh5Xfc5MD5zCrQFot1sjfAwN"


class FlightSearch:
    def __init__(self, city):
        headers ={
            "apikey": api_key
        }
        self.parameters ={
            "term": city

        }
        self.response = requests.get(url=f"{endpoint}/locations/query", params=self.parameters, headers=headers)
        self.response.raise_for_status()
        self.code = self.response.json()['locations'][0]["code"]

    def check_flights(self, destination, destination_iatacode, tomorrow, within_6months):
        headers = {
            "apikey": api_key
        }
        parameters = {
            'fly_from': 'LON',
            'fly_to': destination_iatacode,
            'date_from': tomorrow,
            'date_to': within_6months,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP"
        }
        response = requests.get(url=f"{endpoint}/v2/search", params=parameters, headers=headers)
        # print(self.response.text)
        response.raise_for_status()
        # data = response.json()["data"][0]
        try:
            data = response.json()["data"][0]
        except IndexError:
            parameters["max_stopovers"] = 1
            response = requests.get(url=f"{endpoint}/v2/search", params=parameters, headers=headers)
            response.raise_for_status()
            try:
                data = response.json()["data"][0]
                # pprint.pprint(data)
            except IndexError:
                print(f"No flights found for {destination_iatacode}")
                return None
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][1]["cityTo"],
                destination_airport=data["route"][1]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][2]["local_departure"].split("T")[0],
                stopover=1,
                via_city=data["route"][0]["cityTo"]
            )
            print(f"/stop over = 1/{flight_data.destination_city}: £{flight_data.price}.")
            return flight_data
        flight_data = FlightData(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0]
        )
        print(f"{flight_data.destination_city}: £{flight_data.price}")
        return flight_data
    pass