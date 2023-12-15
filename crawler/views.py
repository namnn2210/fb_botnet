from django.shortcuts import render


# Create your views here.
def index(request):
    return render(template_name='index.html')


def process(request):
    if request.method == 'POST':
        print(request)
    else:
        return render(template_name='form.html')
