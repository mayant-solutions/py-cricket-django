from django.conf.urls import url

from cricket import views

urlpatterns = [
	
    url(r'^$', views.homeHandler, name='home'),
    url(r'^match/(?P<match_key>.+)/$', views.matchHandler, name='match')
]
