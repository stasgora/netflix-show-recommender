import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

dataset = pd.read_csv("netflix_titles.csv")

tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
matrix = tf.fit_transform(dataset['description'])

cosine_similarities = linear_kernel(matrix, matrix)

recommendations = {}

for idx, row in dataset.iterrows():
	similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
	similar_items = [(cosine_similarities[idx][i], dataset['show_id'][i]) for i in similar_indices]

	recommendations[row['show_id']] = similar_items[1:]

with open('netflix_titles.pickle', 'wb') as handle:
	pickle.dump(recommendations, handle, protocol=pickle.HIGHEST_PROTOCOL)
