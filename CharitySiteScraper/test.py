import requests
import lxml.html
import json
import re

req = requests.Session()

headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0",
            "referer": "https://www.google.com"}

about_list = ["about", "about-us", "about_us"]
contact_list = ["contact", "contact_us", "contact_us"]

website_json = open("./json/AUwebsites.json")
websites_load = json.load(website_json)
website_json.close()

def find_external_link(search_term,value):
    return re.match(search_term,value)

for charity in websites_load:
    website = charity["charityWebsite"] 
    '''
    TODO: 
    facebook links,
    https;//example.com,
    multiple entries, seperated by ;
    commas replaced with "." unless after "?"
    replace "\#" with "/"
    replace "wwww" & "ww" with "www"
    '''
    if website.find("http") == -1:      
        website = "http://" + website    #https may not be available, security doesn't matter so much for get
    print(website)

    with open("bruh.txt","a") as txtfile:
        txtfile.write(website+"\n")
    continue

    charity_legal_name = charity["charityLegalName"]

    try:
        site_get = req.get(website,headers=headers)
    except:
        #TODO: logic to tell calling file that site link is
        continue

    if site_get.status_code == 200 || 300:
        root_html = lxml.html.fromstring(site_get.text)
        # print(root_html)
        for link in root_html.iterlinks():
            link_url = link[2]

            #print(link_url)
        #iterlinks() and look for any img with class "logo" or suchlike, and links for social media, email
        #get text_content() look for large strings of numbers prefixed with fax or telephone
        #ping url + dir_list check if response is 200 or redirect 
    else:
        #TODO: add flag that site is down
        continue