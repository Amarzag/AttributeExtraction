import os
import spacy
from spacy.matcher import Matcher
import re
import json
import pymongo
#from cronometer import ChronoMeter

from spacy.lang.char_classes import LIST_PUNCT
from urllib.parse import urlparse, parse_qs
#chrono = ChronoMeter()
#!/usr/bin/env python

'''inizializza lingua e percorso di configurazione'''

nlp = spacy.load("it_core_news_lg")
config=json.load(open("C:\\Users\\bacco\\Desktop\\spacy\\SearchAttributi\\Config.json"))
Rulepath:str=config["pathIntermedio"]+config["pathRulesFile"]
#path rules file
Path:str=Rulepath


'''funzioni utilities'''

#LowerCase su tutti i caretteri degli elementi in lista
def CaseInsensitive(List:list[str])->list[str]:
    toret=[]
    #print("list CaseInsensitive: "+List.__str__())
    for elem in List:
        toret.append(elem.lower())
    return toret    

#elimina tutti i caratteri " "
def elidiSpazio(List:list[str])->list[str]:
    toret=[]
    for elem in List:
        toret.append(elem.replace(" ",""))
    return toret

#elimina punteggiatura dalla lista
def elidiCaratterispeciali(List:list[str])->list[str]:
    toret=[]
    charIN=[]
    #print("lista caratteri speciali: "+LIST_PUNCT.__str__())
    for elem in List:
        for char in elem:
            if(char in LIST_PUNCT):
                charIN.append(char)
        tempvalue=elem
        #print("caratteri speciali trovati nella parola "+elem+": "+charIN.__str__())        
        for char in charIN:
            tempvalue=tempvalue.replace(char.__str__(),"")
        if(tempvalue==""):continue    
        toret.append(tempvalue)
        charIN=[]
        #print("parola senza careatteri speciali: "+tempvalue)
    #print("risultato elidi caratteri speciali: "+toret.__str__())
    return toret    

#ritorna la lista con solo gli elementi che contengo la substr "gb" 
def filtraperGB(List:list[str])->list[str]:
    toret=[]
    #print("list filtragb: "+List.__str__())
    for elem in List:
        if(elem.find("gb") != -1):
            toret.append(elem)
           # print("find gb: "+ elem)
    return toret

def filtraperTB(List:list[str])->list[str]:
    toret=[]
    for elem in List:
        if(elem.find("tb") != -1):
            toret.append(elem)
    print("lista tb filtrata: "+ toret.__str__())        
    return toret            

#estrai memoria di massa se presente parola chiave altrimenti se i valori sono >1 ritorna val Max
def ExtractMemArchiviazione(List:list[str])->list[str]:
    
    for elem in List:
        if(elem.find("rom") != -1 or elem.find("disk") != -1 or elem.find("interna") != -1):
            return [(re.search("(\d+)",elem).group(0))+" "+re.search("gb|tb",elem).group(0).upper()]
    if(List.__len__()<2):return []
    valuesGB:list[str]=[]
    valuesTB:list[str]=[]
    #temp:list[str]=CaseInsensitive(List)
    tempGB:list[str]=[]
    tempTB:list[str]=[]
    tempTB=filtraperTB(List)
    tempGB=filtraperGB(List)  
    for elem in tempGB:
        match=re.search("(\d+)",elem)
        if(match!=None):
            valuesGB.append((match.group(0)))
    for elem in tempTB:
        match=re.search("(\d+)",elem) 
        if(match!=None):
            valuesTB.append((match.group(0)))      
    #values=eliminicaduplicati(values)
    #print("extractMem size list: "+values.__len__().__str__())
    listintTB=[]
    print("list tb val: "+valuesTB.__str__())
    if (valuesTB.__len__() > 0):
        for elem in valuesTB:
            listintTB.append(int(elem))
        return [max(listintTB).__str__()+" TB"]    
    listInt=[]
    for elem in valuesGB:
        listInt.append(int(elem))
    if(listInt.__len__()< 2): return[]
    toret:int=max(listInt)
    return [toret.__str__()+" GB"]

#estrai ram se presente info "RAM", altrimenti ritorna il minimo se e solo se ci sono esattamente 2 valori, else []  
def ExtractRAM(List:list[str])->list[str]:
    temp:list[str]=[]   
    for elem in List:
        if(elem.find("ram") != -1 or elem.find("installata") != -1):
            return [(re.search("(\d+)",elem).group(0))+" "+re.search("(gb|mb)",elem).group(0).upper()]
    #temp=CaseInsensitive(List)
    temp=filtraperGB(List)
    #print("extractRAM size list: "+temp.__len__().__str__())
    if(temp.__len__()!=2):return []
    value:tuple(int,str)=(999999,"GB")
    for elem in temp:
        match1=re.search("(\d+)",elem)
        match2=re.search("(gb|mb)",elem)
        val=int(match1.group(0))
        unit=re.search("(gb|mb)",elem).group(0).upper()
        if(match1!=None and match2!=None):
            if((value[0]>val and (value[1]==unit)) or (unit=="GB" and value[1]=="MB")):
                value=(int(match1.group(0)),match2.group(0).upper())
    return [value[0].__str__()+" "+value[1]]

#funzione elimina sottostringhe e duplicato dalla lista valori 
def eliminicaduplicati(listIN)->list[str]:
    elem_to_remove=set()
    list=set()
    for elem in listIN:
        list.add(elem)
    #eliminare elementi che sono sottostringhe di altri elementi 
    for elem1 in list:
        for elem2 in list:
            if(elem1==elem2):continue               
            if(elem2.find(elem1) != -1):elem_to_remove.add(elem1)
            #if(elem2.__contains__(elem1)):elem_to_remove.add(elem1)      
    for elem in elem_to_remove:
        list.remove(elem)              
    tmplist=[]
    for elem in list:
        tmplist.append(elem)    
    return tmplist

#lettura file regole localmente
def letturaLocale(k1:str)->json:
    namefile:str=""
  
    #LEGGI FILE REGOLE 
    name= k1+".json"  
    for file in os.listdir(Path):
         
        if file==name:
            namefile=os.path.join(Path,file)
            #Userprint("FILE LETTO: ",file)
    if namefile=="":
        return "REGOLA NON TROVATA"
    return json.load(open(namefile))

#lettura file regole da mongo
def letturaMongo(k1:str)->json:
    mongoserver:str=config["mongoServer"]
    myclient = pymongo.MongoClient(mongoserver)
    mydb = myclient["buybuyfreeLocal"]
    mycol = mydb["RulesAttribute"]
    key:str=k1
    mydoc= mycol.find_one({"identity" : key},{"_id":0})
    return mydoc





'''--------------------------------------------FUNC APPLICAZIONE REGOLE---------------------------------------------------'''

def extractRules(match_rules,text):
    doc = nlp(text) 
    result:dict[str,set]={}  
    for rule_name, rule_tags in match_rules.items():       
        rule_matcher = Matcher(nlp.vocab)                    
        rule_matcher.add(rule_name, [rule_tags])        
        matches = rule_matcher(doc)                                      # Run matcher     
        for match_id, start, end in matches:                        
            attribute = doc[start:end]
            if result.get(rule_name) == None:
                attrset=set()
                attrset.add(attribute.text)               
                result.update({rule_name : attrset})
                
            else:
                setresult:set=result.get(rule_name)                           
                setresult.add(attribute.text)               
                result.update({rule_name : setresult})          
    return result
    
#estrai solo dati per structured data, perchè? il risultato della reg ex è una stringa da formattare accuratamente in questo caso
def structData(exp:str,text):                                            
    toret:set= {}     
    for match in re.finditer(exp,text):
        (start,end) = match.span()
        if(end-start>0):           
            attr=text[start:end].removeprefix(" ")                
            splitstr=attr.split(sep=":")              
            if(splitstr.__len__()>1):
                tempset:set=set()
                tempset.add(splitstr[1])               
                toret.update({splitstr[0]: tempset})              
    return toret

def extractRegex(regex,text,result):
    for regexp in regex:
        #caso speciale di un dato strutturato
        if regexp=="structured data:":
            structdict=structData(regex.get(regexp),text)
            for key in structdict.keys():
                result.update({key: structdict.get(key)})
        else:            
            matches = re.findall(regex.get(regexp), text)
            if matches.__len__()==0:continue
            #ci sono regex
            elementi:set=set()
            for elem in matches:
                #match è una tupla su multimatch, converto in set per eliminare duplicati
                if(isinstance(elem,tuple)):
                    for item in elem:
                        if(item==""):continue                       
                        elementi.add(item)
                else:elementi.add(elem)                        
            result.update({regexp : elementi})           
    return result        

'''----------------------------------------------------------------------------------------------------------'''

#funzione exec estrazione         
def run(text,k1):
    '''------------------------------------------------FUNZIONI LOCALI---------------------------------------'''
    #estrae da RAM_ROM: 
    #RAM: se compare per scritto (es: ram10gb), oppure se ci sono esattamente 2 valori espressi in gb prende il minore
    #memoria interna: se c'è più di 1 valore prende il maggiore
    #memoria: singolo valore trovato senza parole chiavi: non posso classificare la specializzazione
    def RAM_ROM(listValue:list[str])->dict[str,list[str]]:   
        Dict:dict[str,list[str]]=dict()
        #print("listavanilla: "+listValue.__str__())
        listValue=elidiCaratterispeciali(listValue)
        #print("lista elidicaratterispeciali: "+listValue.__str__())
        listValue=elidiSpazio(listValue)
        #print("lista elidispazio: "+listValue.__str__())
        listValue=CaseInsensitive(listValue)
        #print("list exec caseInsensitive: "+listValue.__str__())
        listValue=eliminicaduplicati(listValue)
        #print("list Elimina Duplicati: "+listValue.__str__())
        spazioArchiviazione:list[str]=ExtractMemArchiviazione(listValue)
        
        ram:list[str]=ExtractRAM(listValue)       
        
        if(ram.__len__()==0 and spazioArchiviazione.__len__()==0 and listValue.__len__()>0):
            Dict.update({"Memoria": listValue})
        if(ram.__len__()>0):Dict.update({"RAM" : ram})
        if(spazioArchiviazione.__len__()>0):Dict.update({"Memoria Interna" : spazioArchiviazione })
        return Dict
    #estarzione solo del case insensitive senza ripetizioni
    def Colore(listValue:list[str])->dict[str,list[str]]:
        toret=[]
        Dict:dict[str,list[str]]=dict()
        listValue=CaseInsensitive(listValue)
        #print("list value: "+listValue.__str__())
        for elem in listValue:
            if(elem.find("colore") !=-1):
                #print("elem: "+ elem)
                toret.append(elem.split(" ")[1])
            else:toret.append(elem)
        toret=elidiSpazio(toret)    
        toret=eliminicaduplicati(toret)    
        #print("value Colore list: "+toret.__str__())  
        Dict.update({"Colore" : toret}) 
        return Dict     
    #normalizza i valori ad uno stardad xx.yy'' | yy'' cifre decimali<4
    def Pollici(listValue:list[str])->dict[str,list[str]]:
        toret=[]
        Dict:dict[str,list[str]]=dict()
        for elem in listValue:
            #estrai valore numerici 
            flag=True
            match=re.search("(\d+\.\d+)|(\d+)",elem.replace(",","."))
            if(match!=None):
                tmpstr=match.group(0).__str__()
                if(tmpstr.find(".") != -1):
                    splitval=tmpstr.split(".")
                    for elem in splitval:
                        if(elem.__len__()>3):flag=False 
                elif tmpstr.__len__()>3: flag=False        
                if(flag):         
                    toret.append(tmpstr)     
            flag=True
                
        toret=eliminicaduplicati(toret)
        toret1=[]
        for elem in toret:
            elem=elem+"\'\'"
            toret1.append(elem)
        #print(toret1.__str__())    
        Dict.update({"Pollici" : toret1})
        return Dict
    #Elimina valori duplicati, cifre decimali<4 
    def Fotocamera(listValue:list[str])->dict[str,list[str]]:
        #print("list value fotocamera:" + listValue.__str__())
        toret=[]
        Dict:dict[str,list[str]]=dict()
        listValue=eliminicaduplicati(listValue)
        flag=True
        for elem in listValue:
            match=re.search("(\d+\.\d+)|(\d+)",elem.replace(",","."))
            if(match!=None):
                tmpstr=match.group(0).__str__()
                if(tmpstr.find(".") != -1):
                    splitval=tmpstr.split(".")
                    for elem in splitval:
                        if(elem.__len__()>3):flag=False 
                elif tmpstr.__len__()>3: flag=False        
                if(flag):         
                    toret.append(tmpstr)     
            flag=True        
        toret1=[]
        for elem in toret:
            toret1.append(elem + " MP")
        #print(toret.__str__())   
        Dict.update({"Fotocamera" : toret1})
        return Dict
    #formattazione + elimina duplicati 
    def Risoluzione(listValue:list[str])->dict[str,list[str]]:
        toret=[]
        Dict:dict[str,list[str]]=dict()
        listValue=elidiSpazio(listValue)
        for elem in listValue:
            match=re.search(".*(P|p)ixel",elem)
            if(match!=None):
                toret.append(match.group(0).replace("p","P"))
        toret=eliminicaduplicati(toret)
        Dict.update({"Risoluzione" : toret})       
        return Dict 
    #post formattazioni costum per chiave
    def switch(lang,List)->dict[str,list[str]]:
        #print("switch key-list: "+lang+"-"+List.__str__())
        Dict:dict[str,list[str]]=dict()
        if lang=="RAM/ROM":
            return RAM_ROM(List)
        elif lang=="Colore":
            return Colore(List)
        elif lang=="Pollici":
            return Pollici(List)
        elif lang=="Fotocamera":
            return Fotocamera(List)  
        elif lang=="Risoluzione":
            return Risoluzione(List)         
        else:
            Dict.update({lang : eliminicaduplicati(List)})  
            return Dict    
                
    #print("running")

    '''--------------------------------------------------LETTURA & APPLICAZIONE REGOLE-------------------------------------'''
    
    tempdict:json=letturaLocale(k1)
    tempgeneric:json=letturaLocale("generic")
    #print("regole :",tempdict)
    #print("-------------------------print regola---------------------------------------")
    #print(tempdict)
    tempRegole:dict=tempdict.get("regole")
    tempRegoleGeneric:dict=tempgeneric.get("regole")
    tempRule:dict=tempRegole.get("Rules")
    tempRegex:dict=tempRegole.get("Regex")
    tempRule.update(tempRegoleGeneric.get("Rules"))
    tempRegex.update(tempRegoleGeneric.get("Regex"))

    #print("-------------------------print singoli dict---------------------------------------")
    #print("REGOLE: ",tempRule)
    #print("REGEX: ",tempRegex)
    resRules:dict[str:str]={}
    resRegex:dict[str:str]={}
    #estrazione valori
    if tempRule!=None and tempRule.__len__() != 0 :
        resa=extractRules(tempRule,text)
        if(resa!=None):
            for key in resa:
                concatstr=""
                for elem in resa.get(key):
                    if(concatstr==""):
                        concatstr=elem.__str__()
                        resRules.update({key: concatstr})
                    else:
                        concatstr=concatstr+", "+elem.__str__()   
                    
                        resRules.update({key: concatstr})
        
    if tempRegex!=None and tempRegex.__len__() != 0 :
        resb=extractRegex(tempRegex,text+",",{})
        
        if(resb!=None):
            for key in resb:
                concatstr=""
                for elem in resb.get(key):
                    if(concatstr==""):
                        concatstr=elem.__str__()
                        resRegex.update({key: concatstr})
                    else:    
                        concatstr=concatstr+", "+elem.__str__()
                        resRegex.update({key: concatstr})

    
    '''------------------------------------------FORMATTAZIONE VALORI-----------------------------------'''                    
    ToRet:dict[str:list[str]]={}
    setOfKey:set[str]=set()
    for key in resRules:
        setOfKey.add(key)
    for key in resRegex:
        setOfKey.add(key)    
    for key in setOfKey:
        if(resRegex.get(key)!=None and resRules.get(key)!=None):
            ValueRules:str=resRules.get(key)
            
            ValueRegex:str=resRegex.get(key)
            
            listValue:list=ValueRegex.split(", ")      
            for elem in ValueRules.split(", "):       
                listValue.append(elem)
            tmp=switch(key,listValue)
            #print("res switch: "+tmp.__str__())
            if(tmp!=None):ToRet.update(tmp)   
            
            
        else:
            if(resRegex.get(key)!=None):
                string_value:str = resRegex.get(key)
                listValue=string_value.split(", ")
                tmp=switch(key,listValue)
                if(tmp!=None):ToRet.update(tmp)               
            else:
                string_value:str = resRules.get(key)
                listValue=string_value.split(", ")
                tmp=switch(key,listValue)
                if(tmp!=None):ToRet.update(tmp)  


    # STAMPA RISULTATI, JSON 
    jsonResult=json.dumps(ToRet)
    print(jsonResult)
    return jsonResult

#funzione test helloword
def hello():
    print('Caiooooo')
    #with open("C:\\Users\\bacco\\Desktop\\spacy\\SearchAttributi\\appunti.json", "w") as outfile:
        #outfile.write(json.dumps("lanciato"))
#funzione test (run by cmd)
def start(text,k1,k2):
    tempt=text
    tempk1=k1
    tempk2=k2
    tempInput=""
    run(tempt,tempk1,tempk2)
    flag=True
    while flag:
        tempInput=input()
        if(tempInput == "stop"):break
        tempArray=[]
        tempArray=tempInput.split("**")
        tempt=tempArray[0]
        tempk1=tempArray[1]
        tempk2=tempArray[2]
        run(tempt,tempk1,tempk2)


#chrono.start_chrono()
#run(text,k1,k2)
#chrono.stop_chrono()
#chrono.print_time()   
#run(text,k1,k2)
#if __name__ == "__main__":
#   import sys
    #run(k1,k2,text)
    #hello()
    #run(str(sys.argv[1]),str(sys.argv[2]),str(sys.argv[3]))


#server locale
from http.server import BaseHTTPRequestHandler, HTTPServer
    # Creiamo la classe che riceverà e risponderà alla richieste HTTP
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    # Implementiamo il metodo che risponde alle richieste GET
    
    def do_GET(self):
        parse_result = urlparse(self.path)
        dict_result=parse_qs(parse_result.query)
        print(dict_result)
    
        k1:str=dict_result.get("FileRulesName").pop()
        
        try:
            text:str=dict_result.get("text").pop()
        except:
            print("Text==null")
            return     
      
        toret=run(text,k1)
        # Specifichiamo il codice di risposta
        self.send_response(200)
         # Specifichiamo uno o più header
        self.send_header('Content-type','text/html')
        self.end_headers()
        # Specifichiamo il messaggio che costituirà il corpo della risposta
        message = toret
        self.wfile.write(bytes(message, "utf8"))
        return
#start server    
def exe():
    print('Avvio del server...')
    # Specifichiamo le impostazioni del server
    # Scegliamo la porta 8081 (per la porta 80 sono necessari i permessi di root)
    server_address = ('127.0.0.1', 8081)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('Server in esecuzione...')
    httpd.serve_forever()
exe()