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

quickViewList = []
p = open("Charities_results_2020-05-03-09-59-44.txt","rb") 
for line in p.readlines():         ##TODO: USE requests-futures INSTEAD OF grequests
    
    rea = splitTabs(str(line))

    print(rea)
    
    # bnAccntNmbr = str(line)[2:17]
    # #detailList.append(grequests.get(detailsURL+bnAccntNmbr))
    # quickViewList.append(grequests.get(quickViewURL+bnAccntNmbr))
    # print(line)

#b"139764641RR0001\tLE COMIT\xc9 D'ACTION B\xc9N\xc9VOLE DE ST-CYPRIEN INC.\tRegistered\t1990-04-01\t\t0001\t0001\t112 RUE DE L'\xc9GLISE\tST-CYPRIEN\tQC\tCA\tG0L2P0\r\n

#detailReq = grequests.imap(detailList)

quickViewReq = grequests.imap(quickViewList)


# for request in detailReq:
#     scrapeDetail(request.text)

# print(URLlist)