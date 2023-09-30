import requests

sheet_endpoint = None  # replace with sheet endpoint
email_db_endpoint = None  # replace with Sheety endpoint
sheet_headers = {
            "Authorization": "" # replace with necessary authorization
        }


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.destination_data = {}
        self.email_list = []

    def get_destination_data(self):
        response = requests.get(
            url=sheet_endpoint,
            headers=sheet_headers
        )
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{sheet_endpoint}/{city['id']}",
                json=new_data,
                headers=sheet_headers,
            )
            # print(f"update destination codes response: \n{response.text}")

    def update_destination_lowest_price(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "lowestPrice": city["lowestPrice"]
                }
            }
            response = requests.put(
                url=f"{sheet_endpoint}/{city['id']}",
                json=new_data,
                headers=sheet_headers,
            )

    def get_email_addresses(self):
        response = requests.get(
            url=email_db_endpoint,
            headers=sheet_headers
        )
        data = response.json()

        print(f"email json: \n{data}")

        for user in data["users"]:
            self.email_list.append((user["firstName"], user["lastName"], user["email"]))
        return self.email_list