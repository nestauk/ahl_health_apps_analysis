import streamlit as st
import altair as alt
import pandas as pd
from ahl_health_apps_analysis.analysis.plotting import configure_plots

date = ('2022-11-28')
clusters = 20

data = pd.read_csv(f'outputs/data/{date}-kmeans-{clusters}-refined.csv') 

similar_sectors_colors = {'Improve Sports Performance and Sports Network':"#0000FF",
'Cycle Tracker': "#FDB633",
'Mental Health':"#18A48C",
'Monitor Blood Pressure, Insulin and BMI':"#9A1BBE",
'Workout':"#FF6E47",
'Better Sleep Through Sound':"#646363",
'Hydration Reminder':"#0F294A",
'Digital Health Management':"#97D9E3",
'Dietary Management':"#A59BEE",
'Weight Loss/Diet':"#F6A4B7",
'Quit Smoking or Drinking':"#D2C9C0",
'Manage Health Information and Medication':"#000000",
'Food Delivery':"#0000FF",
'Health Information Source':"#FDB633",
'Recipes and Meal Kits':"#18A48C"}

original_title = '<p style="font-family:Courier; color:Black; font-size: 60px;">Mapping Health Apps</p>'

st.markdown(original_title, unsafe_allow_html=True)

st.write('From mindfulness to diet tracking, health apps have the potential to help people lead healthier lives. To find out which healthy living areas are represented in the apps space we have created a dataset of health apps from the Google Play Store and used natural language processing (NLP) techniques to plot the apps in 2D space and cluster them into 15 themes. This plot will allow you to investigate these apps, where the closer two apps are shown on the plot the more similar their descriptions are. The repo for Mapping Health Apps exists can be found [here](https://github.com/nestauk/ahl_health_apps_analysis/pull/5).')

cluster_selected = st.multiselect("Select cluster", data['cluster_names'].unique(),default = data['cluster_names'].unique())
selected_data = data[data['cluster_names'].isin(cluster_selected)]

app_selected = st.selectbox("Select app", selected_data['title'].unique())
selected_app_data = selected_data[selected_data['title']==app_selected] 


st.write(f'Number of apps : {len(selected_data)}')

fig = alt.Chart(selected_data.reset_index(), width=725, height=725).mark_circle(size=60).encode(
	x=alt.X("x", axis=alt.Axis(labels=False, grid=False), title="x"), 
	y=alt.Y("y", axis=alt.Axis(labels=False, grid=False), title="y"), 
	tooltip=[alt.Tooltip("title"), alt.Tooltip("summary", title = "Summary"), alt.Tooltip("realInstalls", title = 'Number of Installs'), alt.Tooltip("score", title = 'Average App Rating'), alt.Tooltip("developer", title = 'Developer')],
	color=alt.Color(
            "cluster_names",
            scale=alt.Scale(
                domain=list(similar_sectors_colors.keys()),
                range=list(similar_sectors_colors.values()),
            ),
            legend=alt.Legend(title=""),
        ))


fig2 = alt.Chart(selected_app_data.reset_index()).mark_circle(size=300, color='red').encode(
	x="x", 
	y="y", 
	tooltip=[alt.Tooltip("title"), alt.Tooltip("summary", title = "Summary"), alt.Tooltip("realInstalls", title = 'Number of Installs'), alt.Tooltip("score", title = 'Average App Rating'), alt.Tooltip("developer", title = 'Developer')])

st.altair_chart(configure_plots(fig + fig2), use_container_width=True)














