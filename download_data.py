#Get list of links to download from TfL

import json
import urllib2
import pandas as pd
import requests 

url = 'http://cycling.data.tfl.gov.uk/cycling-load.json'
data = json.load(urllib2.urlopen(url))
df = pd.DataFrame.from_dict(data, orient='columns', dtype=None)

#Extract urls from dict
links = pd.concat([df, pd.DataFrame((d for idx, d in df['entries'].iteritems()))], axis=1)
del links['entries']
links

#Convert to string
pd.DataFrame.to_string(links)

#Get clean link for download
links['url_clean'] = links['url'].str.slice(start=5)
links.head(5)

#Convert to list
urls_to_call = links['url_clean'].tolist()
urls_to_call

#Download files!
for url in urls_to_call:
    filename = url[43:len(url)]
    r = requests.get(url)
    with open(filename, "wb") as code:
        code.write(r.content)
