from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from .file import save_to_file
import time

def get_jobs(keyword):
    p = sync_playwright().start()

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto(f"https://www.wanted.co.kr/search?query={keyword}&tab=position")

    for x in range(5):
        time.sleep(5)
        page.keyboard.down("End")

    content = page.content()

    p.stop()

    return content

def scrape(content, keyword):
    soup = BeautifulSoup(content, "html.parser")
    jobs = soup.find_all("div", class_="JobCard_container__REty8")

    jobs_db = []

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
        jobs_db.append(job)

    print("Job has been added to the database!")
    save_to_file(keyword, jobs_db)

