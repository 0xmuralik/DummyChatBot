import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer= LancasterStemmer()

import numpy
import tensorflow
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense
import random
import json
import pickle

with open("intents.json") as file:
    data = json.load(file)

with open("data.pickle", "rb") as f:
    words, labels = pickle.load(f)

model=keras.models.load_model("Initial_model")
#model.summary()

def bag_of_words(s,words):
    bag =[0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words if word != "?"]

    for se in s_words:
        for i, w in enumerate(words):
            if w ==se:
                bag[i]=1

    return numpy.array(bag).reshape(1,len(words))

def chat():
    print("Start talking with the bot and enter 'quit' to exit")
    while True:
        inp= input("You: ")
        if inp.lower() == "quit":
            break
        
        results = model.predict([bag_of_words(inp, words)])
        results_index=numpy.argmax(results)
        tag = labels[results_index]

        if results[0][results_index] > 0.7:
            for tg in data["intents"]:
                if tg["tag"]==tag:
                    responses = tg["responses"]
                    print(random.choice(responses))
        else:
            print("I didn't get that, try asking a ralevant question.")
        
def chatbot_response(msg):
    results = model.predict([bag_of_words(msg, words)])
    results_index=numpy.argmax(results)
    tag = labels[results_index]

    if results[0][results_index] > 0.7:
        for tg in data["intents"]:
            if tg["tag"]==tag:
                responses = tg["responses"]
                return random.choice(responses)
    else:
        return "I didn't get that, try asking a relevant question."


#chat()