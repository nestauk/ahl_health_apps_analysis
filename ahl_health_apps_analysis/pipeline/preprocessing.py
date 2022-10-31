from ahl_health_apps_analysis.utils.preprocessing_utils import *

import pandas as pd

if __name__ == "__main__":
	details = pd.read_csv('inputs/data/app_ids_list_27-10.csv')


	details['description'] = details['descriptionHTML']
	details.drop(columns = 'descriptionHTML')

	# step 1 - replace with space
	details.dropna(subset = 'description', inplace= True)

	# step 2 - replace with space
	details['description'] = details['description'].apply(lambda x:replace_dash(x))

	# step 3 - remove emojis
	details['description'] = details['description'].apply(lambda x:remove_emojis(x))	                        

	#step 4 - replace html tags with space
	details['description'] = details['description'].apply(lambda x:remove_html_flags(x))



	details.to_csv('outputs/data/preprocessed_description_27-10.csv')

