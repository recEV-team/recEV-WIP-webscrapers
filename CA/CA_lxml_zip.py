'''
Author: Cosmic-Onion (Isy)
'''
import gevent.monkey
gevent.monkey.patch_all()
import re
import requests
import lxml.html
import json
import math
import zipfile
import grequests
from lxml.html.clean import Cleaner
from flask import Flask, jsonify, Response

'''
The search engine is unavailable between 02:00 a.m. and 06:00 a.m. EST due to maintenance. 
'''

def splitTabs(value):
    re.purge()
    return re.split(r"\\t|\\r",value)

def scrapeQuickView(broth): ##TODO: clean variables, store in JSON file

    def checkListExists(value):
            if len(value) :
                return value[0].text_content()      #considered performing xpath here for 
            else:                                   #briefness, but will increase computation time
                return ""

    broth = lxml.html.fromstring(broth)
    
    websiteURL = checkListExists(broth.find_class("col-xs-12 col-sm-6 col-md-6 col-lg-9 breakword"))
    print(websiteURL)
   
    longDescription = checkListExists(broth.xpath("//p[@id='ongoingprograms']"))
    print(longDescription)

    


headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0",
            "referer": "https://apps.cra-arc.gc.ca/ebci/hacc/srch/pub/advncdSrch"}

URL = "https://apps.cra-arc.gc.ca/ebci/hacc/srch/pub/advncdSrch?"
zipPost = "https://apps.cra-arc.gc.ca/ebci/hacc/srch/pub/dwnldZp"
detailsURL = "https://apps.cra-arc.gc.ca/ebci/hacc/srch/pub/chrtydtls?selectedCharityBn="
quickViewURL = "https://apps.cra-arc.gc.ca/ebci/hacc/srch/pub/dsplyQckVw?selectedCharityBn="

req = requests.Session()
searchPage = req.get(URL).text

chowder = lxml.html.fromstring(searchPage)

token = chowder.xpath("//input[@name='token']")[0].value

file = req.post(zipPost, data={"struts.token.name":"token", "token":token, "q.srchNm":"",       #select only registered, charities
                                "q.bnRtNmbr":"", "q.bnAccntNmbr":"", "q.stts":"0007", 
                                "q.sttsEffctvDt":"", "q.snctnTypCd":"", "q.cty":"",  
                                "q.prvncSttCd":"", "q.pstlZpCd":"", "q.dsgntnTyp":"0001", "q.chrtyTyp":"", 
                                "q.chrtyCtgry":"", "p":"1"}).content

with open("./zip/4.zip", 'wb') as download:
    download.write(file)

with zipfile.ZipFile("./zip/4.zip") as zippedFile:
    fileName = zippedFile.namelist()[2]
    zippedFile.extract(fileName)

completeZipJSON =[]
quickViewList = []
p = open(fileName,"rb") 
for line in p.readlines():         ##TODO: USE requests-futures INSTEAD OF grequests
    
    splitLine = splitTabs(str(line))    

    charityLegalName = splitLine[1]
    addressLine1 = splitLine[7]
    city = splitLine[8]
    state = splitLine[9]
    country = splitLine[10]
    postcode = splitLine[11]
    buisnessRegNumber = str(line)[2:17]       #easier to pull straight from string rather than regex
    
    charityJSON = {
            "charityLegalName": charityLegalName,
            "buisnessRegNumber": buisnessRegNumber,
            "addressLine1": addressLine1, 
            "city": city,
            "state": state,
            "country": country,
            "postcode": postcode,
            # "imageURL": imageURL,                 //the rest to be scraped online
            # "charityWebsite": charityWebsite,
            # "smallDescription": shortDescription,
            # "longDescription": longDescription,
            # "telephone": str(telephone),
            # "fax": fax,
            # "charityNumber": charityNum,
            # "facebook": facebook,
            # "twitter": twitter
        }

    completeZipJSON.append(charityJSON)

    quickViewList.append(grequests.get(quickViewURL+buisnessRegNumber))
    # detailList.append(grequests.get(detailsURL+bnAccntNmbr))

with open("./json/1.json","w",encoding="utf8") as JSONfile:
    json.dump(completeZipJSON, JSONfile, ensure_ascii=False)

quickViewReq = grequests.imap(quickViewList)
#detailReq = grequests.imap(detailList)

for request in quickViewReq:
    scrapeQuickView(request.text)

##TODO: covert JSON files to dictionary and then merge
