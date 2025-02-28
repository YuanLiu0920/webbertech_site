import json
import requests

url = 'https://www.sec.gov/edgar/browse/?cik=1350694'
r = requests.get(url)
print(r.json())