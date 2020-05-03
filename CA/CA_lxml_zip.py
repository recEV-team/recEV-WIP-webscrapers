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

def scrape(value):


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

detailList = []
quickViewList = []
p = open(fileName,"rb") 
for lines in p.readlines():         ##TODO: USE requests-futures INSTEAD OF grequests
    bnAccntNmbr = str(lines)[2:17])
    detailList.append(grequests.get(detailsURL+bnAccntNmbr))
    quickViewList.append(grequests.get(quickViewURL+bnAccntNmbr))


r = grequests.imap(URLlist)

for request in r:
    scrape(request.text)

print(URLlist)