from django.shortcuts import render

from . import CRICKET_API


def homeHandler(request):
  recent_matches_data = CRICKET_API.get_recent_matches("summary_card")
  recent_matches_data = recent_matches_data['data']['cards']
  recent_matches = {  'not_started_matches' : [], 
                      'started_matches': [], 
                      "completed_matches": []
                    }
  for recent_matche_data in recent_matches_data:
    if recent_matche_data['status'] == 'notstarted':
      recent_matches['not_started_matches'].append(recent_matche_data)
    elif recent_matche_data['status'] == 'started':
      recent_matches['started_matches'].append(recent_matche_data)
    else:
      recent_matches['completed_matches'].append(recent_matche_data)

  return render(request, 'home.html', recent_matches)

def matchHandler(request, match_key): 
  match_data = CRICKET_API.get_match(match_key)
  card = match_data['data']['card']
  return render(request, 'match.html', card)