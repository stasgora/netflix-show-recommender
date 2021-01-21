import sys

import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


class DatasetProcessor(object):
	def __init__(self, file):
		self.recommendations = {}
		self.dataset = pd.read_csv(file)

	def create_recommendations(self):
		matrix = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english').fit_transform(self.dataset['description'])
		kernel = linear_kernel(matrix, matrix)

		for idx, row in self.dataset.iterrows():
			similar_indices = kernel[idx].argsort()[:-50:-1]
			similar_items = [(kernel[idx][i], i) for i in similar_indices]
			self.recommendations[row['show_id']] = similar_items[1:]

	def save_as_pickle(self, file):
		with open(file, 'wb') as handle:
			pickle.dump(self.recommendations, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
	processor = DatasetProcessor(sys.argv[1])
	processor.create_recommendations()
	processor.save_as_pickle('netflix_titles.pickle')
