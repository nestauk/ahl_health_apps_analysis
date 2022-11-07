import pandas as pd
import numpy as np
import pickle
import umap.umap_ as umap
import hdbscan
import logging
from sklearn.neighbors import KNeighborsClassifier
import altair as alt
import altair_viewer

date = ('2022-11-04')
details = pd.read_csv(f'outputs/data/preprocessed-description-{date}.csv')

# step 1 - load in word embeddings
pickle_in = open(f'outputs/data/description-embeddings-{date}.pickle','rb')
description_embeddings = pickle.load(pickle_in)

# step 2 - reduce word embeddings to lower dimensions
reducer = umap.UMAP(n_components=2, random_state=1)
embedding = reducer.fit_transform(description_embeddings)

reducer_clustering = umap.UMAP(n_components=50, random_state=1)
embedding_clustering = reducer_clustering.fit_transform(description_embeddings)

# step 3 - 
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

# step 4 - 
df = details.copy()
df["x"] = embedding[:, 0]
df["y"] = embedding[:, 1]
df["cluster"] = [int(x) for x in clusterer.labels_]
df["cluster_confidence"] = [str(x) for x in clusterer.probabilities_]


# step 5 - 
cluster_col = df.columns.get_loc("cluster")

radius = 3
neigh = KNeighborsClassifier(n_neighbors=radius)

current_unassigned = len(df[df.cluster == -1].cluster.to_list())

cluster_list = df.cluster.to_list()

unassigned_indices = []
unassigned_indices.extend([i for i, x in enumerate(cluster_list) if x == -1])
logging.info(f"{len(unassigned_indices)} apps not in clusters")

X_list = [x for i, x in enumerate(embedding_clustering) if i not in unassigned_indices]
y_list = [i for i in cluster_list if i != -1]

neigh.fit(X_list, y_list)

for x in unassigned_indices:
    df.iat[x, cluster_col] = neigh.predict([embedding_clustering[x]])

print(f"{len(df[df.cluster == -1].cluster.to_list())} unassigned apps remain.")

# %%
# Visualise using altair (NB: -1=points haven't been assigned to a cluster)
fig = (
    alt.Chart(df.reset_index(), width=725, height=725)
    .mark_circle(size=60)
    .encode(x="x", y="y", tooltip=["cluster", "appId", "summary"], color="cluster:N")
).interactive()

fig.show()


