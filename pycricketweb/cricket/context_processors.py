from django.core.cache import cache
from . import CRICKET_API
from django.conf import settings

def get_recent_season(request):

	recent_seasons_cache_data = cache.get('recent_seasons')
	if recent_seasons_cache_data:
		recent_seasons = recent_seasons_cache_data
		# print "have_cache"
	else:
		# print "set_cache"
		recent_seasons = CRICKET_API.get_recent_seasons()
		recent_seasons = recent_seasons['data']
		cache.set('recent_seasons', recent_seasons, settings.RECENT_SEASON_CACHE)

	return {'recent_seasons': recent_seasons}