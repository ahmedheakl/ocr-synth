import requests
from tqdm import tqdm
import json

url = """https://archive.org/services/search/beta/page_production/?user_query=%28language%3A%22persian%22%29+AND+Format%3A%28epub%29&hits_per_page=100&page={page}&aggregations=false&uid=R%3Af59972e025d30562e471-S%3A8df3a158cb8f821f63d4-P%3A1-K%3Ah-T%3A1755536554528&client_url=https%3A%2F%2Farchive.org%2Fsearch%3Fquery%3D%2528language%253A%2522persian%2522%2529%2BAND%2BFormat%253A%2528epub%2529"""

import math
TOTAL_ITEMS = 5000
MAX_PAGES = math.floor(TOTAL_ITEMS / 100) + 1
identifier = []
for page in tqdm(range(1, MAX_PAGES + 1)):
    url = url.format(page=page)
    data = requests.get(url).json()
    for d in data['response']['body']['hits']['hits']:
        identifier.append(d['fields']['identifier'])
        
with open("identifiers.json", "w") as f:
    json.dump(identifier, f, indent=2)