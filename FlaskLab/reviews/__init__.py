import os
from flask import Flask
from flask import render_template
import reviews.solrinterface as solr

def create_app(test_config=None):
	# create and configure the app
	app = Flask(__name__, instance_relative_config=True)
	
	app.config.from_mapping(
		SECRET_KEY='dev',
	)

	if test_config is None:
		# load the instance config, if it exists, when not testing
		app.config.from_pyfile('config.py', silent=True)
	else:
		# load the test config if passed in
		app.config.from_mapping(test_config)

	# ensure the instance folder exists
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass
	
	###################################
	## Application code begins
	@app.route('/', methods=['GET'])
	def index():
		return render_template('index.html')
		
	@app.route('/hello/<inputName>', methods=['GET'])
	def hello(inputName):
		return render_template('hello.html', tname=inputName)

	@app.route('/searchresults', methods=['GET'])
	def searchResults():
		res = solr.test_review_search()
		if res['numFound'] == 0:
			r = 'Not found'
		else:
			r = res['docs']
		return render_template('searchresults.html', res = r)

	@app.route('/idlookup/<reviewid>', methods=['GET'])
	def idLookup(reviewid):
		idDetail = solr.test_id_search('2c7cf845-cb08-4afe-bbba-2f46b467e99c')
		doc = idDetail['docs'][0]
		id = doc['id']
		return render_template('reviewdetail.html', id=id, doc=doc )
	
	## Application code ends
	##############################
	return app
