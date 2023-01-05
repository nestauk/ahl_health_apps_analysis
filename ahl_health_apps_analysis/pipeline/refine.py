import pandas as pd
import numpy as np
import altair as alt
import altair_viewer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer 
from datetime import datetime 
from ahl_health_apps_analysis.analysis.plotting import configure_plots


date = ('2022-11-28')
clusters = 20
app_details = pd.read_csv(f'outputs/data/{date}-kmeans-{clusters}-cluster.csv')

re_cluster0 = ['com.bm.android.thermometer',
 'com.contraction.kicks',
 'com.woomfertility.woomapp',
 'com.proov',
 'premom.eh.com.ehpremomapp',
 'org.femmhealth.femm',
 'com.clue.android',
 'com.ovuline.parenting',
 'ovulation.calculator.period.calendar.tracker.fertility.menstrual.apex',
 'com.endometrix.endometrix',
 'com.tamtris.fertilityfriend',
 'com.insanedevelopers.periodtracker']

drop_list = ['com.castlighthealth.returntowork',
 'my.foodhub.ms',
 'com.ckr.hardeesstickers',
 'com.speedway.mobile',
 'com.ckr.carlsjrstickers',
 'com.geonaute.geyeconnect',
 'fi.polar.equine',
 'com.adidas.gmr',
 'com.chiaro.elviepump',
 'com.ggtude.te',
 'com.f45tv.f45powerandroid.live',
 'com.kicksonfire.android',
 'com.riatech.diabeticrecipes',
 'es.nooddle',
 'pl.mb.rest',
 'com.solutran.healthysavings',
 'com.twcsports.android',
 'air.com.nbcuni.com.telemundo.envivo',
 'com.buchdeals.cardbase',
 'com.paninidigitalinc.blitz',
 'de.motain.iliga',
 'com.rotoql.express',
 'com.handmark.sportcaster',
 'net.paniniamerica.direct',
 'com.tennisrn',
 'com.theathletic',
 'com.gotv.nflgamecenter.us.lite',
 'com.espn.score_center',
 'com.ihssntv',
 'com.decathlon.canaveral.v1',
 'app.collx.android',
 'com.bleachr.tennisone',
 'com.virtualrepetitions.playbook.basketball',
 'com.arkeapps.fantasylifecom.tipstersprime.tipster.reviews',
 'co.sayshell.halftime',
 'com.padelmates',
 'com.codexen.fantasyfootball',
 'air.com.nbcuni.com.nbcsports.liveextra',
 'com.espn.fantasy.lm.football',
 'com.foxsports.android',
 'com.dazn',
 'tv.mycujoo.mycujooplayer',
 'weightloss.women.diet.lose_weight - weight loss diet app',
 'com.droidinfinity.compareapp',
 'uk.co.disciplemedia.cvgnation',
 'com.ymca.universalapp',
 'com.mindbodyonline.express',
 'strong.vibrator.massage.vibration.forwomen',
 'com.jgdevlabs.vibra',
 'com.mile.mythalassa',
 'com.healme',
 'nl.deckeron.apps.innerfire']

# drop apps in drop_list 
for app in drop_list:
    app_details = app_details[app_details.appId != app]

'''Refining clusters and renaming cluster_names'''
#re-cluster 0 to 20 and rename cluster 
app_details[app_details.appId.isin(re_cluster0)] = app_details[app_details.appId.isin(re_cluster0)].replace({'cluster':0},20)
app_details[app_details.appId.isin(re_cluster0)] = app_details[app_details.appId.isin(re_cluster0)].replace({'cluster_names':'fertility-health'},'Cycle Tracker')

#re-name cluster 0 
app_details[app_details.cluster ==0] = app_details[app_details.cluster ==0].replace({'cluster_names':'fertility-health'},'Manage Health Information and Medication') 

# Recipees cluster 1,7,9
app_details =app_details.replace({'cluster_names':['cooking-recipe']},'Recipes and Meal Kits')
app_details =app_details.replace({'cluster_names':'calorie-food'}, 'Dietary Management')
app_details =app_details.replace({'cluster_names':'keto-recipes'}, 'Weight Loss/Diet')

# Workout: cluster 2,5,12,14,15
app_details =app_details.replace({'cluster_names':['training-workouts', 
                                 'walking-training', 
                                 'fitness-workouts', 
                                 'workouts-fitness',
                                 'workout-classes']},'Workout')
# Mental Health: cluster 3,13,16
app_details =app_details.replace({'cluster_names':['therapy-anxiety', 
                                 'health-mental', 
                                 'minapp_detailsulness-meditations']},'Mental Health')

app_details =app_details.replace({'cluster_names':'players-tennis'}, 'Improve Sports Performance and Sports Network')

app_details =app_details.replace({'cluster_names':'drinking-drink'}, 'Hydration Reminder')

app_details =app_details.replace({'cluster_names':'weight-pressure'}, 'Monitor Blood Pressure, Insulin and BMI')

app_details =app_details.replace({'cluster_names':'rate-health'}, 'Digital Health Management')

app_details =app_details.replace({'cluster_names':'nclex-anatomy'}, 'Health Information Source')

app_details =app_details.replace({'cluster_names':'restaurants-order'}, 'Food Delivery')

app_details =app_details.replace({'cluster_names':'hearing-sounds'}, 'Better Sleep Through Sound')

app_details =app_details.replace({'cluster_names':'hypnosis-quit'}, 'Quit Smoking or Drinking')

#Re-number clusters
cluster_names_list = app_details['cluster_names'].unique().tolist()

cluster_names_mapping={}
for cluster_name,i in enumerate(cluster_names_list):
    cluster_names_mapping[i] = cluster_name
    
app_details['cluster'] = app_details['cluster_names'].map(cluster_names_mapping)

# 
app_details['released'] = pd.to_datetime(pd.Series(app_details['released']))
app_details['current_date'] = datetime.strptime(date, "%Y-%m-%d")
app_details['app_duration'] = app_details['current_date'] - app_details['released']
app_details['app_duration_days'] = app_details['app_duration'].dt.days
app_details['daily_installs'] = app_details['realInstalls']/app_details['app_duration_days']
app_details = app_details.drop(columns = 'app_duration')
app_details['total_apps_per_cluster'] = app_details.groupby('cluster_names')['appId'].transform('count')
app_details['year'] = pd.to_datetime(app_details['released']).dt.year


#plotting
fig = configure_plots(
    alt.Chart(app_details.reset_index(), width=725, height=725)
    .mark_circle(size=60)
    .encode(x="x", y="y", tooltip=["cluster_names", "appId", "summary", 'description'], color="cluster_names:N")
).interactive()

# save pandas and fig
app_details.to_csv(f'outputs/data/{date}-kmeans-{clusters}-refined.csv') 
fig.save(f'outputs/data/{date}-kmeans-{clusters}-refined.html')


