import requests
import pandas as pd
import xml.etree.ElementTree as ET
import gspread
from gspread_dataframe import set_with_dataframe
import time

def obtain_data(country):
	print(country)
	
	x = requests.get('http://tarea-4.2021-1.tallerdeintegracion.cl/gho_{}.xml'.format(country))
	file = open('gho_{}.xml'.format(country), 'w')
	file.write(x.text)
	file.close()

	tree = ET.parse('gho_{}.xml'.format(country))
	root = tree.getroot()

	col = ['GHO', 'COUNTRY', 'SEX', 'YEAR', 'GHECAUSES', 'AGEGROUP', 
			 'Display', 'Numeric', 'Low', 'High']
	data = []
	for fact in root.findall('Fact'):
		line = []
		for c in col:
			try:
				node = fact.find(c).text #.replace('.',',')
			except AttributeError:
				node = None
			line.append(node)
		data.append(line)

	df = pd.DataFrame(data=data, columns=col)
	print(df.shape)
	return df

def export_spreadsheets(df):
	gc = gspread.service_account(filename='tarea4-angelacp-5be54505e12d.json')
	sh = gc.open_by_key('1F6NJ-ATTHuBmraMWI1S_ub4XA6mDb28YX503zDxLzB8')
	worksheet = sh.get_worksheet(0)
	worksheet.clear()
	set_with_dataframe(worksheet, df)

# México MEX, Chile CHL, Japón JPN, Sudáfrica ZAF, Rusia RUS y España ESP
df_mex = obtain_data('MEX')
df_chl = obtain_data('CHL')
df_jpn = obtain_data('JPN')
df_zaf = obtain_data('ZAF')
df_rus = obtain_data('RUS')
df_esp = obtain_data('ESP')

df = pd.concat([df_mex, df_chl, df_jpn, df_zaf, df_rus, df_esp])

export_spreadsheets(df)

