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

zipJSON = []
quickViewList = []
p = open("Charities_results_2020-05-06-10-41-43.txt","rb") 
for line in p.readlines():         ##TODO: USE requests-futures INSTEAD OF grequests
    
    splitLine = splitTabs(str(line))    

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

    zipJSON.append(charityJSON)
    quickViewList.append(grequests.get(quickViewURL+buisnessRegNumber))

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
            completeJSON.append(z)
            zipJSON.pop(zipJSON.index(z))


    #TODO: find cell in completeZipJSON and append these values

    # quickViewJSON.append(charityJSON)

    # with open("./json/conTest0.json","a",encoding="utf8") as JSONfile:
    #     json.dump(zipJSON, JSONfile, ensure_ascii=False)

zipJSON.pop(0)
quickViewList.pop(0) 

zipJSON.append(charityJSON)
quickViewReq = grequests.imap(quickViewList)

completeJSON = []
g = 0
for request in quickViewReq:
    if g == 4:
        break
    scrapeQuickView(request.text)
    g = g + 1


with open("./json/conTest4.json","a",encoding="utf8") as JSONfile:
        json.dump(completeJSON, JSONfile, ensure_ascii=False)
# print(URLlist)