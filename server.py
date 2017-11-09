import os
import subprocess
import tempfile
import logging
import urllib
import arxivscraper
import json
from flask import Flask, Response, request, redirect, url_for, abort, send_file, jsonify
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
  print("arxivscrapper v1.6")
  cat = request.args.get('c')
  date_from = request.args.get('from')
  date_to = request.args.get('to')
  start = int(request.args.get("start", 0))
  limit = int(request.args.get("limit", 20))
  proxy = request.args.get("proxy" "")

  scraper = arxivscraper.Scraper(category=cat, date_from=date_from,date_until=date_to)
  if proxy is not "":
    print("setting proxy: ", proxy)
    scraper.setProxy(proxy)# example: http://xx.xx.xx.xx:80/

  try:
    # print("fetching category: "+cat+", from: "+date_from+", to: "+date_to)
    return Response(generate(scraper, limit), content_type='application/json')

  except Exception as e:
    return jsonify({error: e.message}), status.HTTP_500_INTERNAL_SERVER_ERROR

  # return jsonify(ds)
def processing_finished():
  return False

def generate(scraper, limit):
  index = 0
  """
  A lagging generator to stream JSON so we don't have to hold everything in memory
  This is a little tricky, as we need to omit the last comma to make valid JSON,
  thus we use a lagging generator, similar to http://stackoverflow.com/questions/1630320/
  """
  # We have some releases. First, yield the opening json
  batchSize = -1
  ds = scraper.scrape(batchSize, 0)
  yield "[\n"

  while (limit == -1 or index < limit) and len(ds) > 0:
    if processing_finished():
      return
    if len(ds) < batchSize or len(ds) == 0:
      # print("size ds below", batchSize)
      break

    for i in ds:
      if limit > -1 and index > limit:
        break
      if index > 0:
        yield ",\n"
      # print("i", i)
      # print(".")
      # print(json.dumps(i), "\n")
      if processing_finished():
        return
      yield json.dumps(i)
      index += 1

    if limit > -1 and index >= limit:
      break

    if not scraper.hasNext():
      print("no more next")
      break

    if limit > -1:
      ds = scraper.next(limit - index)
    else:
      ds = scraper.next(-1)

  yield "]\n"


if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0')
