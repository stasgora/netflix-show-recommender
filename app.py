import csv
import pickle

from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

with open('netflix_titles.pickle', 'rb') as handle:
	recommendations = pickle.load(handle)

with open('netflix_titles.csv') as f:
	dataset = [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]
	dataset_map = {d['show_id']: d for d in dataset}


@app.route("/")
def main_page():
	results = dataset
	for_id = request.args.get('for')
	if for_id is not None:
		results = list(map(lambda t: dataset[t[1]], recommendations[for_id][:6]))

	query = request.args.get('query')
	if query is not None and query:
		results = list(filter(lambda x: x['title'].lower().find(query.lower()) >= 0, results))
	return render_template('index.html', shows=results, query=(query if query else ''), title=(dataset_map[for_id]['title'] if for_id else None))


if __name__ == "__main__":
	app.run()
