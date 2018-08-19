from django.urls import path

from . import views
app_name = 'home'
urlpatterns = [
	# This is the landing page
    path('', views.index, name='index'),
]
