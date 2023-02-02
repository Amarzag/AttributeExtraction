
'''scrive regole su mongo'''


import json
import pymongo

"""153,25,766,174-->Dispositivi elettronici > telefoni cellulari | 325-->Dispositivi elettronici    [113,202]"""

rules={}
Rule={
    "RAM/ROM": [
        { "ORTH": "RAM" },
        { "POS": "NUM" },
        { "ORTH": { "REGEX": "GB|gb|Gb|MB|Mb" } }
      ],
      "Pollici": [{ "ORTH": { "REGEX": "(D|d)isplay" } }, { "POS": "NUM" }],
      "Batteria": [{ "POS": "NUM" }, { "ORTH": "mAh" }],
      "Risoluzione": [
        { "POS": "NUM" },
        { "ORTH": { "REGEX": "x|X" } },
        { "POS": "NUM" },
        { "ORTH": { "REGEX": "(P|p)ixel" } }
      ]
}
exp_batteria = "((\\d*\\d)(mAh))|((\\d*\\d) (mAh))|(\\d*\\d(.|,)(\\d*\\d)(mAh))|(\\d*\\d(.|,)(\\d*\\d) (mAh))"    #xmAh
exp_Pollici= "((\\d*\\d'')|(\\d*\\d ''))|(\\d*\\d(.|,)((\\d*\\d'')|(\\d*\\d '')))"                            #x''
exp_Schermo="(\\d*\\d(.|,)\\d*\\d(MP| MP)|\\d*\\d(MP| MP))"                         #xMP 
exp_structuredData="[^;]*"                                                                #stringhe separate da;
exp_colori="( (R|r)osso| (R|r)ed | (V|v)erde| (G|g)reen| (A|a)rancione| (O|o)range| (B|b)lu | (B|b)lue | (G|g)iallo| (Y|y)ellow| (N|n)ero| (B|b)lack| (B|b)ianco| (W|w)hite| (G|g)rigio| (G|g)ray | (V|v)iola| (P|p)urple| (V|v)iolet| (O|o)ro | (G|g)old | (A|a)rgento| (S|s)ilver| (R|r)osa | (P|p)ink )"  #elenco di tutti i colori it e en??? introdurre un traduttore?(con spacy easy)
exp_RAM="(((\\d*\\d )|(\\d*\\d))(GB|gb|Gb|MB|Mb|gb|mb)( |,|\\n))"

''' "Regex": {
      "Fotocamera": "(\\d*\\d(.|,)\\d*\\d(MP| MP)|\\d*\\d(MP| MP))",
      "Capacit\u00e0": "((\\d*\\d)(mAh))|((\\d*\\d) (mAh))|(\\d*\\d(.|,)(\\d*\\d)(mAh))|(\\d*\\d(.|,)(\\d*\\d) (mAh))",
      "Pollici": "((\\d*\\d'')|(\\d*\\d ''))|(\\d*\\d(.|,)((\\d*\\d'')|(\\d*\\d '')))",
      "RAM/ROM": "(((\\d*\\d )|(\\d*\\d))(GB|gb|Gb|MB|Mb|gb|mb)( |,|\\n))"
    }'''

regex = {"Capacità": exp_batteria, "Pollici" : exp_Pollici, "Fotocamera"  : exp_Schermo, "RAM/ROM": exp_RAM, "colore": exp_colori}

#FORMATO ID: id_negozio+id_categoria
id:str="670"

rules.update({"identity":id,"regole":{"Rules":Rule,"Regex":regex}})
# Serializing json
json_object = json.dumps(rules)
 
# Writing to sample.json
#with open("SearchAttributi\\rules.json", "w") as outfile:
#    outfile.write(json_object)

config=json.load(open("SearchAttributi\\Config.json"))
mongoserver:str=config["mongoServer"]
myclient = pymongo.MongoClient(mongoserver)
mydb = myclient["buybuyfreeLocal"]
mycol = mydb["RulesAttribute"]
mydict = rules
x = mycol.insert_one(mydict)

