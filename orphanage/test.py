'''
Author: Cosmic-Onion (isy)
'''

import re
import requests 
import lxml.html
import json

req = requests.Session()

URL = "http://510582159.swh.strato-hosting.eu/"

orphanages = req.get(URL).text
orphanages = lxml.html.fromstring(orphanages)

def split_country(value):
    return re.split(" - ",value)

completeJSON = []

for link in orphanages.iterlinks():
    name_country = split_country(link[0].text_content())

    charityLegalName = name_country[0]

    if len(name_country) > 1 :
        country = name_country[1]
    else:
        country = ""

    websiteUrl = link[2]

    if websiteUrl.find("#") == 0:       #internal link
        continue

    charityJSON = {
        "charityLegalName"  :   charityLegalName,
        "country"   :   country,
        "websiteUrl"    :   websiteUrl,
    }

    completeJSON.append(charityJSON)

'''
needs cleaning/better collection
'''

with open("./json/scrape0.json","w",encoding="utf8") as outfile:
    json.dump(completeJSON,outfile,ensure_ascii=False)
