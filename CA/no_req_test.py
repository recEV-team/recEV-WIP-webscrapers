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

def splitTabs(value):
    return re.split(r"\\t|\\r",value)

quickViewURL = "https://apps.cra-arc.gc.ca/ebci/hacc/srch/pub/dsplyQckVw?selectedCharityBn="

quickViewList = []
p = open("Charities_results_2020-05-03-09-59-44.txt","rb") 
for line in p.readlines():         ##TODO: USE requests-futures INSTEAD OF grequests
    
    bnAccntNmbr = str(line)[2:17]
    quickViewList.append(grequests.get(quickViewURL+bnAccntNmbr))

    # rea = splitTabs(str(line))
    # print(rea)
    
    # #detailList.append(grequests.get(detailsURL+bnAccntNmbr))
    # print(line)

def scrapeQuickView(broth):

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

quickViewReq = grequests.imap(quickViewList)

for request in quickViewReq:
    scrapeQuickView(request.text)

# print(URLlist)