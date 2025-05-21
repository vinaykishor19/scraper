# scraper.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

# --------------- GURU JOB SCRAPER ---------------
def scrape_guru_jobs():
    """
    Scrapes job listings from Guru.com.
    Returns:
        pd.DataFrame: A DataFrame containing job title, budget, description, skills, etc.
    """
    URL = 'https://www.guru.com/d/jobs'
    try:
        r = requests.get(URL, timeout=10)
        r.raise_for_status()  # Raise HTTPError if status is 4xx or 5xx
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch Guru jobs: {e}")
        return pd.DataFrame()

    soup = BeautifulSoup(r.content, 'html5lib')
    list_items = soup.select('ul.module_list > li')
    data = []

    for li in list_items:
        h2 = li.find('h2', class_='jobRecord__title')
        title = h2.get_text(strip=True) if h2 else 'N/A'
        url = h2.find('a')['href'] if h2 and h2.find('a') else 'N/A'

        budget_div = li.find('div', class_='jobRecord__budget')
        budget = budget_div.get_text(strip=True) if budget_div else 'N/A'

        desc_p = li.find('p', class_='jobRecord__desc')
        desc = desc_p.get_text(strip=True) if desc_p else 'N/A'

        skills_div = li.find('div', class_='skillsList')
        skills = ', '.join(a.get_text(strip=True) for a in skills_div.find_all('a')) if skills_div else 'N/A'

        data.append({
            'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Title': title,
            'URL': url,
            'Budget': budget,
            'Description': desc,
            'Skills': skills
        })

    return pd.DataFrame(data)


# --------------- PEOPLEPERHOUR FREELANCERS SCRAPER ---------------
def scrape_pph_freelancers():
    """
    Scrapes freelancer profiles from PeoplePerHour.com.
    Returns:
        pd.DataFrame: A DataFrame with freelancer title, budget, description, and skills.
    """
    URL = 'https://www.peopleperhour.com/hire-freelancers'
    try:
        r = requests.get(URL, timeout=10)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch PeoplePerHour freelancers: {e}")
        return pd.DataFrame()

    soup = BeautifulSoup(r.content, 'html5lib')
    list_items = soup.select('div.pph-row--nested > ul > li')
    data = []

    for li in list_items:
        h2 = li.find('h2', class_='title-nano')
        title = h2.get_text(strip=True) if h2 else 'N/A'
        url = li.find('a')['href'] if li and li.find('a') else 'N/A'

        budget_div = li.find('div', class_='u-txt--right')
        budget = budget_div.get_text(strip=True) if budget_div else 'N/A'

        desc_p = li.find('p', class_='u-mgb--1')
        desc = desc_p.get_text(strip=True) if desc_p else 'N/A'

        skills_div = li.find('ul', class_='u-mgb--0')
        skills = ', '.join(a.get_text(strip=True) for a in skills_div.find_all('a')) if skills_div else 'N/A'

        data.append({
            'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Title': title,
            'URL': url,
            'Budget': budget,
            'Description': desc,
            'Skills': skills
        })

    return pd.DataFrame(data)


# --------------- MAIN EXECUTION ---------------
def main():
    """
    Main function that scrapes data from both platforms
    and saves them into two separate Excel files.
    """
    # Call scraping functions
    guru_df = scrape_guru_jobs()
    pph_df = scrape_pph_freelancers()

    # Define file paths
    guru_file = 'guru_jobs_data.xlsx'
    pph_file = 'freelancer_data.xlsx'

    # Save Guru job data
    if not guru_df.empty:
        guru_df.to_excel(guru_file, index=False)
        print("✅ Guru job data saved to:", guru_file)
    else:
        print("⚠️ No Guru job data scraped.")

    # Save PeoplePerHour freelancer data
    if not pph_df.empty:
        pph_df.to_excel(pph_file, index=False)
        print("✅ Freelancer data saved to:", pph_file)
    else:
        print("⚠️ No freelancer data scraped.")

# Python entry point
if __name__ == '__main__':
    main()
