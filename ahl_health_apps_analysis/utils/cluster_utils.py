import hdbscan
import logging
from argparse import ArgumentParser
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

def create_argparser():

		parser = ArgumentParser()
		parser.add_argument('--cluster_type', help="Type of cluster", default="kmeans", type=str)
		parser.add_argument('--n_cluster', help="Number of clusters", default="15", type=int)
		return parser

def hdbscan_clustering(embedding_clustering, app_details):

	np.random.seed(3667)
	clusterer = hdbscan.HDBSCAN(
		min_cluster_size=20,
		min_samples=1,
		cluster_selection_method="leaf",
		prediction_data=True,
	)
	clusterer.fit(embedding_clustering)
	logging.info(
		f"{len(set(clusterer.labels_))} clusters with {sum([bool(x) for x in clusterer.labels_ if int(x) == -1])} unassigned apps"
	)
 
	app_details["cluster"] = [int(x) for x in clusterer.labels_]
	app_details["cluster_confidence"] = [str(x) for x in clusterer.probabilities_]

	# assign unassigned apps to their nearest cluster
	cluster_col = app_details.columns.get_loc("cluster")

	radius = 3
	neigh = KNeighborsClassifier(n_neighbors=radius)

	current_unassigned = len(app_details[app_details.cluster == -1].cluster.to_list())

	cluster_list = app_details.cluster.to_list()

	unassigned_indices = [i for i, x in enumerate(cluster_list) if x == -1]
	logging.info(f"{len(unassigned_indices)} apps not in clusters")

	X_list = [x for i, x in enumerate(embedding_clustering) if i not in unassigned_indices]
	y_list = [i for i in cluster_list if i != -1]

	neigh.fit(X_list, y_list)

	for x in unassigned_indices:
		app_details.iat[x, cluster_col] = neigh.predict([embedding_clustering[x]])

	print(f"{len(app_details[app_details.cluster == -1].cluster.to_list())} unassigned apps remain.")

	return app_details

def kmeans_clustering(embedding, app_details, n_clusters = 15):
	clusterer = KMeans(n_clusters=n_clusters)
	y_predicted = clusterer.fit_predict(embedding).tolist()

	
	app_details["cluster"] = [int(x) for x in y_predicted]
	return app_details


