
# Clustering health apps from google play store 

1. Scrape apps using google_play_scraper API and expand current list of apps of interest with simiilar apps (ahl_health_apps_analysis/pipeline/scraping_google_health_apps.py)
2. Preprocess apps descriptions (ahl_health_apps_analysis/pipline/preprocess.py) 
3. Get a sample of the embeddings (ahl_health_apps_analysis/pipeline/create_embeddings.py)
4. Cluster app details using hdbscan (ahl_health_apps_analysis/pipeline/hdbscan_cluster.py)
4. or cluster app details using kmeans (ahl_health_apps_analysis/pipeline/kmeans_cluster.py)