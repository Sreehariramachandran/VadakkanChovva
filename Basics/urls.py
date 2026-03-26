from django.urls import path
from Basics import views
urlpatterns = [
    path('Sum/',views.Sum,name="Sum"),
    path('Largest/',views.Largest,name="Largest"),
    path('Calculator/',views.Calculator,name="Calculator"),
]