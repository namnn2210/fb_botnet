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

def process(request):
    if request.method == 'POST':
        ip = get_client_ip(request)
        print(ip)
        return render(request=request, template_name='form.html')
    else:
        return render(request=request, template_name='form.html')
