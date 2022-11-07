import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle

if __name__ == "__main__":

	'''date in form yyyy-mm-dd'''
	date = '2022-11-04'
	details = pd.read_csv(f'outputs/data/preprocessed-description-{date}.csv')

	model = SentenceTransformer("all-mpnet-base-v2")

	# Generate sentence embeddings (might take a few minutes for 1000s of sentences)
	description_embeddings = np.array(model.encode(details.description.to_list()))

	embedding_ids = details["appId"].iloc[:].to_list()

	with open(f'outputs/data/description-embeddings-{date}.pickle', "wb") as f:
	    pickle.dump(description_embeddings, f)

