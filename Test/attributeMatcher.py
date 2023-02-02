import spacy
from spacy.matcher import Matcher
import re
rules = {
    "sostantivo and compound": [
        {
            "DEP": "compound",
            "OP": "?"
        },
        {
            "POS": "NOUN"
        }
    ],
      "sostantivo and adjective": [
        {
            "POS": "NOUN",
        },
        {
            "POS": "ADJ",
        }
    ],

    
}

regex = "(\w*)(:)\s(\w*)"


nlp = spacy.load("it_core_news_lg")
rule_matcher = Matcher(nlp.vocab)
for rule_name, rule_tags in rules.items(): # register rules in matcher
	rule_matcher.add(rule_name, [rule_tags])
    
def extract(text):
    doc = nlp(text)  # Convert string to spacy 'doc' type
    matches = rule_matcher(doc)  # Run matcher

    result = []
    for match_id, start, end in matches:  # For each attribute detected, save it in a list
        attribute = doc[start:end]
        result.append(attribute.text)

    return result
def regularexpression(text,regex):
    doc = nlp(text)  # Convert string to spacy 'doc' type
    for match in re.finditer(regex,text):
        start, end = match.span()
        span = doc.char_span(start, end)
    # This is a Span object or None if match doesn't map to valid token sequence
        if span is not None:
            print("Found match regexp:", span.text)

exampletext="""Orologio solo tempo donna Philip Watch della collezione Caribe Cassa in acciaio da 39x31mm e spessore da 9,15 mm Cinturino in acciaio di colore silver e oro rosa Quadrante argentato con cristalli e datario Movimento al quarzo Resistenza all'acqua 10 atm"""


regularexpression(exampletext,regex)
    
print("found match rules:")
print(extract(exampletext))