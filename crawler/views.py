from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request=request, template_name='index.html')


def process(request):
    if request.method == 'POST':
        print(request)
    else:
        return render(request=request, template_name='form.html')
