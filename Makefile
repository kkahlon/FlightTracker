.SILENT:

scrape:
	echo "Beginning to scrape"
	python3 Scraper.py
	echo "Scraping complete"

clean:
	echo "No files set to be removed"
