import csv
import pickle

from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

with open('netflix_titles.pickle', 'rb') as handle:
	recommendations = pickle.load(handle)

with open('netflix_titles.csv') as f:
	dataset = [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]


def item(id):
	return dataset.loc[dataset['show_id'] == id]['description'].tolist()[0].split(' - ')[0]


@app.route("/")
def hello():
	return render_template('index.html', shows=dataset)

if __name__ == "__main__":
	app.run()
