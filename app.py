import io
import csv
# import spacy
# from spacy import displacy
from flask import Flask, render_template, request
from graphviz import Digraph
from conllu import parse_incr
from conllu import parse


app = Flask(__name__)


@app.route('/', methods = ['GET', 'POST'])
def index():
	return render_template('index.html', conllu = conllu)



@app.route('/GraphvizConvertor.html', methods = ['GET', 'POST'])
def graphConvertor():
	conllu = ''

	if request.method == 'POST':
		conllu = request.form['conllu']
		svg = propDisplayGraph(conllu)
		return render_template('GraphvizConvertor.html', conllu = conllu, svg = svg)

	return render_template('GraphvizConvertor.html')


@app.route('/SpacyConvertor.html', methods = ['GET', 'POST'])
def spaCyConvertor():
	if request.method == 'POST':		
		prop = request.form['prop']
		svg = propDisplaySpacy(prop)
		return render_template('SpacyConvertor.html', prop = prop, svg = svg)

	return render_template('SpacyConvertor.html')


def propDisplayGraph(connlu):

	try:

		sentences = parse(connlu)

		listOfID = []
		listOfHead = []
		listOfString = []
		listOfUPOS = []

		sentence = sentences[0]
		for i in range(0,len(sentence)):
			token = sentence[i]
			listOfID.append(token['id'] - 1)
			listOfHead.append(token['head'] - 1)
			listOfString.append(token['form'])
			listOfUPOS.append(token['upos'])

		dot = Digraph(comment='The Round Table', format = 'svg')
		dot.graph_attr['rankdir'] = 'LR'

		subgraph = Digraph(comment='The Round Table')
		# subgraph.attr(rank='same')
		subgraph.edge_attr['style'] = 'invis'
		
		for i in range(0,len(listOfHead) - 1):
			subgraph.edge(str(listOfString[i]), str(listOfString[i + 1]))

		for i in range(0,len(listOfHead) - 1):
			if str(listOfHead[i]) == '-1':
				continue
			elif str(listOfUPOS[i]) == 'PUNCT':
				continue				
			else:
				dot.edge(str(listOfString[i]), str(listOfString[listOfHead[i]]))		

		dot.subgraph(subgraph)

		dot.format = 'svg'
		dot.render()  
		svg = dot.pipe().decode('utf-8').strip()
		return svg
	except:
		return "Incorrect format"


# def propDisplaySpacy(prop):
# 	if prop != None:
# 		nlp = spacy.load("ro_core_news_sm")
# 		doc1 = nlp(prop)
# 		options = {"compact": True, "bg": "white","color": "black", "font": "Source Sans Pro"}
# 		svg = displacy.render(doc1, style="dep", page=False, options=options)
# 		return svg
# 	else:
# 		return "Incorrect format"

if __name__ == "__main__":
	app.run(debug=True)