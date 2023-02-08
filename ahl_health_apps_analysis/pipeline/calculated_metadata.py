import pandas as pd
import numpy as np


date = ('2022-11-28')
clusters = 20
cluster_type = kmeans

app_details = pd.read_csv(f'outputs/data/{date}-{cluster_type}-{clusters}-refined.csv')



#app_details_ratings
app_details_ratings = app_details[app_details['ratings'] != 0]


#
app_details_2021 = app_details[app_details['year'] == 2021]
app_details_2019 = app_details[app_details['year'] == 2019]


#app_details_price
app_details_price = app_details.groupby('cluster_names', as_index=False)['free'].value_counts(normalize = True)
app_details_price['proportion'] = app_details_price['proportion']*100
app_details_price = app_details_price[app_details_price['free']!=0]


#app_details_installations_joined
app_details_2021_installed = app_details_2021.groupby('cluster_names')['daily_installs'].mean().reset_index()
app_details_2019_installed = app_details_2019.groupby('cluster_names')['daily_installs'].mean().reset_index()

app_details_installations_joined = pd.merge(app_details_2019_installed, app_details_2021_installed, on = ['cluster_names'], how = 'outer')
app_details_installations_joined.rename(columns = {'daily_installs_x': '2019','daily_installs_y':'2021'}, inplace = True)

diff_installed = app_details_installations_joined['2021'] - app_details_installations_joined['2019']
app_details_installations_joined['percentage_diff'] = diff_installed/app_details_installations_joined['2019']*100


#app_details_installations_joined
app_details_2021_released = app_details_2021.groupby('cluster_names')['year'].count().reset_index().rename(columns={'year':'released'})
app_details_2019_released = app_details_2019.groupby('cluster_names')['year'].count().reset_index().rename(columns={'year':'released'})


app_details_release_joined = pd.merge(app_details_2019_released, app_details_2021_released, on = ['cluster_names'], how = 'outer')
app_details_release_joined.rename(columns = {'released_x': '2019','released_y':'2021'}, inplace = True)

diff_released = app_details_release_joined['2021'] - app_details_release_joined['2019']
app_details_release_joined['percentage_diff'] = diff_released/app_details_release_joined['2019']*100

app_details_ratings.to_csv(f'outputs/data/{date}-{cluster_type}-{clusters}-app_details_ratings.csv')
app_details_price.to_csv(f'outputs/data/{date}-{cluster_type}-{clusters}-app_details_price.csv')
app_details_installations_joined.to_csv(f'outputs/data/{date}-{cluster_type}-{clusters}-app_details_installations.csv')
app_details_release_joined.to_csv(f'outputs/data/{date}-{cluster_type}-{clusters}-app_details_release.csv')