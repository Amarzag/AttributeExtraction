

from string import punctuation
import spacy
nlp = spacy.load("it_core_news_lg")

stop_words = nlp.Defaults.stop_words



def tokenize(sentence):
    toRet=[]
    sentence = nlp(sentence)
    # lemmatizing
    for token in sentence:
        if token.text not in stop_words and token.text not in punctuation:
            toRet.append(token.text)
    # removing stop words
    #sentence = [ word for word in sentence if word not in stop_words and word not in punctuations ]        
    #return sentence
    return toRet
  
def gen_List(lista:list,brand:str="brand"):
    toRet:list=[]
    length=lista.__len__()
    print(length)
    regula=length-1
    i = 0
    while i<regula:
        print(lista)        
        first=True
        for elem in lista:
            if first:
                tempstr=elem
            else:
                tempstr=tempstr+ " " + elem
            first=False
        peso=length-lista.__len__()+1    
        toRet.append(tempstr+" "+brand+"_"+peso.__str__())
        i=i+1
        lista.pop()        
    return toRet    

    

print(tokenize("la scarpa più bella arriva dal pianeta nettuno"))
tokenList=tokenize("la scarpa più bella arriva dal pianeta nettuno")
print(gen_List(tokenList))
