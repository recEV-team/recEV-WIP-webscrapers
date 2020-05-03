import requests
import json
from flask import jsonify, Flask
import re

from flask import Flask

URL = "https://data.gov.au/data/api/3/action/datastore_search?resource_id=eb1e6be4-5b13-4feb-b28e-388bf7c26f93&limit=5&fields=ABN,Charity_Legal_Name,Address_Line_1,Address_Line_2,Address_Line_3,State,Postcode,Town_City,Charity_Website"

data = requests.get(URL).json()

print(data)
records = data["result"]["records"]
# fields = result["fields"]

# records = fields["records"]

completeJSON = []

for record in records:
    

    charityJSON = {
            "charityLegalName": record["Charity_Legal_Name"],
            "imageURL": "",
            "charityWebsite": record["Charity_Website"],
            "smallDescription": "",
            "longDescription": "",
            "addressLine1": record["Address_Line_1"] + record["Address_Line_2"] + record["Address_Line_3"], 
            "state": record["State"],
            "country": "Australia",
            "postcode": record["Postcode"],
            "ABN": record["ABN"],
            "City": record["Town_City"],
            "telephone": "",
            "fax": "",
            "facebook": "",
            "twitter": ""
        }

    print("OK")

    completeJSON.append(charityJSON)


    ##TODO: append this to a json


with open ("./json/parse2.json", "w",encoding="utf8") as outfile:
    json.dump(completeJSON, outfile, ensure_ascii=False)

print(data)