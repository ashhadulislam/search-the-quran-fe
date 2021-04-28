import nltk 
from nltk.corpus import wordnet 
import re
from operator import itemgetter
from fuzzywuzzy import fuzz 
from fuzzywuzzy import process 
import os
from nltk.corpus import words
import pickle



def sort_list_of_tuples(list_tuples):
    '''
    will have list of tuples like
    [
        (s1,v2,dist1),
        (s2,v2,dist2),
        .
        .
        .
        (s100,v100,dist100)
    
    ]
    Need to sort them by the last value of the tuple
    '''
    return sorted(list_tuples,key=itemgetter(2),reverse=True)
    



def get_synonyms(word):
    synonyms = [word.lower()] 
    antonyms = [] 

    for syn in wordnet.synsets(word): 
        for l in syn.lemmas(): 
            word=l.name()
            word=word.lower()
            if "_" not in word:
                synonyms.append(word)
            
    synonyms=list(set(synonyms))
    
    
    return synonyms




def search_word_in_quran_dict(book,language,translation,word,mapper_dict,reject_list,df):
    '''
    this function will return
    {
        word_syn1:[('s#,v#,comp1'),('s#,v#,comp2'),('s#,v#,comp3')],
        word_syn2:[('s#,v#,comp1'),('s#,v#,comp2'),('s#,v#,comp3')],
        word_syn2:[('s#,v#,comp1'),('s#,v#,comp2'),('s#,v#,comp3')], 
    
    }
    comp values are in sorted order for each list
    '''
    word_list=get_synonyms(word)
    print("Will look for the following words")
    print(word_list)
    new_dict={}
    for w in word_list:    
        print("Looking for ",w)
        if w not in reject_list and w not in mapper_dict.keys():
            # print("call get ayah")
            mapper_dict_pickle_location=os.path.join(os.getcwd(),"data",book,language,"pickles",translation+"_mapper_dict.pickle")
            reject_list_pickle_location=os.path.join(os.getcwd(),"data",book,language,"pickles",translation+"_reject_list.pickle")
            print(mapper_dict_pickle_location,reject_list_pickle_location)
            mapper_dict,reject_list=get_ayahs_from_quran(w, mapper_dict_pickle_location, reject_list_pickle_location,df)
            # print("updated the mapper_dict and reject list")
        if w in reject_list:
            # print("Word ",w," is absent from this rendition of Quran")
            # print("*********************")            
            continue

        #now find the sorted edit distance for each word and its corresponding tuple values 
        #in the dictinary
        # print("The tuples are ",mapper_dict[w])
        # sort these tuples
        search_result=[]
        for i in range(len(mapper_dict[w])):
            short_row=[]
            short_row.append(int(mapper_dict[w][i][0]))
            short_row.append(int(mapper_dict[w][i][1]))
            short_row.append(int(mapper_dict[w][i][1]))
            search_result.append(short_row)

        print("BEfore sorting",search_result)
        sorted_list_tuples = sorted(search_result, key = lambda x: (x[0], x[1]))
        print("After sorting",sorted_list_tuples)
        # sorted_list_tuples=mapper_dict[w]
        # print(sorted_list_tuples)
        new_dict[w]=[]
        # print(w," has the following ocurences in Quran")
        # print("*********************")
        
        cols=df.columns[:-1]
        # print("Identifier columns are ",cols)


        for tup in sorted_list_tuples:
            df_filter=df.copy(deep=True)            
            counter=0
            # print("tup is ",tup)
            for each_parameter in tup[:-1]:
                # print(cols[counter])
                # print(each_parameter)
                df_filter=df_filter[df_filter[cols[counter]] == str(each_parameter)]            
                counter+=1
            # print("df filtered is \n",df_filter)
            
            verse=str(df_filter.iloc[0][df_filter.columns[-1]])
            # print(verse)
            small_dict={}
            counter=0
            # print("Tuple is ",tup)
            for col in df.columns:
                small_dict[col]=tup[counter]
                counter+=1
            small_dict["Text"]=verse
            small_dict['Proximity']=tup[-1]
            new_dict[w].append(small_dict)


        # print("*********************")
            

    return new_dict
















def get_best_score(word,parag):
    similarity_score=0
    list_words=parag.split()
    for each_w in list_words:
        score=fuzz.ratio(word, each_w)
        if similarity_score<score:
            similarity_score=score
    
    return similarity_score


def get_ayahs_from_quran(the_word, mapper_dict_pickle_location, reject_dict_pickle_location,df):
    

    
    
    
    print("The word is ",the_word)
    synons=list(get_synonyms(the_word))
    print("It's synonyms are ",synons)

    if os.path.isfile(mapper_dict_pickle_location):
#         print("pickle exists, extracting dict")
        mapper_dict=open(mapper_dict_pickle_location,"rb")
        mapper_dict = pickle.load(mapper_dict)
#         print("Length of dict is ",len(mapper_dict))
    else:
#         print("pickle does not exist")
        mapper_dict={}
#         print("Created new dict")


    if os.path.isfile(reject_dict_pickle_location):
        reject_list=open(reject_dict_pickle_location,"rb")
        reject_list = pickle.load(reject_list)
    else:
#         print("pickle does not exist")
        reject_list=[]



    
    
    for word in synons:
        print("Searcing for {}".format(word))
        if word not in reject_list:
            if word not in mapper_dict:
                found=False
                for index,row in df.iterrows():
#                     print("Searcing for {} all over".format(word))
                    if word in row["Text"]:
                        found=True
                        if word not in mapper_dict:
                            mapper_dict[word]=[]
                        similarity_score=get_best_score(word,row["Text"])
                        mapper_dict[word].append((row["Surah"],row["Ayah"],similarity_score))
                if not found:
                    reject_list.append(word)
                    pickle_out = open(reject_dict_pickle_location,"wb")
                    pickle.dump(reject_list, pickle_out)
                    pickle_out.close()

                
                
    #now saving the dict as a pickle
#     print("New length is ",len(mapper_dict))
    pickle_out = open(mapper_dict_pickle_location,"wb")
    pickle.dump(mapper_dict, pickle_out)
    pickle_out.close()
    return mapper_dict,reject_list





