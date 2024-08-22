from scraping.scraper import get_jobs, scrape
import time
import csv


keywords = [
    "flutter",
    "nextjs",
    "kotlin"
]

for keyword in keywords:
    scrape_content = get_jobs(keyword)
    jobs = scrape(scrape_content, keyword)