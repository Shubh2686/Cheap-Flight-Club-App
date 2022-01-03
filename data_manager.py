import requests
End_Point = "https://api.sheety.co/80a776766d1e7c2c63ae29076d75aaa4/myFlightDeals/prices"
USERS_EndPoint = "https://api.sheety.co/80a776766d1e7c2c63ae29076d75aaa4/myFlightDeals/users"

header = {
                "Authorization": "Bearer thisisshit"
            }

class DataManager:
    def __init__(self):
        self.sheet_data = {}
        self.customer_data = {}

    def get_data(self):
        response = requests.get(url=End_Point, headers=header)
        print(response.text)
        response.raise_for_status()
        data = response.json()["prices"]
        return data

    def update_iata(self, code_list):
        if self.sheet_data[0]["iataCode"] == "":
            i = 0
            for dic in self.sheet_data:
                id = dic["id"]
                new_data = {
                    "price": {
                        'iataCode': code_list[i]
                    }
                }

                response = requests.put(url=f"{End_Point}/{id}", json=new_data, headers=header)
                print(response.text)
                i += 1

    def get_customer_emails(self):
        customers_endpoint = USERS_EndPoint
        response = requests.get(url=customers_endpoint)
        data = response.json()
        self.customer_data = data["users"]
        return self.customer_data


    pass