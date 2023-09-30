import datetime as dt
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

ORIGIN_CITY_IATA = "WAS"
manual_mode = False

TODAY = dt.date.today()
TODAY_FORMATTED = TODAY.strftime("%d/%m/%Y")
TOMORROW = TODAY + dt.timedelta(1)
TOMORROW_FORMATTED = TOMORROW.strftime("%d/%m/%Y")
SIX_MONTHS_FROM_NOW = TOMORROW + dt.timedelta(weeks=26)
SIX_MONTHS_FROM_NOW_FORMATTED = SIX_MONTHS_FROM_NOW.strftime("%d/%m/%Y")



# MANUAL CALL

if manual_mode:
    destination_city_iata = "HKG"

    flight = flight_search.find_flights(
            ORIGIN_CITY_IATA,
            destination_city_iata,
            from_time=TOMORROW_FORMATTED,
            to_time=SIX_MONTHS_FROM_NOW_FORMATTED,
            max_stopovers=2
        )

    email_list = data_manager.get_email_addresses()

    notification_manager.send_emails(flight.price, flight.origin_city, flight.origin_airport,
                                      flight.destination_city, flight.destination_airport, flight.out_date,
                                      flight.return_date, email_list)
else:
    sheet_data = data_manager.get_destination_data()
    print(f"sheet data: \n{sheet_data}")
    email_list = data_manager.get_email_addresses()

    if sheet_data[0]["iataCode"] == "":
        for row in sheet_data:
            row["iataCode"] = flight_search.find_codes(row["city"])
        data_manager.destination_data = sheet_data
        # data_manager.update_destination_codes()

    for destination in sheet_data:
        flight = flight_search.find_flights(
            ORIGIN_CITY_IATA,
            destination["iataCode"],
            from_time=TOMORROW_FORMATTED,
            to_time=SIX_MONTHS_FROM_NOW_FORMATTED,
            max_stopovers=2
        )
        update_google_sheet = False
        try:
            if flight.price < destination["lowestPrice"]:
                notification_manager.send_message(flight.price, flight.origin_city, flight.origin_airport,
                                                  flight.destination_city, flight.destination_airport, flight.out_date,
                                                  flight.return_date)
                # TODO rewrite to only edit the row in question; not re-run all of them
                destination["lowestPrice"] = flight.price
                data_manager.destination_data = sheet_data
                update_google_sheet = False

        except AttributeError:
            print(f"No nonstop flights were available for {ORIGIN_CITY_IATA} to {destination['iataCode']}.\nChecking flights with 1 layover")
            flight = flight_search.find_flights(
                ORIGIN_CITY_IATA,
                destination["iataCode"],
                from_time=TOMORROW_FORMATTED,
                to_time=SIX_MONTHS_FROM_NOW_FORMATTED,
                max_stopovers=2
            )
        finally:
            notification_manager.send_emails(flight.price, flight.origin_city, flight.origin_airport,
                                             flight.destination_city, flight.destination_airport, flight.out_date,
                                             flight.return_date, email_list)

            if update_google_sheet:
                data_manager.update_destination_lowest_price()





"""
cities_with_codes = [[2, 'Paris', 'PAR', '54'], [3, 'Berlin', 'BER', '42'], [4, 'Tokyo', 'TYO', '485'], [5, 'Sydney', 'SYD', '551'], [6, 'Istanbul', 'IST', '95'], [7, 'Kuala Lumpur', 'KUL', '414'], [8, 'New York', 'NYC', '240'], [9, 'San Francisco', 'SFO', '260'], [10, 'Cape Town', 'CPT', '378']]


print(f"cities with codes: {cities_with_codes}")


flights_with_prices = flight_search.find_flights(cities_with_codes)
print(f"flights with prices: {flights_with_prices}")

"""
