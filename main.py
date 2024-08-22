from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time
import csv

class WantedScrapper:
    def __init__(self, keyword):
        self.jobs_db = []
        self.keyword = keyword
    
    def get_jobs(self):
        p = sync_playwright().start()

        browser = p.chromium.launch(headless=False)

        page = browser.new_page()

        page.goto(f"https://www.wanted.co.kr/search?query={self.keyword}&tab=position")

        for x in range(5):
            time.sleep(5)
            page.keyboard.down("End")

        content = page.content()

        p.stop()

        return content
    
    def scrape(self):
        content = self.get_jobs()
        soup = BeautifulSoup(content, "html.parser")
        jobs = soup.find_all("div", class_="JobCard_container__REty8")

        self.jobs_db = []

        for job in jobs:
            link = f"https://www.wanted.co.kr{job.find('a')['href']}"
            title = job.find("strong", class_="JobCard_title__HBpZf").text
            company_name = job.find("span", class_="JobCard_companyName__N1YrF").text
            reward = job.find("span", class_="JobCard_reward__cNlG5").text
            job = {
                "title": title,
                "company_name": company_name,
                "reward": reward,
                "link": link
            }
            self.jobs_db.append(job)
            print("Job has been added to the database!")

    def export_csv(self, keyword):
        file = open(f"{keyword}-jobs.csv", "w")
        writer = csv.writer(file)
        writer.writerow(["Title", "Company", "Reward", "Link"])

        for job in self.jobs_db:
            writer.writerow(list(job.values()))

        file.close()

        print('CSV file has been created!')

keywords = [
    "flutter",
    "nextjs",
    "kotlin"
]

for keyword in keywords:
    scrapper = WantedScrapper(keyword)
    scrapper.scrape()
    scrapper.export_csv(keyword)