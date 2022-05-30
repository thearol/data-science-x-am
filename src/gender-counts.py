import sys, os
from pathlib import Path
import pandas as pd
import spacy
import argparse
nlp = spacy.load("en_core_web_sm")
nlp.disable_pipes('parser', 'ner')
nlp.add_pipe('sentencizer')
nlp.max_length = 1500000

def read_data(datapath, metadata):
    """
    Read the files whose titles are in the metadate.
    For each book make text chunks by paragraph. 
    returns: 
        list with books (chunked by paragraph)
        list with book id's 
    """
    id_list = []
    txts = []
    # load files 
    for filepath in Path(datapath).glob("*.txt"):
        if filepath.stem in list(metadata["id"]): # take only files that are in metadata csv
            id_list.append(str(filepath.stem)) # save text id
            with open(filepath, "r") as f:
                text = f.read()
                texts = text.split("\n\n") # split into chunks when new paragraph ("\n\n")
                stripped = [t.replace('\n', ' ') for t in texts] # replace \n with space
                txts.append(stripped) # save text chunks
    return txts, id_list

def process_paragraphs(text):
    """
    For each paragraph retrieve all pronouns.
    args:
        a list of text chunks (one book)
    returns:
        all pronouns from the book 
    """
    pronouns = []
    for doc in nlp.pipe(text):
        # retreive tokens where pos tag = pronoun (for one paragraph at a time)
        big_list = ([[token.lower_ for token in sent if token.pos_ == "PRON"] for sent in doc.sents])
        # flatten list of lists of pos tags
        pronouns.extend([item for sublist in big_list for item in sublist])  
    return pronouns

def process_books(all_books, book_ids, pronouns_M, pronouns_F):
    """
    args:
        list with chunked books
        book ids 
        list of male pronouns
        list of female pronouns  
    returns:
        df with total count of pronouns, male pronouns and female pronouns
    """
    female_mentions = []
    male_mentions = []
    total_pronouns = []
    for i in range(len(all_books)):
        print(i)
        pronouns = process_paragraphs(all_books[i])
        total_pronouns.append(len(pronouns))
        male_mentions.append(sum([pronouns.count(c) for c in pronouns_M]))
        female_mentions.append(sum([pronouns.count(j) for j in pronouns_F]))

    # calculate sum of mentions
    total_mentions = [(m + f) for (m,f) in zip(male_mentions, female_mentions)]

    # create df
    df = pd.DataFrame({'id':book_ids,
                    'total_pronouns': total_pronouns,
                    'female_mentions': female_mentions,
                    'male_mentions': male_mentions,
                    'total': total_mentions})    
    return df



def main():
    # initialise argumentparser
    ap = argparse.ArgumentParser()
    
    # define arguments
    ap.add_argument("-i", 
                    "--infile", 
                    required = False, 
                    type     = str, 
                    default  = "meta_data_published_after1799.csv", 
                    help="Input filename of metadata file")

    ap.add_argument("-o", 
                    "--outfile", 
                    required = False, 
                    type     = str, 
                    default  = "gender-counts_allbooks_after1799.csv", 
                    help="Output filename of df")

    # parse arguments to args
    args = vars(ap.parse_args())

    # read metadata
    metapath = os.path.join("..", "gutenberg-data", "metadata", args["infile"])
    meta_data = pd.read_csv(metapath)

    # path to txt files 
    all_data_path = os.path.join( "..", "gutenberg-data", "destination-folder-1799")

    # load texts and their id's
    texts, ids = read_data(all_data_path, meta_data)

    # define lists of pronouns
    male_pro = ['his', 'him', 'he', 'himself']
    female_pro = ['hers', 'her', 'she', 'herself']

    # process books
    df = process_books(texts, ids, male_pro, female_pro)

    # save df
    df.to_csv(os.path.join(os.getcwd(),"output", args["outfile"]), index=False)

if __name__=="__main__":
    main()
