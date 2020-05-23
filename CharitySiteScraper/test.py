import requests
import lxml.html
import json
import re

req = requests.Session()

headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0",
            "referer": "https://www.google.com"}

dir_list = ["about", "about-us", "aboutus"]

with open("./json/AUwebsites.json") as website_json:
    websites_load = json.load(website_json)

    for charity in websites_load:
        website = charity["charityWebsite"]
        charity_legal_name = charity["charityLegalName"]

        site_get = req.get(website,headers=headers)

        if site_get.status_code == 200:
            root_html = lxml.html.fromstring(site_get.text)
            print(root_html)
            #iterlinks() and look for any img with class "logo" or suchlike, and links for social media, email
            #get text_content() look for large strings of numbers prefixed with fax or telephone
            #ping url + dir_list check if response is 200 or redirect 
