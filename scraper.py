# scraper.py


import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

# -------- PEOPLEPERHOUR FREELANCER SCRAPER --------

def scrape_pph_freelancer_hourlies():
    base_url = 'https://www.peopleperhour.com/hire-freelancers?page={}'
    data = []

    # Fixed range: pages 1 to 10
    for page in range(1, 11):
        page_url = base_url.format(page)
        print(f"Scraping page {page}: {page_url}")

        try:
            r = requests.get(page_url, timeout=10)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch page {page}: {e}")
            continue

        soup = BeautifulSoup(r.content, 'html5lib')
        list_items = soup.select('div.pph-row--nested > ul > li')

        for li in list_items:
            h2 = li.find('h2', class_='title-nano')
            title = h2.get_text(strip=True) if h2 else 'N/A'
            url = li.find('a')['href'] if li and li.find('a') else 'N/A'
            budget_div = li.find('div', class_='u-txt--right')
            budget = budget_div.get_text(strip=True) if budget_div else 'N/A'
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            skills = 'N/A'
            hourlies_combined = 'N/A'
            member_stats_combined = 'N/A'
            corrected_title = title

            if url:
                try:
                    profile_r = requests.get(url, timeout=10)
                    profile_r.raise_for_status()
                    profile_soup = BeautifulSoup(profile_r.text, 'html5lib')

                    details_div = profile_soup.find('div', class_='details')
                    if details_div:
                        h1_tag = details_div.find('h1')
                        if h1_tag:
                            for p in h1_tag.find_all('p'):
                                p.decompose()
                            corrected_title = h1_tag.get_text(strip=True)

                    skills_div = profile_soup.find('div', class_='clearfix widget-tag-list')
                    if skills_div:
                        skill_tags = skills_div.find_all('a')
                        skills = ', '.join(tag.get_text(strip=True) for tag in skill_tags)

                    tab_content_div = profile_soup.find('div', class_='tab-content')
                    if tab_content_div:
                        hourlie_wrappers = tab_content_div.find_all('div', class_='hourlie-wrapper')
                        hourlies = []
                        for wrapper in hourlie_wrappers:
                            desc = wrapper.find('div', class_='hourlie__description')
                            price = wrapper.find('div', class_='hourlie__price')
                            if desc and price:
                                desc_text = desc.get_text(strip=True)
                                price_text = price.get_text(strip=True)
                                hourlies.append(f"{desc_text} - {price_text}")
                        hourlies_combined = ', '.join(hourlies) if hourlies else 'N/A'

                    member_stats_section = profile_soup.find('section', class_='widget-memberStats')
                    if member_stats_section:
                        member_items = member_stats_section.find_all('div', class_='memberStats-item')
                        stats = []
                        for item in member_items:
                            label = item.find('div', class_='insights-label')
                            value = item.find('div', class_='insights-value')
                            if label and value:
                                stats.append(f"{label.get_text(strip=True)} - {value.get_text(strip=True)}")
                        member_stats_combined = ', '.join(stats) if stats else 'N/A'

                except Exception as ex:
                    print(f"Failed to fetch profile ({url}): {ex}")

            data.append({
                'Timestamp': timestamp,
                'Title': corrected_title,
                'URL': url,
                'Budget': budget,
                'Skills': skills,
                'Hourlies': hourlies_combined,
                'Member Stats': member_stats_combined
            })

    return pd.DataFrame(data)



# -------- GURU JOB SCRAPER --------
def scrape_guru_jobs():
    base_url = 'https://www.guru.com/d/jobs/pg/{}/'
    data = []
    start_page = 1
    max_pages = None

    # First request to get max page number
    first_url = base_url.format(start_page)
    try:
        r = requests.get(first_url, timeout=10)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch Guru jobs page {start_page}: {e}")
        return pd.DataFrame()

    soup = BeautifulSoup(r.content, 'html5lib')

    # Get max page number from pagination
    pagination_div = soup.find('div', class_='pagination')
    if pagination_div:
        page_links = pagination_div.find_all('a')
        page_numbers = [
            int(link.get_text(strip=True)) for link in page_links
            if link.get_text(strip=True).isdigit()
        ]
        if page_numbers:
            max_pages = max(page_numbers)
    if not max_pages:
        print("Could not determine total number of pages. Defaulting to page 1 only.")
        max_pages = 1

    # Loop through all pages
    for page in range(1, max_pages + 1):
        url = base_url.format(page)
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch Guru jobs page {page}: {e}")
            continue

        soup = BeautifulSoup(r.content, 'html5lib')
        list_items = soup.select('ul.module_list > li')

        for li in list_items:
            h2 = li.find('h2', class_='jobRecord__title')
            title = h2.get_text(strip=True) if h2 else 'N/A'
            relative_url = h2.find('a')['href'] if h2 and h2.find('a') else 'N/A'
            full_url = f"https://www.guru.com{relative_url}" if relative_url != 'N/A' else 'N/A'

            budget_div = li.find('div', class_='jobRecord__budget')
            budget = budget_div.get_text(strip=True) if budget_div else 'N/A'
            desc_p = li.find('p', class_='jobRecord__desc')
            desc = desc_p.get_text(strip=True) if desc_p else 'N/A'
            skills_div = li.find('div', class_='skillsList')
            skills = ', '.join(a.get_text(strip=True) for a in skills_div.find_all('a')) if skills_div else 'N/A'

            data.append({
                'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'Title': title,
                'URL': full_url,
                'Budget': budget,
                'Description': desc,
                'Skills': skills
            })

    return pd.DataFrame(data)




# -------- SAVE TO EXCEL --------
def save_to_excel(df, filename):
    folder_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(folder_path, filename)

    try:
        df.to_excel(file_path, index=False)
        print(f"Data saved to {file_path}")
    except PermissionError:
        print(f"Cannot write to {file_path}. Please close the file if it's open.")

if __name__ == "__main__":
    # Scrape and save PeoplePerHour freelancer data
    pph_df = scrape_pph_freelancer_hourlies()
    if not pph_df.empty:
        save_to_excel(pph_df, 'peopleperhour_freelancer_data.xlsx')
    else:
        print("No PeoplePerHour data scraped.")

    # Scrape and save Guru jobs data
    guru_df = scrape_guru_jobs()
    if not guru_df.empty:
        save_to_excel(guru_df, 'guru_jobs_data.xlsx')
    else:
        print("No Guru job data scraped.")

