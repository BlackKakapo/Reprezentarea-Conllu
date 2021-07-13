import io
# import spacy
import csv
from flask import Flask, render_template, request
# from spacy import displacy
from graphviz import Digraph
from conllu import parse_incr
from conllu import parse


app = Flask(__name__)


@app.route('/', methods = ['GET', 'POST'])
def index():
	conllu = ''
	svg = ''

	if request.method == 'POST':
		if request.form['func'] == '1':		
			conllu = request.form['conllu']
			print(conllu)
			svg = propDisplaySpacy(conllu)
			return render_template('index.html', conllu = conllu, svg = svg)

		elif request.form['func'] == '2':
			conllu = request.form['conllu']
			print(conllu)
			svg = propDisplayGraph(conllu)
			return render_template('index.html', conllu = conllu, svg = svg)


	return render_template('index.html', conllu = conllu)




def propDisplayGraph(connlu):

	sentences = parse(connlu)

	listOfID = []
	listOfHead = []
	listOfString = []

	sentence = sentences[0]
	for i in range(0,len(sentence)):
		token = sentence[i]
		listOfID.append(token['id'])
		listOfHead.append(token['head'] - 1)
		listOfString.append(token['form'])

	dot = Digraph(comment='The Round Table', format = 'svg')

	subgraph = Digraph(comment='The Round Table')
	subgraph.attr(rank='same')
	
	for i in range(0,len(listOfHead) - 1):
		subgraph.edge(str(listOfString[i]), str(listOfString[i + 1]))

	for i in range(0,len(listOfHead)):
		if str(listOfString[listOfHead[i]]) == '0':
			continue
		else:
			subgraph.edge(str(listOfString[i]), str(listOfString[listOfHead[i]]))
			continue

	dot.subgraph(subgraph)

	dot.format = 'svg'
	dot.render()  
	svg = dot.pipe().decode('utf-8').strip()
	return svg


# def propDisplaySpacy(conllu):
# 	nlp = spacy.load("ro_core_news_lg")
# 	doc1 = nlp(conllu)
# 	options = {"compact": True, "bg": "white","color": "black", "font": "Source Sans Pro"}
# 	svg = displacy.render(doc1, style="dep", page=False, options=options)
# 	return svg

if __name__ == "__main__":
	app.run(debug=True)