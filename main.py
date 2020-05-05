import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer= LancasterStemmer()


import numpy
import tensorflow
import tflearn
import random
import json
import datetime



with open('intents.json') as file:
    data=json.load(file)

words=[]
labels=[]
docs_x=[]
docs_y=[]

for intent in data['intents']:
    for pattern in intent["patterns"]:
        wrds=nltk.word_tokenize(pattern)
        words.extend(wrds)
        docs_x.append(wrds)
        docs_y.append(intent['tag'])


        if intent['tag'] not in labels:
            labels.append(intent['tag'])

words= [stemmer.stem(W.lower()) for W in words if W not in "?"]
words= sorted(list(set(words)))

labels= sorted(labels)

training =[]
output=[]

out_empty=[0 for _ in range(len(labels))]
for x , doc in enumerate(docs_x):
    bag=[]
    wrds=[stemmer.stem(W) for W in doc]

    for w in words:
        if w in wrds:
            bag.append(1)
        else:
            bag.append(0)

    output_row=out_empty[:]
    output_row[labels.index(docs_y[x])]=1

    training.append(bag)
    output.append(output_row)

training= numpy.asarray(training)
output=numpy.array(output)


tensorflow.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

try:
    model.load("model.tflearn")
except:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return numpy.array(bag)


def chat(inp):
    results = model.predict([bag_of_words(inp, words)])
    temp=numpy.asarray(results)
    if temp.max()< .6:
        unknownQ = open("UnknownQ.txt", "a")
        unknownQ.write(inp+" \n")
        unknownQ.close()
        return "Sorry I cant Understand! Please ask again."
    else:
        results_index = numpy.argmax(results)
        tag = labels[results_index]
        if tag=="time":
            return time_now(inp)
        else:
            for tg in data["intents"]:
                if tg['tag'] == tag:
                    responses = tg['responses']
            x=random.choice(responses)
            print(x)
            return x

def time_now(inp):
    if "today" in inp or "date" in inp:
        x = datetime.datetime.now()
        return x.strftime("%d %B %Y")
    elif 'time' in inp:
        x= datetime.datetime.now()
        return  x.strftime("%I:%M %p")
    else:
        x = datetime.datetime.now()
        return x.strftime("%X %x")
