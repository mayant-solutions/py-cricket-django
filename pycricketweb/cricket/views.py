from django.shortcuts import render

from datetime import datetime
from . import CRICKET_API


def homeHandler(request):
  recent_matches_data = CRICKET_API.get_recent_matches("summary_card")

  recent_matches_data = recent_matches_data['data']['cards']
  smart_cards = prepare_smart_cards(recent_matches_data)
  return render(request, 'home.html', smart_cards)


def seasonHandler(request, season_key):
  season_data = CRICKET_API.get_season(season_key)
  season_matches = season_data['data']['season']['matches']
  season_matches_list = []
  for key ,season_match in season_matches.items():
    season_matches_list.append(season_match)
  smart_cards = prepare_smart_cards(season_matches_list)
  return render(request, 'home.html', smart_cards)


def matchHandler(request, match_key): 
  match_data = CRICKET_API.get_match(match_key)
  card = match_data['data']['card']
  
  if card['status'] == 'completed':
    smart_card = create_match_completed_data(card)
  elif card['status'] == 'started':
    smart_card = create_match_started_card(card) 
  else:
    smart_card = create_match_notstated_data(card)

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

def create_match_started_card(card):

  data = {}

  run_rate = ""
  data['nonstriker_runs'] = ""
  data['striker_runs'] = ""
  data['bowler_runs'] = "Waiting for bowler"
  data['bowler_name'] = ""
  data['nonstriker_name'] = ""
  data['striker_name'] = ""

  now = card['now']
  data['runs_str'] = now['runs_str']
  
  batting_team = now['batting_team']
  bowling_team = now['bowling_team']
  data['status'] = card['status']
  data['key'] = card['key']
  data['short_name'] = card['short_name']
  data['team_a_name'] = card['teams']['a']['name']
  data['team_b_name'] = card['teams']['b']['name']
  data['bat_team_name'] = card['teams'][batting_team]['short_name']
  data['bowl_team_name'] = card['teams'][bowling_team]['short_name']
  data['run_rate'] = now['run_rate']
  data['req_obj'] = now['req']
  data['now'] = datetime.now()

  nonstriker = now['nonstriker']
  striker = now['striker']
  bowler = now['bowler']

  if nonstriker:
    data['nonstriker_name'] = card['players'][nonstriker]['name']
    if card['players'][nonstriker]['match']['innings'][now['innings']]['batting']:
      data['nonstriker_runs'] = str(card['players'][nonstriker]['match']['innings'][now['innings']]['batting']['runs']) + \
          "(" + str(card['players'][nonstriker]['match']['innings'][now['innings']]['batting']['balls']) +")"
    else:
      data['nonstriker_runs'] += "0(0)"
  else:
    data['nonstriker_runs'] += "Waiting for batsman"


  if striker:
    data['striker_name'] = card['players'][striker]['name']
    if card['players'][striker]['match']['innings'][now['innings']]['batting']:
      data['striker_runs'] = str(card['players'][striker]['match']['innings'][now['innings']]['batting']['runs']) + \
          "(" + str(card['players'][striker]['match']['innings'][now['innings']]['batting']['balls']) +")"
    else:
      data['striker_runs'] += "0(0)"
  else:
    data['striker_runs'] += "Waiting for batsman"

  
  if bowler:
    data['bowler_name'] = card['players'][bowler]['name']
    data['bowler_runs'] = str(card['players'][bowler]['match']['innings'][now['innings']]['bowling']['runs']) + \
                        "/" + str(card['players'][bowler]['match']['innings'][now['innings']]['bowling']['wickets']) \
                       + " in " + str(card['players'][bowler]['match']['innings'][now['innings']]['bowling']['overs'])


  data['over'] = str(now['balls'] / 6) + "." + str(now['balls'] % 6)

  data['recent_overs_str'] = []
  recent_overs_balls = now['recent_overs'][0][1]

  extra_types =  {'noball' : 'nb', 'wide':'wd', 'legbye':'lg', 'bye':'by'}
   
  for recent_ball_key in recent_overs_balls:
    ball = {}
    recent_ball = card['balls'][recent_ball_key]
    recent_overs_str = ""

    if recent_ball['wicket']:
      ball['class'] = 'w'
      recent_overs_str += "W"

    if recent_ball['ball_type'] == 'normal':
      if recent_ball['wicket'] and recent_ball['batsman']['runs'] == 0:
        recent_overs_str += ""
      else:
        recent_overs_str += str(recent_ball['batsman']['runs']) + " "
      if recent_ball['batsman']['runs'] == 4:
        ball['class'] = 'b4'
      if recent_ball['batsman']['runs'] == 6:
        ball['class'] = 'b6'

    if recent_ball['ball_type'] in extra_types:
      recent_overs_str +=  str(recent_ball['extras']) + " " + extra_types[recent_ball['ball_type']]

    ball['recent_overs_str'] = recent_overs_str
    data['recent_overs_str'].append(ball) 

  if now['last_ball']['comment']:
    data['comment'] = now['last_ball']['comment']
  elif card['toss'] and 'str' in card['toss']:
    data['comment'] = card['toss']['str']

  return data

def create_match_notstated_data(card):
  data = {}
  data['start_date_obj'] = datetime.fromtimestamp(card['start_date']['timestamp'])
  data['short_name'] = card['short_name']
  data['team_a_name'] = card['teams']['a']['name']
  data['team_b_name'] = card['teams']['b']['name']
  data['start_date_str'] = card['teams']['b']['name']
  data['related_name'] = card['related_name']
  data['status'] = card['status']
  data['key'] = card['key']

  timestamp_date = card['start_date']['timestamp']
  date = datetime.fromtimestamp(timestamp_date)
  data['datetime_obj'] = date
  data['now'] = datetime.now()
  return data

def create_match_completed_data(card):
  data = {}
  man_of_match_key = card['man_of_match']

  possible_innings = ['1', '2', 'superover']
  team_a_possible_innings = ['a_1', 'a_2', 'a_superover']
  team_b_possible_innings = ['b_1', 'b_2', 'b_superover']
  data['mom_runs'] = ""
  data['mom_boundries'] = ""
  data['mom_wickets'] = ""
  data['team_a_run_str'] = ""
  data['team_b_run_str'] = ""
  data['mom_name'] = ""
  data['start_date_obj'] = datetime.fromtimestamp(card['start_date']['timestamp'])
  data['team_a_name'] = card['teams']['a']['name']
  data['team_b_name'] = card['teams']['b']['name']
  data['related_name'] = card['related_name']
  data['completed_msg'] = card['msgs']['completed']
  data['status'] = card['status']
  data['key'] = card['key']
  data['now'] = datetime.now()
  data['mom_key'] = man_of_match_key


  if man_of_match_key:
    man_of_match_obj = card['players'][man_of_match_key]
    data['mom_key'] = man_of_match_key
    data['mom_name'] = man_of_match_obj['name']
    innings = man_of_match_obj['match']['innings']
 
    for index, team_inn in enumerate(team_a_possible_innings):
      if index == 1 and team_inn in card['innings'] and \
                        card['innings'][team_inn]['runs'] and \
                        card['innings'][team_inn]['balls']:
        data['team_a_run_str'] += " & "
      if team_inn in card['innings'] and card['innings'][team_inn] and \
         card['innings'][team_inn]['runs'] and card['innings'][team_inn]['balls']:
        data['team_a_run_str'] += card['innings'][team_inn]['run_str']

    for index, team_inn in enumerate(team_b_possible_innings):
      if index == 1 and team_inn in card['innings'] and \
                    card['innings'][team_inn]['runs'] and \
                    card['innings'][team_inn]['balls']:
        data['team_b_run_str'] += " & "
      if team_inn in card['innings'] and card['innings'][team_inn] and \
         card['innings'][team_inn]['runs'] and card['innings'][team_inn]['balls']:
        data['team_b_run_str'] += card['innings'][team_inn]['run_str']

    for inn_number in  possible_innings:
      if inn_number in innings:
        innings_1_bat = innings[inn_number]['batting']
        innings_1_bowl = innings[inn_number]['bowling']

        if innings[inn_number]['batting']:
          if inn_number == '2' or inn_number == 'superover':
            data['mom_runs'] += " & "
            data['mom_boundries'] += " & "
          data['mom_runs'] += str(innings_1_bat['runs']) + "(" + \
                                  str(innings_1_bat['balls']) + ")"

          data['mom_boundries'] += str(innings_1_bat['fours']) + "x4  " + \
                                str(innings_1_bat['sixes']) + "x6"

        if innings[inn_number]['bowling']:
          if inn_number == '2' or inn_number == 'superover':
            data['mom_wickets'] += " & "

          data['mom_wickets'] += str(innings_1_bowl['runs']) + "/" + \
                                str(innings_1_bowl['wickets']) +\
                                " (" + str(innings_1_bowl['overs']) + \
                                " ov)"

    if not data['mom_runs']:
      data['mom_runs'] = "nill"
    if not data['mom_boundries']:
      data['mom_boundries'] = "nill"
    if not data['mom_wickets']:
      data['mom_wickets'] = "nill"

  return data

def prepare_smart_cards(matches):
  smart_match_data = []
  for match in matches:
    match_data = CRICKET_API.get_match(match['key'])
    match_data = match_data['data']['card']
    if match_data['status'] == 'completed':
      smart_match_data.append(create_match_completed_data(match_data))
    elif match_data['status'] == 'started':
      smart_match_data.append(create_match_started_card(match_data))
    else:
      smart_match_data.append(create_match_notstated_data(match_data))

  smart_cards = {'smart_cards': smart_match_data}
  return smart_cards
