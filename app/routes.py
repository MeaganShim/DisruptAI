from flask import render_template, request
import requests
# pprint is pretty print (formats the JSON)
from pprint import pprint
from IPython.display import HTML
import os
from flask import request
import json
import pdb

subscription_key = 'c1b32410a5504f6eab545bde66576089'
assert subscription_key
text_analytics_base_url = "https://australiaeast.api.cognitive.microsoft.com/text/analytics/v2.0/"
   
from app import app

@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def index():
    if request.method == "GET":
        return render_template('index.html')
    if request.method == "POST":
        text = request.json['data']
        # pdb.set_trace()
    text_analytics_base_url = "https://australiaeast.api.cognitive.microsoft.com/text/analytics/v2.1-preview/"

    api_url = text_analytics_base_url + "entities"
    print(api_url)

    ## INPUT REQUEST HERE 

    ## WE NEED TO POPULATE "TEXT" WITH THE INPUT FIELD 
    documents = {'documents' : [
        {'id': '1', 'text': text}
        ]}

    headers   = {"Ocp-Apim-Subscription-Key": subscription_key}
    response  = requests.post(api_url, headers=headers, json=documents)
    entities = response.json()
    pprint(entities)

    ## ANALYZE ENTITIES 

    name = ""
    money = ""
    date = ""
    for match in entities["documents"][0]["entities"]:
    #     print(match["name"])
    #     print(match["type"])
    #     print("")
        
        if(match["type"] == "Person"):
            name = match["name"]
            
        if(match["type"] == "Quantity"):
            money = match["name"]
            
        if(match["type"] == "DateTime"):
            date = match["name"]

    ## NLTK ANALYSIS 
    input_text = documents["documents"][0]["text"]
    # input_tokens = nltk.word_tokenize(input_text)
    input_tokens = input_text.split(" ")
        
    send_money = False
    auto_deposit = False
    cash_response = False
    urgent = False 
    for token in input_tokens:
        if (token == "send" or token == "etransfer" or token == "e-transfer" or token == "transfer"):
            send_money = True
        if (token == "transferring" or token == "sent"):
            auto_deposit = True
        if (token == "cash"):
            cash_response = True 
        if (token == "need"):
            urgent = True

    print("Name: " + name)
    print("Money: " + money)
    print("Date: " + date)
    print("SM: " + str(send_money))
    print("AD: " + str(auto_deposit))
    print("****")
    print()

    ## CREATE RESPONSE BASED ON VARIABLES: 
    response_text = ""
    if(send_money == True and name != "" and money != ""):
        response_text = "Send " + name + " " + money
        if(date):
            # date_tokens = nltk.word_tokenize(date)
            date_tokens = date.split(" ")
            for token in date_tokens:
                if token == "by":
                    response_text = response_text + date
                else:
                    response_text = response_text + " for " + date.capitalize()
                    
    elif(send_money == True and money != ""):
        response_text = "Transfer " + money + " through your banking app"

    elif(send_money == True):
        response_text = "Set up e-transfer to easily transfer funds"
        
    if(auto_deposit == True):
        response_text = "Set up auto-deposit with your account"
        
    if(cash_response == True):
        response_text = "Cash? Use e-transfers with your mobile banking app"

    print(documents["documents"][0]["text"])
    print(response_text)


    ## CREATING JSON TO SEND BACK TO FRONTEND 
    response = {
        "response": response_text
    }

    response = json.dumps(response)
    # pdb.set_trace()
    return response


@app.route('/page2')
def secondPage():
    return render_template('secondPage.html')

# @app.route('/text_analytics_lang')
# def text_analytics_lang():
#     documents = { 'documents': [
#         { 'id': '1', 'text': 'This is a document written in English.' },
#         { 'id': '2', 'text': 'Este es un document escrito en Español.' },
#         { 'id': '3', 'text': '这是一个用中文写的文件' }
#     ]}
    
#     response = query_azure_cognos("languages", documents)
#     return render_template('cognos.html', title='Home', response=response)

# @app.route('/text_analytics_sentiment')
# def text_analytics_sentiment():
#     documents = {'documents' : [
#         {'id': '1', 'language': 'en', 'text': 'I had a wonderful experience! The rooms were wonderful and the staff was helpful.'},
#         {'id': '2', 'language': 'en', 'text': 'I had a terrible time at the hotel. The staff was rude and the food was awful.'},  
#         {'id': '3', 'language': 'es', 'text': 'Los caminos que llevan hasta Monte Rainier son espectaculares y hermosos.'},  
#         {'id': '4', 'language': 'es', 'text': 'La carretera estaba atascada. Había mucho tráfico el día de ayer.'}
#     ]}
#     response = query_azure_cognos("sentiment", documents)
#     return render_template('cognos.html', title='Home', response=response)

# @app.route('/text_analytics_key_phrases')
# def text_analytics_key_phrases():
#     documents = {
#         'documents' : [
#             {'id': '1', 'language': 'en', 'text': 'I had a wonderful experience! The rooms were wonderful and the staff was helpful.'},
#             {'id': '2', 'language': 'en', 'text': 'I had a terrible time at the hotel. The staff was rude and the food was awful.'},  
#             {'id': '3', 'language': 'es', 'text': 'Los caminos que llevan hasta Monte Rainier son espectaculares y hermosos.'},  
#             {'id': '4', 'language': 'es', 'text': 'La carretera estaba atascada. Había mucho tráfico el día de ayer.'}
#         ]
#     }
#     response = query_azure_cognos("keyPhrases", documents)
#     return render_template('cognos.html', title='Home', response=response)

# @app.route('/text_analytics_text_entities')
# def text_analytics_text_entities():
#     documents = {
#         'documents' : [
#             {'id': '1', 'language': 'en', 'text': 'I had a wonderful experience! The rooms were wonderful and the staff was helpful.'},
#             {'id': '2', 'language': 'en', 'text': 'I had a terrible time at the hotel. The staff was rude and the food was awful.'},  
#             {'id': '3', 'language': 'es', 'text': 'Los caminos que llevan hasta Monte Rainier son espectaculares y hermosos.'},  
#             {'id': '4', 'language': 'es', 'text': 'La carretera estaba atascada. Había mucho tráfico el día de ayer.'}
#         ]
#     }
#     response = query_azure_cognos("entities", documents)
#     return render_template('cognos.html', title='Home', response=response)

# def query_azure_cognos(service, documents):
#     headers   = {"Ocp-Apim-Subscription-Key": subscription_key}
#     url = language_api_url = "{}{}".format(text_analytics_base_url, service)
#     response  = requests.post(url, headers=headers, json=documents)
#     return response.json()

