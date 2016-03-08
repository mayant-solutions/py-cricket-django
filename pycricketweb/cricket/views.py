from django.shortcuts import render

from datetime import datetime
from . import CRICKET_API
from smart import *
import json



def homeHandler(request):
  recent_matches_data = CRICKET_API.get_recent_matches("summary_card")
  recent_matches_data = recent_matches_data['data']['cards']
  smart_cards = prepare_smart_cards(recent_matches_data)
  return render(request, 'home.html', smart_cards)


def seasonHandler(request, season_key):
  season_data = CRICKET_API.get_season(season_key, "summary_card")
  season_matches = season_data['data']['season']['matches']
  season_matches_list = []
  for key, season_match in season_matches.items():
    season_matches_list.append(season_match)


  sorted_season_matches_list = sorted(season_matches_list, key=lambda k: k['start_date']['timestamp']) 
  smart_cards = prepare_smart_cards(sorted_season_matches_list)
  return render(request, 'home.html', smart_cards)


def matchHandler(request, match_key): 
  match_data = CRICKET_API.get_match(match_key)
  card = match_data['data']['card']
  
  if card['status'] == 'completed':
    smart_card = create_match_completed_data(card)
  elif card['status'] == 'started':
    smart_card = create_match_started_card(card) 
  else:
    smart_card = create_match_notstarted_data(card)

  smart_card = {'smart_card': smart_card}
  smart_card['title'] = card['title']
  smart_card['season_name'] = card['season']['name']
  smart_card['start_date_str'] = card['start_date']['str']
  smart_card['format'] = card['format']
  smart_card['toss_str'] = card['toss']['str']
  smart_card['venue'] = card['venue']

  smart_card['team_a_name'] = card['teams']['a']['name']
  smart_card['team_b_name'] = card['teams']['b']['name']

  team_a_obj = card['teams']['a']['match']
  squad_a_keys = team_a_obj['players']
  playing_11_a_keys = team_a_obj['playing_xi']
  
  smart_card['playing_11_a_obj'] = []
  smart_card['playing_a_obj'] = []
  bench_a_keys = []
  smart_card['bench_a_obj'] = []
  smart_card['have_benach_a'] = False
  smart_card['have_playing_a_11'] = False
  smart_card['have_benach_b'] = False
  smart_card['have_playing_b_11'] = False
  smart_card['have_squad_a'] = False
  smart_card['have_squad_b'] = False


  # Playing 11, season squad and bench player information for Team a
  if playing_11_a_keys:
    bench_a_keys = set(squad_a_keys) - set(playing_11_a_keys)
  for player_a_key in squad_a_keys:
    captain = card['teams']['a']['match']['captain']
    keeper = card['teams']['a']['match']['keeper']
    if player_a_key == captain:
      card['players'][player_a_key]['is_captain'] = True
    if player_a_key == keeper:
      card['players'][player_a_key]['is_keeper'] = True

    if player_a_key in bench_a_keys:
      smart_card['bench_a_obj'].append(card['players'][player_a_key ])
      smart_card['have_benach_a'] = True
    elif player_a_key in playing_11_a_keys:
      smart_card['playing_11_a_obj'].append(card['players'][player_a_key ])
      smart_card['have_playing_a_11'] = True
    else:
      smart_card['have_squad_a'] = True
      smart_card['playing_a_obj'].append(card['players'][player_a_key ])


  team_b_obj = card['teams']['b']['match']
  squad_b_keys = team_b_obj['players']
  playing_11_b_keys = team_b_obj['playing_xi']

  smart_card['playing_11_b_obj'] = []
  smart_card['playing_b_obj'] = []
  bench_b_keys = []
  smart_card['bench_b_obj'] = []
  # Playing 11, season squad and bench player information for Team a
  if playing_11_b_keys:
    bench_b_keys = set(squad_b_keys) - set(playing_11_b_keys)
  for player_b_key in squad_b_keys:
    captain = card['teams']['a']['match']['captain']
    keeper = card['teams']['a']['match']['keeper']
    if player_b_key == captain:
      card['players'][player_b_key]['is_captain'] = True
    if player_b_key == keeper:
      card['players'][player_b_key]['is_keeper'] = True

    if player_b_key in bench_b_keys:
      smart_card['have_benach_b'] = True
      smart_card['bench_b_obj'].append(card['players'][player_b_key ])
    elif player_b_key in playing_11_b_keys:
      smart_card['have_playing_b_11'] = True
      smart_card['playing_11_b_obj'].append(card['players'][player_b_key ])
    else:
      smart_card['have_squad_b'] = True
      smart_card['playing_b_obj'].append(card['players'][player_b_key ])
  return render(request, 'match.html', smart_card)

def scheduleHandler(request, month=None, year=None):

  data = {}

  if month and year:
    params = month + "-" + year
    schedule_data = CRICKET_API.get_schedule(params)
  else:
    schedule_data = CRICKET_API.get_schedule()

  schedule_list = []
  if schedule_data['status']:
    days = schedule_data['data']['months'][0]['days']
    for day in days:
      for match in day['matches']:
        schedule_list.append(prepare_full_caleandar_data(match))
  return render(request, 'schedule.html', 
    {
    'schedule_list' : json.dumps(schedule_list)
    })
