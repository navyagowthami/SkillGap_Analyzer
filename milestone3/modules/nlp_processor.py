import spacy
import re

nlp = spacy.load("en_core_web_sm")

def preprocess(text):

    text=text.lower()

    text=re.sub(r'[^a-z\s]',' ',text)

    doc=nlp(text)

    tokens=[]

    for token in doc:

        if token.is_alpha and not token.is_stop:
            tokens.append(token.lemma_)

    return tokens