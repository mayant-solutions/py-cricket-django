from django.conf.urls import url

from cricket import views

urlpatterns = [
	
    url(r'^$', views.homeHandler, name='home'),
    url(r'^match/(?P<match_key>.+)/$', views.matchHandler, name='match'),
    url(r'^season/(?P<season_key>.+)/$', views.seasonHandler, name='season'),
    url(r'^schedule/$', views.scheduleHandler, name='schedule'),
    url(r'^schedule/(?P<month>.+)/(?P<year>.+)/$', views.scheduleHandler, name='schedule')

]
