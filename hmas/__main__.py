import json
from hmas import scrape


for proxy in scrape():
    print json.dumps(proxy)
