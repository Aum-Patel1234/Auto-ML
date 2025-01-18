from django.shortcuts import render

# Create your views here.
def predictions_page(request):
    return render(request ,'automl_app/index.html')