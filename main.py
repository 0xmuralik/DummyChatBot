import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer= LancasterStemmer()
#nltk.download('punkt')
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

words=[]
lables=[]
docs_x=[]
docs_y=[]

for intent in data["intents"]:
    for pattern in intent["patterns"]:
         wrds=nltk.word_tokenize(pattern)
         words.extend(wrds)
         docs_x.append(wrds)
         docs_y.append(intent["tag"])

    if intent["tag"] not in lables:
        lables.append(intent["tag"])

words =[stemmer.stem(w.lower()) for w in words if w != "?"]
words=sorted(list(set(words)))

lables=sorted(lables)

training=[]
output=[]

out_empty =[0 for _ in range(len(lables))]

for x,doc in enumerate(docs_x):
    bag=[]

    wrds =[stemmer.stem(w) for w in doc]

    for w in words:
        if w in wrds:
            bag.append(1)
        else:
            bag.append(0)
    output_row=out_empty[:]
    output_row[lables.index(docs_y[x])]=1

    training.append(bag)
    output.append(output_row)

training=numpy.array(training)
output=numpy.array(output)


model= Sequential()

model.add(Dense(8, input_shape=(len(training[0]),)))
model.add(Dense(8))
model.add(Dense(len(output[0]),activation="softmax"))

model.compile(optimizer="sgd",loss="categorical_crossentropy")

model.summary()

model.fit(x=training,y=output,batch_size=8,epochs=1000)

model.save("Initial_model")

with open("data.pickle", "wb") as f:
        pickle.dump((words, lables), f)
