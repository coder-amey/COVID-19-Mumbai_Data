'''This script generates the predictions for COVID-19 spread in Mumbai and stores the results in the predictions CSV file.'''

from datetime import datetime
import numpy as maths
import pandas as data
import os.path
from utility import *

base_dir = os.path.join(os.path.dirname(__file__), "../")		#Obtain the path to the base directory for absosulte addressing.

#Load the time-series.
time_series = data.read_csv(base_dir + "time-series/Mumbai_aggregated.csv")
time_series.Date = data.to_datetime(time_series.Date, dayfirst =True)

#Create the days-to-double dataframe.
predictions = data.DataFrame(columns = ["Date", "CNF_1D", "CNF_1W", "CNF_2W", "DCS_1D", "DCS_1W", "DCS_2W"], data = maths.zeros([time_series.Date.size, 7]))
predictions.Date = time_series.Date

#Alternative approach for predictions with insufficient data.
#predictions.CNF_1D = predictions.CNF_1W = predictions.CNF_2W = time_series.Confirmed
#predictions.DCS_1D = predictions.DCS_1W = predictions.DCS_2W = time_series.Deceased

#Calculate and store the predictions for each date. [Vectorized approach]
for samples, suffix in zip([n_samples, 7 * n_samples, 14 * n_samples], ["1D", "1W", "2W"]):
	cnf_predictables = []
	cnf_matrix =[]
	dcs_matrix = []
	dcs_predictables = []
	for date in time_series.Date.tolist()[samples:]:		#Select entries with sufficient historical samples.
		vector = time_series[time_series.Date <= date].Confirmed.tolist()
		if(vector[-samples] > 0):		#Ensure that only non-zero entries are passed.
			cnf_predictables.append(date)
			cnf_matrix.append(vector[-samples:])

		vector = time_series[time_series.Date <= date].Deceased.tolist()
		if(vector[-samples] > 0):		#Ensure that only non-zero entries are passed.
			dcs_predictables.append(date)
			dcs_matrix.append(vector[-samples:])

	pred_index = samples + (samples / n_samples) - 1		#Input index for querying a prediction.
	#Predict new infections:
	raw_predictions = maths.rint(exp_predict(pred_index, *exp_reg(cnf_matrix)))
	for date, pred in zip(cnf_predictables, raw_predictions):
		predictions.loc[predictions.Date == date, f"CNF_{suffix}"] = pred

	#Predict new deaths:
	raw_predictions = maths.rint(exp_predict(pred_index, *exp_reg(dcs_matrix)))
	for date, pred in zip(dcs_predictables, raw_predictions):
		predictions.loc[predictions.Date == date, f"DCS_{suffix}"] = pred

#Format the columns.
predictions.Date = data.to_datetime(predictions.Date, dayfirst = True)
predictions = predictions.astype({"CNF_1D": int,"CNF_1W": int,"CNF_2W": int,"DCS_1D": int,"DCS_1W": int,"DCS_2W": int})

#Store the days-to-double series to a CSV file.
predictions.to_csv(base_dir + "time-series/Mumbai_predictions.csv", index = False)