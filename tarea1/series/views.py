from django.shortcuts import render
from series.models import Season, Episode, Character
import requests
import pandas as pd 
from datetime import datetime, date

# Create your views here.
def index(request):
	r = requests.get('https://tarea-1-breaking-bad.herokuapp.com/api/episodes?series=Breaking+Bad')
	df = pd.DataFrame.from_dict(r.json())
	bb_set = set((row['series'], row['season']) for index, row in df.iterrows())
	bb = []
	for s in bb_set:
		season = Season(season_id=s[1], serie=s[0])
		bb.append(season)
	bb.sort(key=lambda x: x.season_id)

	r = requests.get('https://tarea-1-breaking-bad.herokuapp.com/api/episodes?series=Better+Call+Saul')
	df = pd.DataFrame.from_dict(r.json())
	bcs_set = set((row['series'], row['season']) for index, row in df.iterrows())
	bcs = []
	for s in bcs_set:
		season = Season(season_id=s[1], serie=s[0])
		bcs.append(season)
	bcs.sort(key=lambda x: x.season_id)
	
	context = {'bb': bb, 'bcs': bcs} # Diccionario para enviar info al template
	
	return render(request, 'index.html', context)


def season_detail(request, serie, season_id):
	#season = Season.objects.get(pk=pk) # Query q retorna la season con primary key pk
	#serie = serie.name.replace(' ','+')
	season_id = str(season_id)
	r = requests.get('https://tarea-1-breaking-bad.herokuapp.com/api/episodes?series='+serie)
	df = pd.DataFrame.from_dict(r.json())
	episodes = []
	for i,d in df.iterrows():
 		if d['season'] == season_id:
 			episode = Episode(episode_id = d['episode_id'],
 							  title = d['title'],
 							  season = d['season'],
 							  episode = d['episode'],
 							  air_date = datetime.strptime(d['air_date'], '%Y-%m-%dT00:00:00.000Z').date(),
 							  characters = d['characters'],
 							  series = d['series'])
 			episodes.append(episode)
	#print(episodes)
	context = {'episodes': episodes, 'series': serie, 'season_id': season_id}
	return render(request, 'season_detail.html', context)

def character_detail(request, name):
	r = requests.get('https://tarea-1-breaking-bad.herokuapp.com/api/characters?name='+name)
	df = pd.DataFrame.from_dict(r.json()).iloc[0]
	character = Character(character_id = df['char_id'],
						  name = df['name'],
						  occupation = ', '.join(df['occupation']),
						  img = df['img'],
						  status = df['status'],
						  nickname = df['nickname'],
						  appearance = df['appearance'],
						  better_call_saul_appearance = df['better_call_saul_appearance'],
						  portrayed = df['portrayed'],
						  category = df['category'])
	context = {'character': character}
	return render(request, 'character_detail.html', context)


def search_character (request):
	name = request.GET.get('q','')
	r = requests.get('https://tarea-1-breaking-bad.herokuapp.com/api/characters?name='+name)
	df = pd.DataFrame.from_dict(r.json())
	print(df)
	characters = []
	for i,d in df.iterrows():
		character = Character(character_id = d['char_id'],
							  name = d['name'],
							  occupation = ', '.join(d['occupation']),
							  img = d['img'],
							  status = d['status'],
							  nickname = d['nickname'],
							  appearance = d['appearance'],
							  better_call_saul_appearance = d['better_call_saul_appearance'],
							  portrayed = d['portrayed'],
							  category = d['category'])
		characters.append(character)
	context = {'characters': characters}
	return render(request, 'search_character.html', context)