import pandas as pd
import numpy as np
import pickle
import umap.umap_ as umap
import altair as alt
import altair_viewer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

from ahl_health_apps_analysis.utils.cluster_utils import *

if __name__ == '__main__':

	# details and description embedding is referring to the same apps 
	date = ('2022-11-28')
	details = pd.read_csv(f'outputs/data/preprocessed-description-{date}.csv')

	pickle_in = open(f'outputs/data/description-embeddings-{date}.pickle','rb')
	description_embeddings = pickle.load(pickle_in)

	# reduce word embeddings to lower dimensions
	reducer = umap.UMAP(n_components=2, random_state=1)
	embedding = reducer.fit_transform(description_embeddings)

	reducer_clustering = umap.UMAP(n_components=50, random_state=1)
	embedding_clustering = reducer_clustering.fit_transform(description_embeddings)

	def get_top_tf_idf_words(response, top_n=2, exclude_words=[]):
	    sorted_nzs = np.argsort(response.data)
	    return [word for word in feature_names[response.indices[sorted_nzs]] if word not in exclude_words][-(top_n+1):-1]

	tfidf = TfidfVectorizer(stop_words='english')


	# pick cluster type:			
	parser = create_argparser()
	args = parser.parse_args()

	app_details = details.copy()
	app_details["x"] = embedding[:, 0]
	app_details["y"] = embedding[:, 1]

	if args.cluster_type == "hdbscan":
		app_details = hdbscan_clustering(embedding_clustering, app_details)

		
	elif args.cluster_type == "kmeans":
		app_details = kmeans_clustering(embedding, app_details, n_clusters = args.n_cluster)

	else:
		print('not recognised, pick from ["hdbscan", "kmeans"]')

	cluster_description = {}
	for i, cluster in app_details.groupby('cluster'):
	    cluster_description[i] = ' '.join(cluster['description'])

	X = tfidf.fit_transform(cluster_description.values())
	feature_names = np.array(tfidf.get_feature_names())

	cluster_names = {i:"-".join(get_top_tf_idf_words(response,2,["app", "apps"])) for i, response in enumerate(X)}
	app_details['cluster_names'] = app_details['cluster'].map(cluster_names)

	
	# Visualise using altair (NB: -1=points haven't been assigned to a cluster)
	fig = (
		alt.Chart(app_details.reset_index(), width=725, height=725)
		.mark_circle(size=60)
		.encode(x="x", y="y", tooltip=["cluster_names", "appId", "summary"], color="cluster_names:N")
	).interactive()

	if args.cluster_type == "hdbscan":
		fig.save(f'outputs/figures/{date}-hdbscan-cluster.html')
		app_details.to_csv(f'outputs/data/{date}-hdbscan-cluster.csv')

	elif args.cluster_type == "kmeans":
		fig.save(f'outputs/figures/{date}-kmeans-{args.n_cluster}-cluster.html')
		app_details.to_csv(f'outputs/data/{date}-kmeans-{args.n_cluster}-cluster.csv')

	else:
		print('not recognised, pick from ["hdbscan", "kmeans"]')



