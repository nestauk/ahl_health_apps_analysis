
from google_play_scraper import search
from google_play_scraper import app
import pandas as pd
from tqdm import tqdm




def search_apps(search_term_list, n_hits = 5):

    '''Input list of app names, defaulted to return the top 5 apps from each search name in list, this can be altered but the maximum n_hits is 30'''

    app_ids = []
    for search_name in search_term_list:
        results = search(search_name,
                        lang="en",  
                        country="uk",  
                        n_hits=n_hits 
        )
        for result in results:
            app_ids.append(result['appId'])
    return app_ids



def get_app_info(app_ids):
    """
    Gets app information for a list of app ids
    """
    app_ids_df = []
    number_errors = 0
    for app_id in tqdm(app_ids):
        try:
          result = app(
            app_id,
            lang='en',
            country='uk')
          app_ids_df.append(result)
        except:
           number_errors += 1
    print(f"Number of apps that errored: {number_errors} out of {len(app_ids)}")
    return pd.DataFrame(app_ids_df)



def app_snowball(seed_app_id: str, depth: int = 5, __current_depth: int = 1) -> list:
    """
    Retrieves ids of Play Store apps related to `seed_app_id` by calling itself recursively.

    Args:
        seed_app_id: str - the app id of the app of interest
        depth: int, default = 5 - the depth of recursion. This will increase the number of apps interrogated (and
        therefore the time taken for the initial call to complete) exponentially
        __current_depth: used for recursion, should be left blank by user

    Returns:
        a list of app ids
    """

    try:
        app_details = app(seed_app_id)
        similar_apps = app_details["similarApps"]
    except:
        return False

    snowball = set([seed_app_id])
    try:
        snowball.update(similar_apps)
    except:
        return False
    if (__current_depth < depth) and (similar_apps is not None):
        for this_app in similar_apps:
            next_step_results = app_snowball(this_app, depth, (__current_depth + 1))
            if next_step_results:
                snowball.update(next_step_results)     
                     
    return list(snowball)




