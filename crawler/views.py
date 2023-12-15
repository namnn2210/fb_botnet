from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request=request, template_name='index.html')


def process(request):
    if request.method == 'POST':
        client_ip = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
        print(client_ip)
    else:
        return render(request=request, template_name='form.html')
