import requests
import re
import json
import lxml

req = requests.Session()

irs_form_2019 = req.get('https://s3.amazonaws.com/irs-form-990/index_2019.json').json()

with open("index_2019.json","w",encoding="utf8") as outfile:
    json.dump(irs_form_2019, outfile, ensure_ascii=False, indent=2)

# load from file when testing



# xml_test = req.get("https://s3.amazonaws.com/irs-form-990/201931019349301083_public.xml").text

# with open("form990_sample2.xml", "w", encoding="utf8") as outfile:
#     outfile.write(xml_test)


'''
JSON:
"charityNumber": EIN,
"charityLegalName": OrganizationName
ObjectID shall be taken, this can be concat'ed with url to get xml file


XPaths for xml:

"charityWebsite": charityWebsite,
"smallDescription": shortDescription,
"longDescription": longDescription,
"addressLine1": addressLine1, 
"state": state,
"country": "UK",
"postcode": postcode,
"telephone": str(telephone),


contains 640411847

and 640427465
'''