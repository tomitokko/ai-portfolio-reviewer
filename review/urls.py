from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('submit-url', views.submit_url, name='submit-url'),
    path('feedback', views.feedback, name='feedback'),
]