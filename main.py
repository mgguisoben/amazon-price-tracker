import os
import smtplib

import requests
from bs4 import BeautifulSoup

MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")
TO_EMAIL = os.environ.get("TO_EMAIL")

product_url = ("https://www.amazon.com/OSTRICH-ORIGINAL-Pillow-Airplanes-Accessories/dp/B00B4S6SLW/ref=sr_1_5?crid"
               "=ZT4TM3XHX6EI&keywords=ostrich+pillow&qid=1698756512&sprefix=ostrich+pill%2Caps%2C359&sr=8-5")
# From http://myhttpheader.com/
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0",
    "Accept-Language": "en-US,en;q=0.5"
}

response = requests.get(url=product_url, headers=headers).text

soup = BeautifulSoup(response, "lxml")

product_title = soup.find(name="span", id="productTitle").getText()

price_whole = soup.find(name="span", class_="a-price-whole").getText()
price_fraction = soup.find(name="span", class_="a-price-fraction").getText()
price = float(price_whole + price_fraction)

# Check if price is below the price you want
if price < 70:
    with smtplib.SMTP(host="smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=TO_EMAIL,
            msg=f"Subject: Low Price Alert {product_title} is now {price}"
        )

print("Done!")
