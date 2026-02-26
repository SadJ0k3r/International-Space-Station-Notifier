# ==================================================
# 🌌🛰️ ISS Tracker - International Space Station Notifier
# Tracks the ISS and sends an email alert when
# it passes over your location at night!
# ==================================================

import os
import smtplib
import requests
from datetime import datetime
import time

# =============================================
# 📍 Configuration - Set Your Location
# =============================================
MY_LAT  = 51.5074   # Your latitude  (e.g. London)
MY_LONG = -0.1278   # Your longitude (e.g. London)

# =============================================
# 📧 Email Credentials (from environment variables)
# =============================================
MY_EMAIL    = os.environ.get('MY_EMAIL')
MY_PASSWORD = os.environ.get('MY_PASSWORD')
TO_EMAIL    = os.environ.get('TO_EMAIL')

# =============================================
# 🛰️ Check if ISS is Overhead
# =============================================
def is_iss_overhead():
    """
    Queries the Open Notify API to get the current
    ISS position and checks if it's within +/-5 degrees
    of your configured lat/long.

    Returns:
        bool: True if ISS is overhead, False otherwise.
    """
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()

    data = response.json()
    iss_latitude  = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    print(f"🛰️  ISS Position -> Lat: {iss_latitude:.4f}, Long: {iss_longitude:.4f}")

    # 📌 Check if ISS is within 5 degrees of your location
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True
    return False


# =============================================
# 🌙 Check if It Is Currently Nighttime
# =============================================
def is_night():
    """
    Queries the Sunrise-Sunset API for your location
    and checks if the current time is after sunset
    or before sunrise (i.e. it is dark outside).

    Returns:
        bool: True if it is night, False otherwise.
    """
    params = {
        "lat":       MY_LAT,
        "lng":       MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=params)
    response.raise_for_status()

    data        = response.json()
    sunrise_hr  = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset_hr   = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now    = datetime.now().hour

    print(f"🌅 Sunrise: {sunrise_hr}:00 UTC | 🌇 Sunset: {sunset_hr}:00 UTC | 🕒 Now: {time_now}:00 UTC")

    # It's dark if we're past sunset OR before sunrise
    if time_now >= sunset_hr or time_now <= sunrise_hr:
        return True
    return False


# =============================================
# 📧 Send Email Notification
# =============================================
def send_email():
    """
    Sends an email alert via Gmail SMTP to notify
    that the ISS is currently overhead and visible.
    """
    print("📧 Sending ISS alert email...")
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=TO_EMAIL,
            msg=(
                "Subject: 🛰️ Look Up! ISS Overhead!\n\n"
                "🌌 The International Space Station is passing over your location right now!\n"
                "🔭 Grab your binoculars and look up at the sky! 🌠\n\n"
                f"Your Location -> Lat: {MY_LAT}, Long: {MY_LONG}\n"
                "Enjoy the view! 🚀"
            )
        )
    print("✅ Email sent successfully!")


# =============================================
# 🔄 Main Loop - Check Every 60 Seconds
# =============================================
print("🚀 ISS Tracker started! Checking every 60 seconds...")
print(f"📍 Monitoring location -> Lat: {MY_LAT}, Long: {MY_LONG}")

while True:
    time.sleep(60)  # ⏳ Wait 60 seconds between checks

    # ✅ Only alert if it's dark AND the ISS is overhead
    if is_night() and is_iss_overhead():
        send_email()
    else:
        print("🔍 ISS is not overhead or it's still daytime. Waiting...")
