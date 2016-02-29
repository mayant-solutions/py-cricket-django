from django.shortcuts import render
import json

from . import CRICKET_API


def homeHandler(request):
  recent_match_data = CRICKET_API.get_recent_matches()
  data = recent_match_data['data']
  return render(request, 'home.html', data)

def matchHandler(request, match_key): 
  match_data = CRICKET_API.get_match(match_key)
  card = match_data['data']['card']
  return render(request, 'match.html', card)