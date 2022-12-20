from ahl_health_apps_analysis.utils.preprocessing_utils import *
from langdetect import detect

import pandas as pd

if __name__ == "__main__":
	'''date in format YYYY-MM-DD'''
	date = '2022-11-28'
	details = pd.read_csv(f'inputs/data/app-ids-info-{date}.csv')

	details['description'] = details['descriptionHTML']
	details.drop(columns = 'descriptionHTML')

	# step 1 - drop nulls
	details.dropna(subset = 'description', inplace= True)

	# step 2 - replace with space
	details['description'] = details['description'].apply(lambda x:replace_dash(x))

	# step 3 - remove emojis
	details['description'] = details['description'].apply(lambda x:remove_emojis(x))	                        

	#step 4 - replace html tags with space
	details['description'] = details['description'].apply(lambda x:remove_html_flags(x))

	#step 5 - filtering by relevent apps to health
	details = details[(details['genre'] == 'Health & Fitness') | (details['genre'] == 'Food & Drink') | (details['genre'] == 'Medical') | (details['genre'] == 'Sports')].reset_index()

	#step 6 - keep english apps
	details['language'] = details['description'].apply(detect)
	details = details[details['language'] == 'en']


	details.to_csv(f'outputs/data/preprocessed-description-{date}.csv')

