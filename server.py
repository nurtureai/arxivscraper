import os
import subprocess
import tempfile
import logging
import urllib
import arxivscraper
from flask import Flask, request, redirect, url_for, abort, send_file, jsonify
from flask_api import status
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
  start = int(request.args.get("start", 0))
  limit = int(request.args.get("limit", 20))

  try:
    # print("fetching category: "+cat+", from: "+date_from+", to: "+date_to)
    scraper = arxivscraper.Scraper(category=cat, date_from=date_from,date_until=date_to)
    ds = scraper.scrape(limit, start)
  except Exception as e:
    return jsonify({error: e.message}), status.HTTP_500_INTERNAL_SERVER_ERROR

  return jsonify(ds)

if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0')
