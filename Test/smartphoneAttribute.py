
""" 

-idea generale: individuare categoria da arricchire e scrivere accurate regole per estrarre attributi già noti, più è omogeneo e circoscritto
                il dominio delle descrizioni e più accurato sarà il risultato atteso e semplice per la scrittura delle regole. come? selezionare
                accuratamente negozi e individuare pattern per dati già semi strutturati delle descrizioni: è possibile automatizzare questo processo? 
                bella domanda, per il momento a mano e testa, se funziona con i dati selzionati a mano ci si può pensare***

                1-differenziare a blocchi di negozi & categoria (estratti dal csv)
                2-lanciare n processi(sequenzialmente) per ogni blocco trovato
                3-per ognuno progettare regole ad-hoc per la sua estrazione di attributi
                4-scrematura sui dati estratti, eventuali constraint per ogni attributo(tipo lavoro già fatto da Luca con regExp sui dati strutturati
                quali traduzioni linguistiche ecc..), (idea secondaria introdurre traduttore automatico di spacy ed effrontare ipotetici vincoli prima di generare il 
                csv di output)
                5-arricchire CSV e restituirlo al chiamante del processo
    
    input: 
            -regole di match sequenza token e/o regExp su intera frase di descrizione
            -csv 

    elaborazione:
            -leggere csv
            -formattazione delle stringhe da dare in pasto alle regole
            -metadata di stringhe etichettate per regole di match, stringhe basate su risultati mirati di regEX su intera descrizione 
            -formattazione attributi e selezione di quest'ultimi (definire bene la logica)
            -sovrascrittura csv 
   
    output: 
            -csv arricchito 

che cosa comporta questa soluzione: individuazione dei negozi,categoria sul quale è possibile effettuare un estrazione di attributi dalle descrizione + scrittura ad-hoc
                                    per ogni (negozio,categoria) individuti.

***
IDEA off-topic GOAL: alleggerire il lavoro ricerca dei candidati alla scrittura di nuove regole.
                rating sulla similarità delle descrizioni di ogni negozio per loro categoria associata---> stiamo individuando per ogni negozio e per ogni sua categoria
                associata il grado di similarità strutturale delle descrizioni, creiamo questo data set di training e di test e diamo in pasto ad un algo ml, l'intenzione è
                quello di creare un sisteme che dato in pasto qualsiasi csv ci comunica il livello di similarità delle desc per tupla (negozio,categoria) conetenuti in esso:
                F:(negozio,categoria)-->rating.
                Dove il rating è alto tenere tupla (negozio,categoria) come candidato alla scrittura di nuove regole per l'estrazione di attributi dedicato ad esso. 
               
***                
------------------------------------ASTRAZIONE AD ALTO LIVELLO--------------------------------------------------------

1-tooladimin: seleziona la attivazione/generazione attributi, seleziona attributi da cercare + opzionale negozio/categoria(consigliato)

2-chiamata la funzione lato backend c#: chiama la funzione python con input passati precedentemente + path del csv da aprire(dove risiedono i csv?)

3-la funzione python sovrascrive il csv con i nuovi attributi ove compaiono, verificare che gli attributi non siano già presenti 

4-al prossimo update dei prodotti aggiornati 
            
"""


import spacy
from spacy.matcher import Matcher
import re
from translate import Translator
import numpy
import json

class Regex:
    def __init__(self,nome,expression):
        self.nome=nome
        self.expression=expression
class Array_attributi:
    def __init__(self,rules_result:list,regEX_result:list):
        self.rules_result=rules_result
        self.regEX_result=regEX_result
translator = Translator(from_lang='it', to_lang='en')





#--------------------------------------------CSV reader-----------------------------------------------------------------------------------------------------------------------

"""obbiettivo: leggere il file csv in imput e scremare per negozio & categoria dato in input"""
import csv



"""153,25,766,174-->Dispositivi elettronici > telefoni cellulari | 325-->Dispositivi elettronici"""

categoria="[113,202]".__str__()
negozio="153".__str__()
flag=False
#la funzione restituisce la lista delle descrizioni date come filter in input (categoria,negozio,csv)--->list descrizioni
def filter_csv(categoria:str,negozio:str,path:str):
    with open(path, newline="", encoding="utf-8") as filecsv:
     lettore = csv.reader(filecsv,delimiter=";")
     index:int=0
     indexCategoryDesc:int=0
     indexDescription:int=0
     indexEshopId:int=0
     for elem in next(lettore):
        #print(elem)
        if elem=="CategoryId":
            indexCategoryDesc=index
            #print("indexCategoryDesc:",indexCategoryDesc)
        if elem=="Description":
            indexDescription=index 
            #print("indexDescriptionID:",indexDescription)  
        if elem=="EshopId":
            indexEshopId=index
            #print("indexEshopID:",indexEshopId)

        index=index+1    

     dati=[]
     index=0
     for linea in lettore: 
        

        try:
            #mi porto dietro solo le descrizioni che rispettano i parametri da input
            if ((linea[indexCategoryDesc]==categoria or categoria=="") and ((linea[indexEshopId]==negozio) or negozio==0)):    
               
                dati=dati.__add__([linea[indexDescription]])
            index=index+1
        except IndexError:          
            print("campo non esiste per la linea num: ",index)
     return dati  

#TEST stampa risultati 
import os
s = '\\'
descriptions=[]
for elem in os.listdir("NegoziAman"):
    path="NegoziAman"+s+elem
    descriptions=descriptions+filter_csv(categoria,negozio,path)
    print(filter_csv(categoria,negozio,path))





#regole POS-Tag DEP-tag e regEX(sui sigoli token e non su intera frase) per telefonia mobile
"""le rules sono espressioni di match sulla sequenza di token, ogni blocco {} rappresenta un token, il contenuto le regole di match.
   le regole di match possono essere di tipo  POS-tag DEP-tag regEx e altri ancora, guarda doc https://spacy.io/api/matcher"""
rules = {
    "RAM/ROM": [
        {
            "ORTH": "RAM",
            
        },
        {
            "POS": "NUM"
        },
        {
            "ORTH":
                {
                    
                    "REGEX":"GB|gb",
                      
                },
                "OP": "?"
        }
    ],
    "colore":[
        {
            "ORTH":
            {
                "REGEX":"((C|c)olore)"
            }
        },
        {
            "POS":"ADJ"
        }
    ],
    "Risoluzione":[
        
        {
            "POS":"NUM"
        },
        {
            "ORTH":
            {
                "REGEX":"x|X"
            }
        },
        {
            "POS":"NUM"
        },
        {
            "ORTH":
            {
                "REGEX":"(P|p)ixel"
            }
        } 
 
    ]
}
#regular expression
regex = "(\w*)(:)\s(\w*)"                                                                 #x:y
exp_batteria = "((\d*\d)(mAh))|((\d*\d) (mAh))|(\d*\d(.|,)(\d*\d)(mAh))|(\d*\d(.|,)(\d*\d) (mAh))"    #xmAh
exp_Pollici= "((\d*\d'')|(\d*\d ''))|(\d*\d(.|,)((\d*\d'')|(\d*\d '')))"                             #x''
exp_Schermo="(\d*\d(.|,)\d*\d(MP| MP)|\d*\d(MP| MP))"                         #xMP 
exp_structuredData="[^;]*"                                                                #stringhe separate da;
exp_colori="(R,r)osso |(V,v)erde |(A,a)rancione |(B,b)lu |(G,g)iallo |(N,n)ero |(B,b)ianco"                                           #elenco di tutti i colori it e en??? introdurre un traduttore?(con spacy easy)
exp_RAM="(\d*\d (?i)(GB))|(\d*\d(?i)(gb))"
exp_array=[Regex("struct data", exp_structuredData)]

#-------------------------------------------------------------------------------------------------------------------

nlp = spacy.load("it_core_news_lg")


    
def extract(text):
    doc = nlp(text) 
    result = {}
    for rule_name, rule_tags in rules.items(): 
        rule_matcher = Matcher(nlp.vocab)                    
        rule_matcher.add(rule_name, [rule_tags])        
        matches = rule_matcher(doc)                                      # Run matcher     
        for match_id, start, end in matches:                        # For each attribute detected, save it in a list
            attribute = doc[start:end]
            result.__setitem__(rule_name , attribute.text)
    return result 
    


def regularexpression(text="",regex=numpy.array([],dtype=Regex)):
    #doc = nlp(text)                                            # Convert string to spacy 'doc' type
    toret={}
    for regexp in regex:
        matches = re.findall(regexp.expression, text)
        if matches.__len__()==0:continue
        elementi:set=set()
        for elem in matches:
            if(isinstance(elem,tuple)):
                for item in elem:
                    if(item==""):continue
                    elementi.add(item)
            else:elementi.add(elem)

        elem_to_remove=set()

        for elem1 in elementi:
            

            for elem2 in elementi:
                if(elem1==elem2):continue               
                if(elem1 in elem2):elem_to_remove.add(elem1)

        for elem in elem_to_remove:
            elementi.remove(elem)        
        if(elementi.__len__()==0):continue    
        toret.update({regexp.nome : elementi.__str__()})
        
            #(start,end) = match.span()
            #if(end-start>0):
                #print("(",start,",",end,")")
             #   attr=text[start:end].removeprefix(" ")                
              #  splitstr=attr.split(sep=":")              
               # if(splitstr.__len__()>1):
                #    toret.__setitem__(splitstr[0],splitstr[1])
                #print(attr)

    return toret          
        #span = doc.char_span(start, end)
        #print(match)
        
        #if span is not None:                                  #This is a Span object or None if match doesn't map to valid token sequence
            #print("Found match regexp:",span.text, "(",start,",",end,")")
    #print(doc.char_span(0,10))        
    
            

exampletext="""HSistema operativo: Android 7; Dual sim: No; Fotocamera: 12 MP; Memoria interna: 64 GB; Display: 5,87 ''; Rete: 4G; RAM: 4 GB; N core processore: Octa-core; Colore: Nero; Modello: KEYone; Serie: n.d.;"""

#regularexpression(exampletext,regex)
#regularexpression("batteria:",exampletext,exp_batteria)
#regularexpression("display:",exampletext,exp_Pollici)
#regularexpression("fotocamera:",exampletext,exp_Schermo)
#regularexpression("split \';\':",exampletext,exp_structuredData)
#regularexpression(exampletext,exp_array)
#print('\r\n',"FOUND MATCH RULES:",'\r\n',extract(exampletext))
countRegex=0
countRule=0
if flag==False:
    
    for dati in descriptions:
        alist=regularexpression(dati,exp_array)   
        jsonRegEX=json.dumps(alist)
        if(jsonRegEX=="{}"):continue
        print(alist)
        countRegex=countRegex+1
        #print("attributi regEX: ",jsonRegEX)
    counter:str=countRegex.__str__()   
    



if flag==True:
    for dato in descriptions:
        alist=extract(dato)
        jsonRules=json.dumps(alist)
        if(jsonRules=="{}"):continue
        print(alist)
        countRule=countRule+1
    counter:str=countRule.__str__() 
   
print("numero prodotti totale visionati : "+descriptions.__len__().__str__()+" | numero prodotti generati: "+counter)



#TODO: json format
#alist=regularexpression(exampletext,[Regex("stuctured data",exp_structuredData)])
#blist=extract(exampletext)
#jsonRegEX=json.dumps(alist)
#jsonRules=json.dumps(blist)
#print("attributi regEX: ",jsonRegEX)
#print("attributi match rules: ", jsonRules)


#print(type(json.dumps(regularexpression(exampletext,[Regex("stuctured data",exp_structuredData)]))))
#obj=Array_attributi(extract(exampletext),regularexpression(exampletext,[Regex("stuctured data",exp_structuredData)]))
#print(json.dumps(obj))
#print(json.dump(regularexpression(exampletext,[Regex("stuctured data",exp_structuredData)])))
