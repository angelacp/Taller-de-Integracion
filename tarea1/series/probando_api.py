import requests
import pandas as pd
from datetime import datetime

name = 'w'
r = requests.get('https://tarea-1-breaking-bad.herokuapp.com/api/characters?name='+name)
df = pd.DataFrame.from_dict(r.json())

for i,d in df.iterrows():
	print(d['name'])