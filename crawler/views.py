from django.shortcuts import render


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


def get_geolocation(request):
    try:
        # Get the public IP address of the client
        client_ip = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')

        # Make a request to ipinfo.io to retrieve geolocation data
        response = requests.get(f"https://ipinfo.io/{client_ip}/json")
        geolocation_data = response.json()

        # Extract country code and city from the response
        country_code = geolocation_data.get("country")
        city = geolocation_data.get("city")

        # Create a JSON response with the geolocation information
        response_data = {
            "country_code": country_code,
            "city": city
        }
        return response_data
    except Exception as e:
        return None


def process(request):
    if request.method == 'POST':
        ip = get_client_ip(request)
        print(ip)
        return render(request=request, template_name='form.html')
    else:
        return render(request=request, template_name='form.html')
