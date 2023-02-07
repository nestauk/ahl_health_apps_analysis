
# Clustering health apps from google play store 


## Follow the steps below to scrape, clean and cluster a dataset apps relevent to a health life space
1. Scrape apps using google_play_scraper API and expand current list of apps of interest with simiilar apps (ahl_health_apps_analysis/pipeline/scraping_google_health_apps.py)
2. Preprocess apps descriptions (ahl_health_apps_analysis/pipline/preprocess.py) 
3. Get a sample of the embeddings (ahl_health_apps_analysis/pipeline/create_embeddings.py)
4. Choose cluster type:
	- Cluster app details using **hdbscan** clustering (ahl_health_apps_analysis/pipeline/cluster.p --cluster_type hdbscan)
	- Cluster app details using **kmeans** clustering (ahl_health_apps_analysis/pipeline/cluster.p --cluster_type kmeans)
		- When cluster_type is kmeans choose the number of cluster_types required (ahl_health_apps_analysis/pipeline/cluster.p --cluster_type kmeans --n_cluster 20)
5. refine.py demonstates a manually examination of clusters resulting in naming, merging and splitting clusters.(ahl_health_apps_analysis/pipeline/refine.py)
6. run (ahl_health_apps_analysis/pipeline/calculate_metadata.py) to create new datasets with new metadata from calculations made from existing information:
	- app_details_ratings saved in location **f'outputs/data/{date}-{cluster_type}-{clusters}-app_details_ratings.csv'**
	- app_details_price (dataset that only includes the apps that apply installation charges) saved in location **f'outputs/data/{date}-{cluster_type}-{clusters}-app_details_price.csv')**
	- app_details_installations_joined (dataset includes information on precentage change from number of installations of apps released in 2019 to number of installations of apps released in 2021 averaged by cluster. Dates chosen to see the effect covid might of had on behaviour of customers and developers.) saved in location **f'outputs/data/{date}-{cluster_type}-{clusters}-app_details_installations.csv'**
	- app_details_release_joined (dataset includes information on percentage change from number of apps released 2019 to number of apps released 2019 avereged by cluster. Dates chosen to see the effect covid might of had on behaviour of customers and developers) **f'outputs/data/{date}-{cluster_type}-{clusters}-app_details_release_joined.csv'**


## Adjust parameter in each file before running each file to suit your specific aims.
Default Parameters:
**date** = ('2022-11-28')
**clusters** = 20
**cluster_type** = kmeans


Default name for final manually refined dataset is saved in the location **f'outputs/data/{date}-{cluster_type}-{clusters}-refined.csv'** completed in step 5 of the pipeline.
The final dataset before manually adjusting clusters and names is the dataset saved in the location **f'outputs/data/{date}-{cluster_type}-{clusters}-cluster.csv'** completed in step 4 of the pipeline.