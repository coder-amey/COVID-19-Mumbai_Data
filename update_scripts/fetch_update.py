'''This script loads the worksheet of the TIFR for updates on COVID-19 spread in Mumbai and stores the latest tally in the time-series dataset and regenerates the corresponding CSV file.'''

import pandas as data
import requests
import os.path

base_dir = os.path.join(os.path.dirname(__file__), "../")		#Obtain the path to the base directory for absosulte addressing.

#Tabulate the Worksheet data.
raw_data = requests.get('https://docs.google.com/spreadsheet/ccc?key=1-OYukZzMlRcRKfMqh-pAle0JYAjLjUy08N9V6S51sq0&output=csv')
raw_data = raw_data.content.decode().split('\r\n')
time_series = data.DataFrame([row.split(',') for row in raw_data[1:]], columns = raw_data[0].split(','))

#Rename and format the required columns and drop the rest.
time_series.index = data.to_datetime(time_series.Date, dayfirst = True)
time_series = time_series.rename(columns = {"Cumulative Cases": "Confirmed", "Cumulative Recovered": "Recovered/Migrated", "Cumulative Deaths": "Deceased"})
time_series = time_series[["Confirmed", "Recovered/Migrated", "Deceased"]]
time_series = time_series.astype({"Confirmed": int, "Recovered/Migrated": int, "Deceased": int})

#Store the time-series to a CSV file.
time_series.to_csv(base_dir + "time-series/Mumbai_aggregated.csv")