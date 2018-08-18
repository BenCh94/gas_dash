from django.urls import path

from . import views

urlpatterns = [
	# This is the landing page
    path('', views.index, name='index'),
]
