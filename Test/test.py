import spacy
from spacy.kb import KnowledgeBase
from spacy import displacy


nlp = spacy.load("it_core_news_lg")
vocab = nlp.vocab
kb = KnowledgeBase(vocab=vocab, entity_vector_length=64)


text = """"Fotocamera Mirrorless - Sensore MOS 24,3 Megapixel - Supporti compatibili: Memory Stick PRO Duo, Memory Stick PROHG Duo, Memory Stick XC-HG Duo, SD, SDHC, SDXC - Singolo Slot Supporti (SD o MS) - Display 3"" - Funzione filmati HD - WiFi - PictBridge - Connessione HDMI"""
doc = nlp(text)
total_entities = len(kb)
all_aliases = kb.get_alias_strings()
print(total_entities)

sentence_spans = list(doc.sents)
displacy.serve(sentence_spans, style="dep")
#http://localhost:5000/