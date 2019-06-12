from flask import Flask, render_template, request

application = Flask(__name__)

# from scripts import helper
import requests


import json

import time
import os
import pickle


# def setup_app(application):
#    # All your initialization code
   
#    helper.setup()


# setup_app(application)



@application.route("/")
def hello():
    return "Hello World of search!"

@application.route('/search')
def search():
    # data_json=helper.search_for_word(word)
    # return "data_json"
    return render_template('index.html')


@application.route('/search_in_quran',methods=["POST"])
def search_in_quran():
    word=str(request.form['word_in_quran'])
    if not word.isalpha():
        return "Please enter alphabets"
    elif " " in word:
        return "Please enter single word"

    #this part to do the grunt work
    url_built="https://iqrah.herokuapp.com/search/"+str(word)
    print(url_built)
    result=requests.get(url_built).content
    result = json.loads(result)
    
            

    

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




    


if __name__ == "__main__":
    
    application.run(debug=True)
