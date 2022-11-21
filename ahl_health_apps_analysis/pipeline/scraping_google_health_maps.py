from ahl_health_apps_analysis.utils.scraping_google_health_maps_utils import *


from tqdm import tqdm
import logging
from datetime import date

date = date.today()

general_search = [
'health', 
'fitness', 
'well being', 
'nutrition', 
'diet', 
'healthy eating',
'take away',
'giving up smoking',
'giving up drinking',
'cook books',
'exercise',
'loneliness']

apps_to_explore_ids  = [
'com.getsomeheadspace.android',
'com.myfitnesspal.android',
'com.heytap.health.international',
'com.wsl.noom',
'com.strava',
'com.calm.android',
'com.fitbit.FitbitMobile',
'stretching.stretch.exercises.back',
'com.spotlightsix.zentimerlite2',
'com.nike.plusgps',
'com.nike.ntc',
'com.runbuddy.prod',
'com.google.android.apps.fitness', 
'com.google.android.apps.fitness',
'com.joinzoe.results',
'com.ouraring.oura',
'com.weightwatchers.mobile',
'fi.polar.beat',
'com.downdogapp',
'com.balance_app.app',
'com.fiton.android',
'com.onepeloton.callisto']

if __name__ == "__main__":

	app_ids = search_apps(general_search) + apps_to_explore_ids

	'''Looks for similar apps many times over returned in variable named app_ids_set'''
	app_ids_set = set()
	for x in tqdm(app_ids):
		logging.info(f"Getting apps related to {x}")
		related_apps = app_snowball(x)
		if related_apps:
			app_ids_set.update(set(related_apps))


	app_details_df = get_app_info(app_ids_set)

	app_details_df.to_csv(f'inputs/data/app-ids-info-{date}.csv')








