
# Clustering health apps from google play store 

1. Scrape apps using google_play_scraper API and expand current list of apps of interest with simiilar apps (ahl_health_apps_analysis/pipeline/scraping_google_health_apps.py)
2. Preprocess apps descriptions (ahl_health_apps_analysis/pipline/preprocess.py) 
3. Get a sample of the embeddings (ahl_health_apps_analysis/pipeline/create_embeddings.py)
4. Choose cluster type:
	- Cluster app details using hdbscan clustering (ahl_health_apps_analysis/pipeline/cluster.p --cluster_type hdbscan)
	- Cluster app details using kmeans clustering (ahl_health_apps_analysis/pipeline/cluster.p --cluster_type kmeans)