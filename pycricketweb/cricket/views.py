from django.shortcuts import render
import json
from datetime import datetime


from . import CRICKET_API


def homeHandler(request):
  recent_match_data = CRICKET_API.get_recent_matches()
  data = recent_match_data['data']
  return render(request, 'home.html', data)

def matchHandler(request, match_key): 
  match_data = CRICKET_API.get_match(match_key)
  card = match_data['data']['card']
  timestamp_date = card['start_date']['timestamp']
  date = datetime.fromtimestamp(timestamp_date)
  card['start_date']['datetime_obj'] = date
  if card['man_of_match']:
    card['man_of_match_obj'] = card['players'][card['man_of_match']]
  else:
    card['man_of_match_obj'] = ""
  card['now'] = datetime.now() 
  card['squad_a'] = card['teams']['a']['match']['players']
  card['playing_11_a'] = card['teams']['a']['match']['playing_xi']
  captain = card['teams']['a']['match']['captain']
  keeper = card['teams']['a']['match']['keeper']
  card['playing_11_a_obj'] = []
  for player_a_key in card['playing_11_a']:
    if player_a_key == captain:
      card['players'][player_a_key]['is_captain'] = True
    # if card['players'][player_a_key] == keeper:
    #   card['players'][player_a_key]['is_keeper'] = True
    card['playing_11_a_obj'].append(card['players'][player_a_key])

  return render(request, 'match.html', card)