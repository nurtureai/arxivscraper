import getopt
import arxivscraper
import sys

def main():
	println("running...")
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
	if args.size >= 1:
		cat = args[0]
	date_from = ""
	date_to = ""
	if args.size >= 2:
		date_from = args[1]

	if args.size >= 3:
		date_to = args[2]

	println("fetching category: "+cat+", from: "+date_from+", to: "+date_to)
	scraper = arxivscraper.Scraper(category=cat, date_from=date_from,date_until=date_to)
	out = scraper.scrape()
	print(out)

