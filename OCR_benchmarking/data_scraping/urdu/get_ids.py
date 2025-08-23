import requests
from tqdm import tqdm
import json


url = "https://archive.org/services/search/beta/page_production/?user_query=&page_type=collection_details&page_target=ibteda&hits_per_page=100&page={page}&aggregations=false&uid=R%3Ac10d7a43414d1dcee372-S%3A12e75fdafef68b104b14-P%3A1-K%3Ah-T%3A1755453242237&client_url=https%3A%2F%2Farchive.org%2Fdetails%2Fibteda"

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