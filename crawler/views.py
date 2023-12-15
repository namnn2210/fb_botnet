from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request=request, template_name='index.html')


def process(request):
    if request.method == 'POST':
        print('================================')
        return render(request=request, template_name='form.html')
    else:
        return render(request=request, template_name='form.html')
