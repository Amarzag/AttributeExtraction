'''sincronizza le regole salvate su mongo con i file json in locale'''


import json
import pymongo
import os


config=json.load(open("SearchAttributi\\Config.json"))
Rulepath:str=config["pathRulesFile"]
mongoserver:str=config["mongoServer"]
myclient = pymongo.MongoClient(mongoserver)
mydb = myclient["buybuyfreeLocal"]
mycol = mydb["RulesAttribute"]

listDoc:list=[]
# function to add to JSON
def write_json(new_data, filename):
    with open(filename,'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data 
        file_data["RulesAttribute"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)



def delete_all_elem(path):
    for file in os.listdir(path):
        namefile=os.path.join(path,file)
        os.remove(namefile)

      


save_path=config["pathIntermedio"]+Rulepath
delete_all_elem(save_path)  
mydoc= mycol.find()
for x in mydoc:
    print(x)
    print("-----------------------")
    tmpdict:dict=x
    tmpdict.pop("_id")
    name_of_file:str=tmpdict.get("identity")
    completeName = os.path.join(save_path, name_of_file+".json") 
    json_object=json.dumps(tmpdict)   
    #file = open(completeName,"w")
    #file.write(tmpdict,indent=3) 
    #file.close()
    with open(completeName, "w") as outfile:
        outfile.write(json_object)
    #write_json(json_object,Rulepath)
   
      