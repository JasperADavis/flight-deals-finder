class FlightData:
    # This class is responsible for structuring the flight data.
    # Think of it as creating a class instance to represent each flight (rather than leaving all associated info in a dict format)

    def __init__(self, price, origin_city, origin_airport, destination_city, destination_airport, out_date, return_date, via_city=""):
        self.price = price
        self.origin_city = origin_city
        self.origin_airport = origin_airport
        self.destination_city = destination_city
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date
        self.stop_overs = 0
        self.via_city = via_city

    # def send_message(self, flight_data, sheet_data):
    #     # check
    #     # check if current price is lower than lowest price from sheet
    #     if i in range(len(sheet_data[])):
    #         # check each location for tomorrow - 6 months away prices
    #         # find lowest (one-way?), if lowest is lower than sheet's lowest, send text and update sheet via data_manager
    #         pass


"""

def organize_flight_data(self, flights_with_prices):
    for item in flights_with_prices:
        city = item["data"][0]["cityTo"]
        price = item["data"][0]["price"]
        print(f"{city}: ${price}")

"""