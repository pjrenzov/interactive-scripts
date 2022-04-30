import json,os

path = "Metadata/"

def makeMetaData(name, discription, image,id, attributes = None):
    metadata = {"name":name, "description":discription,"image":image}
    if attributes != None:
        metadata["attributes"] = attributes
    s = len("0000000000000000000000000000000000000000000000000000000000000000")
    namestr = "0"*(s-len(id))+id
    
    with open(f"Metadata/{namestr}.json","w") as file:
        json.dump(metadata,file)

