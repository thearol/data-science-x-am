#packages
import pandas as pd
import spacy
from pathlib import Path
import os
import json
from util_func import*

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("sentencizer")

metapath = "/Users/thearolskovsloth/gutenberg.nosync/metadata/meta_gender_en_12-05-202215:06:38.csv"
all_data_path = "/Users/thearolskovsloth/gutenberg.nosync/data/text/" 

def main():

    # read gender identification file
    with open("identify-gender.json","r") as fp:
        identifiable_gender = json.load(fp)

    with open("author-genders.json","r") as fp:
        author_genders = json.load(fp)

    # load dataframe containing bodyparts
    body = pd.read_csv("bodyparts.csv")
    bodywords = list(body["BodyPart"])

    # path to txt files
    all_data_path = os.path.join(os.getcwd(), "data")

    #read data
    texts, ids = read_data(all_data_path)

    #create empty dataframe to append to
    column_names = ["bodypart", "owner","owner_gender", "description", "ID", "author_gender"]
    main_df = pd.DataFrame(columns = column_names)

    for book, book_id in zip(texts,ids):
        for chunk in nlp.pipe(book):
            for sentences in chunk.sents:
                all_bodyparts = nouns_bodyparts(sentences, bodywords)
                for bodypart in all_bodyparts:
                    located_owner = detect_owner(sentences, bodypart)
                    description = descriptive_words(sentences, bodypart)
                    ID = book_id
                    
                    if located_owner in identifiable_gender:            
                        owner_gender = identifiable_gender[located_owner]
                        author_gender = author_genders[book_id]
                        main_df.loc[len(main_df.index)] = [bodypart, located_owner,owner_gender, description, ID, author_gender]

    main_df.to_csv("/Users/thearolskovsloth/Documents/MASTERS_I_COGSCI/second_sem/DataScience/datascience_exam/GenderedDescriptions/dataatlast.csv")


