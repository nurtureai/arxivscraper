# ArxivScrapper

## Usage

* docker run arxivscraper category date_from date_to
* examples: 
** docker run --rm nurtureai/arxivscraper run cs.AI 2017-01-01
** docker run -p 5005:5005 arxivscraper server
*** curl "127.0.0.1:5005/crawl?c=cs&from=2017-01-01&to=2017-10-01"
** docker run --rm -v "$PWD:/home/app/box" -i -t nurtureai/arxivscraper sh
*** cd /home/app/box && python scraper.py 'cs.AI' '2017-01-01' '2017-09-31'


## development build
* docker build -t arxivscraper .


## deployment
* docker build -t nurtureai/arxivscraper
* docker push nurtureai/arxivscraper

## latest & credit:
* https://github.com/Mahdisadjadi/arxivscraper
