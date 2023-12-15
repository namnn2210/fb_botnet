from django.shortcuts import render
import requests

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
            "longitude": longitude
        }
        return response_data
    except Exception as e:
        return None


def process(request):
    if request.method == 'POST':
        final_data = {}
        public_ip = get_client_ip(request)
        geolocation = get_geolocation(public_ip)
        final_data['public_ip'] = public_ip
        final_data.update(geolocation)
        print(final_data)
        return render(request=request, template_name='form.html')
    else:
        return render(request=request, template_name='form.html')
