import spacy
from pathlib import Path

def read_data(datapath):
    """
    Read data, make chunks of 10 tweets. 
    """
    id_list = []
    txts = []
    # load files 
    for filepath in Path(datapath).glob("*.txt"):
        id_list.append(filepath.stem) # save text id
        with open(filepath, "r") as f:
            text = f.read()
            texts = text.split("\n\n") # split into chunks when new paragraph ("\n\n")
            stripped = [t.replace('\n', ' ') for t in texts] # replace \n with space
            txts.append(stripped)# save text chunks
    return txts, id_list

#define functions
def nouns_bodyparts(sent, bodywords):
    '''
    evaluates if a noun is a bodypart
    '''
    located_bodyparts = []
    for token in sent:
        if token.pos_ == "NOUN" and token.lemma_ in bodywords:
            located_bodyparts.append(token.text)
    return located_bodyparts

def detect_owner(sent, bodypart):
    '''
    locate the owner of the bodypart
    '''
    for token in sent:
        #print(token.pos_, token.dep_, token.text)
        if token.text == bodypart:
            children = list(token.children)
            for c in children:
                if c.pos_ == "PRON" and c.dep_ =="poss":
                    return c.text
                elif c.pos_ == "PROPN" and c.dep_ =="poss" or c.dep_ =="nsubj":
                    return c.text
                elif c.pos_ == "NOUN" and c.dep_ =="nsubj" or c.dep_ =="poss" :
                    return c.text

def descriptive_words(sent, bodypart):
    descr = []
    for token in sent:
        if token.text == bodypart:
            children = list(token.children)
            for c in children:
                if c.dep_ == "amod" or c.dep_== "acomp":
                    descr.append(c.text)
    return descr
