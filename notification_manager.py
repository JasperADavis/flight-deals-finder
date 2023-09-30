import requests
from twilio.rest import Client
import smtplib
import datetime as dt


# ------------------- CONSTANTS -------------------

MY_EMAIL = None # replace with email username
PASSWORD = None # replace with email password
my_email_y = None # replace with 2nd email address

# Twilio account info
account_sid = None # replace with Twilio account sid
auth_token = None # replace with Twilio auth_token


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.

    def __init__(self):
        self.message_text = ""
        self.email_text = ""

    def send_message(self, price, departure_city, departure_airport_code, arrival_city, arrival_airport_code,
                     outbound_date, return_date):
        self.message_text = f"\nOnly ${price} to fly from {departure_city}-{departure_airport_code} to {arrival_city}-{arrival_airport_code}, from {outbound_date} to {return_date}"

        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=self.message_text,
            from_="+1", # replace with phone number
            to="+1",  # replace with phone number
        )
        print(f"Twilio message status for {departure_airport_code} to {arrival_airport_code}: {message.status}")

    def send_emails(self, price, departure_city, departure_airport_code, arrival_city, arrival_airport_code, outbound_date, return_date, email_list):  # or get these elements in main.py and place them in a text var that is sent to this function
        # str format for date (dd-mm-yy)
        fixed_outbound_date = f"{outbound_date[8:10]}-{outbound_date[5:7]}-{outbound_date[2:4]}"
        fixed_return_date = f"{return_date[8:10]}-{return_date[5:7]}-{return_date[2:4]}"
        print(f"DEBUG:\nfixed outbound: {fixed_outbound_date}\nfixed return: {fixed_return_date}\ndeparture code: {departure_airport_code}\narrival code: {arrival_airport_code}")
        self.email_text = f"\nOnly ${price} to fly from {departure_city}-{departure_airport_code} to {arrival_city}-{arrival_airport_code}, from {outbound_date} to {return_date}"
        url_str = f"https://www.google.com/travel/flights?q=Flights%20to%20{arrival_airport_code}%20from%20{departure_airport_code}%20on%20{fixed_outbound_date}%20through%20{fixed_return_date}"
        print(f"link to book: \n{url_str}")
        print(f"Email list: {email_list}")

        for person in email_list:
            with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL, password=PASSWORD)
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=person[2],
                    msg=f"{self.email_text}\n\nBook your ticket now: \n{url_str}"
                )
            print(f"email sent to {person[0]} {person[1]} at {person[2]}")


"""
reference:
https://www.google.com/travel/flights?q=Flights%20to%20SFO%20from%20HNL%20on%2023-09-13%20through%2023-09-23

"""