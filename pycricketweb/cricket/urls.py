from django.conf.urls import url

from cricket import views

urlpatterns = [
	
    url(r'^$', views.home, name='home'),
]
