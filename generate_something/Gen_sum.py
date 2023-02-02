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
def run(text,brand):
    toret=tokenize(text)
    count=0
    string=""
    for elem in toret:
        count=count+1
        if(count==1):
            string=elem
        else:string=string+" "+elem          
        if(count==6):break

    return string+" "+brand
tempstr='camicia soft per tutte le stagioni maniche corte leggera forte e stringente bambini e adulti'    
print(run(tempstr,"brand"))