from irsx.
import json



with open("index_2019.json","r") as infile:
    index_2019 = json.load(infile)["Filings2019"]
infile.close()
    
object_id_list = []
for item in index_2019:
    object_id_list.append(item["ObjectId"])