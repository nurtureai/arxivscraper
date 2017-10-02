# ArxivScrapper

## Usage

* docker run arxivscraper category date_from date_to
* example: docker run --rm nurtureai/arxivscraper run cs.AI 2017-01-01
* example: docker run --rm nurtureai/arxivscraper serve

## development build
* docker build -t arxivscraper .


## deployment
* docker build -t nurtureai/arxivscraper
* docker push nurtureai/arxivscraper
