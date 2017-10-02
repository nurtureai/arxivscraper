import os
import subprocess
import tempfile
import logging
import urllib
import arxivscraper
from flask import Flask, request, redirect, url_for, abort, send_file
from werkzeug import secure_filename

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = set(['pdf'])

app = Flask(__name__)
app.config.from_pyfile('config.py')

logging.getLogger().setLevel(logging.INFO)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/crawl')
def crawl():
	cat = request.args.get('c')
  date_from = request.args.get('from')
  date_to = request.args.get('to')

  println("fetching category: "+cat+", from: "+date_from+", to: "+date_to)
	scraper = arxivscraper.Scraper(category=cat, date_from=date_from,date_until=date_to)
	out = scraper.scrape()
	print(out)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
