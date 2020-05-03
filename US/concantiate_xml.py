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

    #returnData = root.getroot().xpath("//Return")

    #data = etree.tostring(root.getroot())
    
   # print(returnData)
    
    
    # with open("concat2.xml", "a") as output:
    #     output.write(str(data))
    
    