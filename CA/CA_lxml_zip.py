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
The search engine is unavailable between 02:00 a.m. and 06:00 a.m. EST due to maintenance. Please try again during operating hours.
'''

def returnBN(value):
    value = re.search("[0-9]*RR[0-9]*", str(value))
    re.purge()
    return value

def splitTabs(value):
    return re.split(r"\\t|\\r",value)

def scrapeDetail(value):


    print(value)

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

completeJSON =[]
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

'''
quickViewReq = grequests.imap(quickViewList)
#detailReq = grequests.imap(detailList)
'''

# for request in detailReq:
#     scrapeDetail(request.text)

# print(URLlist)
#BN/Registration Number	Charity Name	Charity Status	Effective Date of Status	Sanction	Designation Code	Category Code	Address	City	Province	Country	Postal Code	
#b"139764641RR0001\tLE COMIT\xc9 D'ACTION B\xc9N\xc9VOLE DE ST-CYPRIEN INC.\tRegistered\t1990-04-01\t\t0001\t0001\t112 RUE DE L'\xc9GLISE\tST-CYPRIEN\tQC\tCA\tG0L2P0\r\n
