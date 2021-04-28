import pandas as pd

from . import search_functions
import os
import pickle
import time

import json

import zipfile


def read_and_reformat(csv_path):
    df = pd.read_csv(csv_path,dtype=object)
    return df


def setup(book,language,translation):
    src_location=os.getcwd()
    data_location=os.path.join(src_location,"data",book,language)
    print("All my data ", data_location)
    
    
    file_name=language+"_"+translation+".csv"
    print("File name to get verses is ",file_name)

    
    df=read_and_reformat(data_location+"/"+file_name)
    print("dataframe read")
    print(df.head())

    pkl_location=os.path.join(data_location,"pickles")



    reject_list=translation+"_reject_list.pickle"
    print("reject list {}".format(reject_list))
    # reject_list=get_from_pickle(pkl_location+reject_list)

    
    mapping_dict=translation+"_mapper_dict.pickle"
    # mapping_dict=get_from_pickle(pkl_location+mapping_dict)
    print("mapping dict {}".format(mapping_dict))

    print("Setup done")
    return df,mapping_dict,reject_list,pkl_location

def get_from_pickle(pkl_location):
    if os.path.isfile(pkl_location):
        var=open(pkl_location,"rb")
        var = pickle.load(var)
        return var
    else:
        return pkl_location+" does not exist"


def get_result(book,language,translation,word,df,mapping_dict,reject_list,pkl_location):
    '''
    check if pkl file for the word exists
    and returns necessary data_dict.
    If pickle not there, do the search,
    create pickle and return the same

    '''
    pkl_file=os.path.join(pkl_location,translation,word)
    print("Pickle file for word is ",pkl_file)
    if os.path.isfile(pkl_file):
        print("Relax! Pickle exists")
        data_dict=pickle.load(open(pkl_file,"rb"))
        return data_dict

    #this part to do the grunt work
    
    mapping_dict_unpickled=get_from_pickle(os.path.join(pkl_location,mapping_dict))
    reject_list_unpickled=get_from_pickle(os.path.join(pkl_location,reject_list))    


    data_dict=search_functions.search_word_in_quran_dict(book,language,translation,word,mapping_dict_unpickled,reject_list_unpickled,df)
    print("Saving "+word+" In pickle "+pkl_file)
    pickle.dump(data_dict,open(pkl_file,"wb"))
    
    return data_dict





    


def search_for_word(book,language,translation,word):
    print("searching for {} in the book {}".format(word,book))
    print("language {} translation {}".format(language,translation))
    df,mapping_dict,reject_list,pkl_location=setup(book,language,translation)
    print("Returned ",df.shape,mapping_dict,reject_list,pkl_location)
    data_dict=get_result(book,language,translation,word,df,mapping_dict,reject_list,pkl_location)
    
    
    data_json = json.dumps(data_dict)
    return data_json
