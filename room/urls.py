from django.urls import path

from .views import AddMeasure, GetMeasures

urlpatterns = [
    path('add_measure/', AddMeasure.as_view()),
    path('get_measures/', GetMeasures.as_view()),
]
