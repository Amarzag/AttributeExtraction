import spacy
nlp = spacy.load("it_core_news_lg")
text = "Samsung Galaxy S22 5G Display 6.1'' Dynamic AMOLED 2X, 4 fotocamere, RAM 8 GB, 256 GB, 3.700mAh, Phantom White, 15,5 cm (6.1''), 8 GB.."
doc = nlp(text)
tokens = {token.text:token for token in doc}

def is_attribute(token):
    # todo: use a classifier to determine whether the token is an attrubute
    return token.pos_=="ADJ"

def getchildren(attribute):
    for token in doc:
        if token.text.lower()==attribute.lower() : return list(token.children) 
    
def getfather(attribute):
    for token in doc:
        if token.text.lower()==attribute.lower() : return token.head

print(getchildren("Colore"))


