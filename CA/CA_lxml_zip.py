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

def scrapeQuickView(broth): ##TODO: clean variables, store in JSON file

    def cleanWhiteSpaces(value):
        return re.sub("(Ongoing programs: )| (?!w*)|([\t\n\r\f\v])|(\s*$)","",value)

    def checkListExists(value):
            if len(value) :
                return value[0].text_content()      #considered performing xpath here for 
            else:                                   #briefness, but will increase computation time
                return ""

    broth = lxml.html.fromstring(broth)

    buisnessRegNumber = cleanWhiteSpaces(checkListExists(broth.find_class("col-xs-12 col-sm-6 col-md-6 col-lg-9"))) #luckily this is the first on the page
    print(buisnessRegNumber)

    websiteURL = cleanWhiteSpaces(checkListExists(broth.find_class("col-xs-12 col-sm-6 col-md-6 col-lg-9 breakword")))
    print(websiteURL)
   
    longDescription = cleanWhiteSpaces(checkListExists(broth.xpath("//p[@id='ongoingprograms']")))
    print(longDescription)

    for z in zipJSON:
        if z["buisnessRegNumber"] == buisnessRegNumber:
            z["websiteURL"] = websiteURL
            z["longDescription"] = longDescription

    # with open("./json/quick6.json","a",encoding="utf8") as JSONfile:
    #     json.dump(zipJSON, JSONfile, ensure_ascii=False)

headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0",
            "referer": "https://apps.cra-arc.gc.ca/ebci/hacc/srch/pub/advncdSrch"}

URL = "https://apps.cra-arc.gc.ca/ebci/hacc/srch/pub/advncdSrch?"

req = requests.Session()

searchPage = req.get(URL).text
chowder = lxml.html.fromstring(searchPage)
token = chowder.xpath("//input[@name='token']")[0].value

zipPost = "https://apps.cra-arc.gc.ca/ebci/hacc/srch/pub/dwnldZp"
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

detailsURL = "https://apps.cra-arc.gc.ca/ebci/hacc/srch/pub/chrtydtls?selectedCharityBn="
quickViewURL = "https://apps.cra-arc.gc.ca/ebci/hacc/srch/pub/dsplyQckVw?selectedCharityBn="

zipJSON =[]
quickViewList = []
p = open(fileName,"rb") 

for line in p.readlines():         ##TODO: USE requests-futures INSTEAD OF grequests

    splitLine = re.split(r"\\t|\\r",str(line))
    re.purge()

    charityLegalName = splitLine[1]
    addressLine1 = splitLine[7]
    city = splitLine[8]
    state = splitLine[9]
    country = splitLine[10]
    postcode = splitLine[11]
    buisnessRegNumber = str(line)[2:17]       #easier to pull straight from string rather than regex
    
    charityJSON = {                                 #TODO: clean double slashes, so can be encoded in utf8 properly
            "charityLegalName": charityLegalName,
            "buisnessRegNumber": buisnessRegNumber,
            "addressLine1": addressLine1, 
            "city": city,
            "state": state,
            "country": country,
            "postcode": postcode,
        }

    zipJSON.append(charityJSON)

    quickViewList.append(grequests.get(quickViewURL+buisnessRegNumber))
    # detailList.append(grequests.get(detailsURL+bnAccntNmbr))

zipJSON.pop(0)          #remove txt file header
quickViewList.pop(0) 

quickViewReq = grequests.imap(quickViewList, size=4)
#detailReq = grequests.imap(detailList)

quickViewJSON = []
for request in quickViewReq:
    scrapeQuickView(request.text)

with open("./json/conTest1.json","w",encoding="utf8") as JSONfile:
    json.dump(zipJSON, JSONfile, ensure_ascii=False)

