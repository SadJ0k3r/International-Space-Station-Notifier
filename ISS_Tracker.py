import os
import smtplib
import requests
from datetime import datetime
import time

# Your latitude and longitude
MY_LAT = 51.5074
MY_LONG = -0.1278

# Your email details
MY_EMAIL = os.environ.get('MY_EMAIL')
MY_PASSWORD = os.environ.get('MY_PASSWORD')
TO_EMAIL = os.environ.get('TO_EMAIL')

def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    
    data = response.json()
    
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    
    #Your position is within +5 or -5 degrees of the ISS position.
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True

def send_email():
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL, 
            to_addrs=TO_EMAIL, 
            msg="Subject:Look Up!\n\nThe ISS is above you in the sky."
        )

while True:
    # If the ISS is close to my current position
    # and it is currently dark
    if is_iss_overhead():
        send_email()
    # Then send me an email to tell me to look up.
    # BONUS: run the code every 60 seconds.
    time.sleep(60)
