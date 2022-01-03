#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime
from datetime import timedelta
from notification_manager import NotificationManager



now = datetime.today()
delta_1day = timedelta(days=1)
delta_6months = timedelta(days=180)
tomorrow = (now+delta_1day).strftime("%d/%m/20%y")
within_6months = (now+delta_6months).strftime("%d/%m/20%y")


data_manager = DataManager()
data_manager.sheet_data = data_manager.get_data()
sheet_data = data_manager.get_data()
# print(sheet_data)
search = FlightSearch("paris")
iata_code = []
cities = [dic['city'] for dic in sheet_data]
# print(cities)
if sheet_data[0]["iataCode"] == "":
    for city in cities:
        iata_code.append(FlightSearch(city).code)
    # print(iata_code)

data_manager.update_iata(iata_code)
data_manager.sheet_data = data_manager.get_data()
sheet_data = data_manager.sheet_data
# print(sheet_data)

users = data_manager.get_customer_emails()
emails = [row["email"] for row in users]
names = [row["firstName"] for row in users]

for destination in sheet_data:
    flight = search.check_flights(destination, destination['iataCode'], tomorrow, within_6months)
    if flight is not None and flight.price < destination['lowestPrice']:
        msg = F"Low price alert! only £{flight.price} to fly from {flight.origin_city}-{FlightSearch(flight.origin_city).code} to " \
              F"{flight.destination_city}-{FlightSearch(flight.destination_city).code}, from {flight.out_date} to {flight.return_date}"
        if flight.stopover > 0:
            msg += f"\nFlight has {flight.stopover} stop over, via {flight.via_city}."

        link = f"https://www.google.co.uk/flights?hl=en#flt={flight.origin_airport}.{flight.destination_airport}.{flight.out_date}*{flight.destination_airport}.{flight.origin_airport}.{flight.return_date}"
        NotificationManager().send_emails(emails, msg, link)

