from django.urls import path
from . import views

urlpatterns = [
    path("",views.predictions_page,name="predictions"),
]
