import requests
from flight_data import FlightData

flightsearch_api = None  # replace with flightsearch API
flightsearch_endpoint = "https://api.tequila.kiwi.com"
flightsearch_headers = {
        "apikey": flightsearch_api,
        "Content-Type": "application/json"
    }

ONEWAY_OR_ROUND = "round"  # "round" / "oneway"


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.

    def find_codes(self, city_name):
        locations_endpoint = f"{flightsearch_endpoint}/locations/query"
        query = {"term": city_name, "location_types": "city"}
        response = requests.get(
            url=locations_endpoint,
            headers=flightsearch_headers,
            params=query
        )
        results = response.json()["locations"]
        code = results[0]["code"]
        return code

    def find_flights(self, origin_city_code, destination_city_code, from_time, to_time, max_stopovers=0):
        search_endpoint = f"{flightsearch_endpoint}/v2/search"
        print(f"max_stopovers: {max_stopovers}")
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time,
            "date_to": to_time,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": max_stopovers,
            "curr": "usd"
        }

        response = requests.get(
            url=search_endpoint,
            headers=flightsearch_headers,
            params=query
        )
        print(f"response from flight search: \n{response.text}")

        try:
            data = response.json()["data"][0]
        except IndexError:
            print(f"No flights were available for {origin_city_code} to {destination_city_code} with (up to) {max_stopovers} stop(s).")

            if input("Try with an additional stopover? (y/n)\n") == "y":
                max_stopovers += 1
                flight_data = self.find_flights(origin_city_code, destination_city_code, from_time, to_time, max_stopovers=max_stopovers)
                return flight_data
            else:
                pass
        else:
            if max_stopovers == 0:
                route_seg_num = ((len(data['route'])) - 1)

                flight_data = FlightData(
                    price=data["price"],
                    origin_city=data["cityFrom"],
                    origin_airport=data["flyFrom"],
                    destination_city=data["cityTo"],
                    destination_airport=data["flyTo"],
                    out_date=data["route"][0]["local_departure"].split("T")[0],
                    return_date=data["route"][route_seg_num]["local_arrival"].split("T")[0],
                    via_city=data["route"][0]["cityTo"],
                )

                print(f"{flight_data.destination_city}: ${flight_data.price}")
                print(f"Num of route entries: {len(data['route'])}")
                print(f"dates: from {flight_data.out_date} to {flight_data.return_date}")

                return flight_data

            else:
                route_seg_num = ((len(data['route'])) - 1)

                flight_data = FlightData(
                    price=data["price"],
                    origin_city=data["cityFrom"],
                    origin_airport=data["flyFrom"],
                    destination_city=data["cityTo"],
                    destination_airport=data["flyTo"],
                    out_date=data["route"][0]["local_departure"].split("T")[0],
                    return_date=data["route"][route_seg_num]["local_arrival"].split("T")[0],
                    via_city=data["route"][0]["cityTo"],
                )

                print(f"{flight_data.destination_city}: ${flight_data.price} (via {flight_data.via_city})")
                print(f"Num of route entries: {len(data['route'])}")
                print(f"dates: from {flight_data.out_date} to {flight_data.return_date}")

                return flight_data



#### INFO ####

"""
https://tequila.kiwi.com/portal/docs/tequila_api/search_api
"""


"""
selected_cabins - Specifies the preferred cabin class. Cabins can be: M (economy), W (economy premium), C (business), or F (first class). There can be only one selected cabin for one call. Cannot be used for ground (train, bus) content.

# "mix_with_cabins": "M",
# "fly_days": "0123456",
# "fly_days_type": "departure",
# "ret_fly_days": "0123456",
# "ret_fly_days_type": "departure",
# "stopover_from": "72:00",
# "stopover_to": "24:00",

"sort" - # price / quality / duration / date

"""

"""
def __init__(self):
    self.api = flightsearch_api
    self.endpoint = flightsearch_endpoint
    
    self.today_date = TODAY_FORMATTED
    self.search_day_start = TOMORROW_FORMATTED
    self.search_day_end = SIX_MONTHS_FROM_NOW_FORMATTED
    self.starting_city = "WAS
    
"""


"""

"fly_from": self.starting_city,
"fly_to": item[2],
"date_from": self.search_day_start,
"date_to": self.search_day_end,
"nights_in_dst_from": 7,
"nights_in_dst_to": 28,
"flight_type": "round",
"one_for_city": 1,
"max_stopovers": 0,
"curr": "usd"

"""


"""

"fly_from": self.starting_city,
"fly_to": item[2],
"date_from": self.search_day_start,
"date_to": self.search_day_end,
"return_from": self.search_day_start,
"return_to": self.search_day_end,
"nights_in_dst_from": 2,
"nights_in_dst_to": 30,
"max_fly_duration": 20,
"flight_type": ONEWAY_OR_ROUND,
"ret_from_diff_city": True,
"ret_to_diff_city": True,
"one_for_city": 0,
"one_per_date": 0,
"adults": 1,
"selected_cabins": "M",
"only_weekends": False,
"partner_market": "us",
"curr": "USD",
"locale": "en",
"dtime_from": "6:00",
"dtime_to": "21:00",
"atime_from": "23:59",
"atime_to": "23:00",
"ret_dtime_from": "6:00",
"ret_dtime_to": "21:00",
"ret_atime_from": "23:59",
"ret_atime_to": "23:00",
"max_stopovers": "0",
"ret_from_diff_airport": "1",
"ret_to_diff_airport": "1",
"vehicle_type": "aircraft",
"sort": "price",
"asc": "1",
"limit": "1",

"""