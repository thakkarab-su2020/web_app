
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='ui-home'),
    path('about/',views.about, name='ui-about'),

]
