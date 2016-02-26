from django.shortcuts import render
import json

from . import CRICKET_API


def home(request):
  # TODO 
  match_data = CRICKET_API.get_match('iplt20_2013_g30')
  return render(request, 'match.html', match_data)
