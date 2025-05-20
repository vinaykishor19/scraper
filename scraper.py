import requests

from bs4 import BeautifulSoup
import pandas as pd

URL = 'https://www.guru.com/d/jobs'
r = requests.get(URL)

soup = BeautifulSoup(r.content, 'html5lib')


soup.prettify()

list_items = soup.select('ul.module_list > li')

data = []

for li in list_items:
    
    # h2 with class jobRecord__title
    h2 = li.find('h2', class_='jobRecord__title')
    title = h2.get_text(strip=True) if h2 else 'N/A'
    
    # URL inside the <a> inside h2
    url = h2.find('a')['href'] if h2 and h2.find('a') else 'N/A'
    
    # div with class jobRecord__budget
    budget_div = li.find('div', class_='jobRecord__budget')
    budget = budget_div.get_text(strip=True) if budget_div else 'N/A'
    
    # p with class jobRecord__desc
    desc_p = li.find('p', class_='jobRecord__desc')
    desc = desc_p.get_text(strip=True) if desc_p else 'N/A'
    
    # all anchor tags inside div.skillsList, joined by commas
    skills_div = li.find('div', class_='skillsList')
    if skills_div:
        skills = [a.get_text(strip=True) for a in skills_div.find_all('a')]
        skills_joined = ', '.join(skills)
    else:
        skills_joined = 'N/A'

    data.append({
    'Title': title,
    'URL': url,
    'Budget': budget,
    'Description': desc,
    'Skills': skills_joined
    })

df = pd.DataFrame(data)

print(df)
