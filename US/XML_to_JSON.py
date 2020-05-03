from lxml import etree
from io import StringIO, BytesIO
import os

concat = ""


for file in os.listdir("/home/luci/Documents/programming/recEV/webscraper/US/form990"):
    with open("/home/luci/Documents/programming/recEV/webscraper/US/form990/" + file, 'rb') as xml:
        content = xml.read()

    print(file, end="\n")
    root = BytesIO(content)
    
    for event, element in etree.iterparse(root):
        # print(element.tag)
        if element.tag == "{http://www.irs.gov/efile}BusinessNameLine1Txt":
            print(element.text)



    # charityJSON = {
    #             "charityLegalName": charityLegalName,
    #             "imageURL": imageURL,
    #             "charityWebsite": charityWebsite,
    #             "smallDescription": shortDescription,                       #from the  ##basically all the descriptions were long we can parse some
    #             "longDescription": longDescription ,      ##of them and include the first para in small and then the
    #             "addressLine1": addressLineOne,                                ##whole thing in long? Might be a bit janky
    #             "city": city,
    #             "state": state,
    #             "country": country,
    #             "postcode": postcode,
    #             "telephone": str(telephone),
    #             "fax": fax,
    #             "charityNumber": charityNum
    #     }

    # with open("concat2.xml", "a") as output:
    #     output.write(str(data))
    
    