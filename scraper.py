import getopt
import arxivscraper

import sys

def main():
	print("running...")
	try:
		opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
	except getopt.GetoptError as err:
		print(err)
		print("for help use --help")
		sys.exit(2)
	# process options

	for o, a in opts:
		if o in ("-h", "--help"):
			print("example: python scrapper.py ['category'] [date_from:yyyy-mm-dd] [date_to:yyyy-mm-dd]")
			sys.exit(0)

	cat = ""
	if len(args) >= 1:
		cat = args[0]
	date_from = ""
	date_to = ""
	if len(args) >= 2:
		date_from = args[1]

	if len(args) >= 3:
		date_to = args[2]

	print("fetching category: "+cat+", from: "+date_from+", to: "+date_to)
	scraper = arxivscraper.Scraper(category=cat, date_from=date_from,date_until=date_to)
	ds = scraper.scrape()
	for row in ds:
		print(row.output())


if __name__ == '__main__':
	main()
