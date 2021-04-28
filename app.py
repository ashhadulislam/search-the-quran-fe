from flask import Flask, render_template, request
app = Flask(__name__)

# from scripts import helper
import requests


import json

import time
import os
import pickle

from scripts import helper

@app.route("/")
def hello():
    return "Hello World of search!"

@app.route('/search')
def search():
    # data_json=helper.search_for_word(word)
    # return "data_json"
    return render_template('index.html')


@app.route('/search_in_quran',methods=["POST"])
def search_in_quran():
    word=str(request.form['word_in_quran'])
    language,translation=str(request.form['translations']).split("_")
    print("Lang",language,"transl",translation)
    if not word.isalpha():
        return "Please enter alphabets"
    elif " " in word:
        return "Please enter single word"

    #this part to do the grunt work locally    
    result=search_word("quran",language,translation,word)
    result = json.loads(result)
    print("Result obtained ")
    print(result.keys())
    



    #this part to do the grunt work different server
    # url_built="https://iqrah.herokuapp.com/search/quran/yuali/"+str(word)
    # print(url_built)
    # result=requests.get(url_built).content
    # result = json.loads(result)

    
            

    

    # result=str(result)
    # result = result.replace("'", "\"")
    # result = result.replace('"', '\"')
    # result=    ast.literal_eval(result)
    '''
    for key, value in result.items():
        
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        print(key)
        for verse_details in value:
            print(verse_details["Surah"])
            print("**************************************************")
            print(verse_details["Ayah"])
            print("**************************************************")
            print(verse_details["Text"])
        
    '''
    
    # return str(result)
    
    return render_template('index.html',result = result)



@app.route('/search/<book>/<language>/<translation>/<word>')
def search_word(book,language,translation,word):
    data_json=helper.search_for_word(book,language,translation,word)
    return data_json

    


if __name__ == "__main__":
    
    app.run(debug=True)
