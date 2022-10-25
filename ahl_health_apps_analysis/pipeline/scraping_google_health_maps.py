from ahl_health_apps_analysis.utils.scraping_google_health_maps_utils import *


from tqdm import tqdm
import logging

general_search = [
'health', 
'fitness', 
'well_being', 
'nutrition', 
'diet', 
'healthy eating']

apps_to_explore  = [
'Headspace',
'MyFitnessPal',
'HealthTap',
'Noom',
'Strava',
'Calm',
'Fitbit',
'Stretching Exercises - Flexibility',
'Insight Timer',
'Nike Running App',
'Nike Training Club',
'Runna',
'Apple health app', 
'Google fit',
'ZOE',
'Clue',
'Oura',
'WW app',
'Polar Flow',
'Down Dog',
'Balance',
'Fiton',
'Peloton']



app_ids = search_apps(general_search,30) + search_apps(apps_to_explore)



'''Looks for similar apps many times over returned in variable named app_details_set'''
app_details_set = set()
for x in tqdm(app_ids[:1]):
    logging.info(f"Getting apps related to {x}")
    related_apps = app_snowball(x)
    if related_apps:
        app_details_set.update(set(related_apps))


app_details_df = load_all_app_ids(app_details_set)

app_details_df.to_csv('inputs/data/app_ids_list_5.csv')








