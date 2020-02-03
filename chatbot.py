import nltk
nltk.download('punkt')
# Stemmer tool bahasa indonesia
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
factory = StemmerFactory()
stemmer = factory.create_stemmer()

import numpy
import tflearn
import tensorflow
import random
import json
import os
import pickle

with open("intents.json") as file:
  data = json.load(file)

try: 
  with open("chatbot.pickle", "rb") as c:
    words, labels, training,output=pickle.load(c)

except:
  words = [] # list kata di pattern
  labels = [] # list tag
  docs_x = [] # list kalimat di pattern
  docs_y = [] # list tag dengan jumlah sama dengan jumlah pattern

  for intent in data ["intents"]:
    for pattern in intent["patterns"]:
      # Mecah pattern jadi perkata
      wrds = nltk.word_tokenize(pattern)
      words.extend(wrds)
      docs_x.append(wrds)
      docs_y.append(intent["tag"])

    if intent["tag"] not in labels:
      labels.append(intent["tag"])

  # Memecah tiap kata menjadi lebih kecil dan tidak redundant
  words = [stemmer.stem(w.lower()) for w in words if w != "?"]
  words = sorted(list(set(words)))

  labels = sorted(labels)

  training = []
  output = []

  # Membentuk model dari tag dalam bentuk binary list
  out_empty = [0 for _ in range(len(labels))]

  for x, doc in enumerate(docs_x):
    bag = []

    # Kata yang udah distem di words dicek per huruf apakah ada di tiap kalimat di pattern
    wrds = [stemmer.stem(w.lower()) for w in doc]

    for w in words:
      if w in wrds:
        bag.append(1)
      else:
        bag.append(0)
    # Bikin model label dalam bentuk binary
    output_row = out_empty[:]
    output_row[labels.index(docs_y[x])] = 1
    # bikin model words atau kata dari tiap pattern
    training.append(bag)
    output.append(output_row)

  training = numpy.array(training)
  output = numpy.array(output)

  with open("chatbot.pickle", "wb") as c:
    pickle.dump((words,labels,training,output),c)

  tensorflow.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 3)
net = tflearn.fully_connected(net, 3)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)


if os.path.exists("model.tflearn.meta"):
  model.load("model.tflearn")
else:
  model.fit(training, output, n_epoch=1000, batch_size=3, show_metric=True)
  model.save("model.tflearn")

def bag_words(sentence):
    bag=[0 for _ in range(len(words))]
    word_new=nltk.word_tokenize(sentence)
    word_new=[stemmer.stem(word.lower()) for word in word_new]

    for se in word_new:
        for x, e in enumerate(words):
            if se == e :
                bag[x]=1

    return numpy.array(bag)

def bot_reply(text):
  text_input = text.lower()
  result = model.predict([bag_words(text_input)])
  # index tag dengan probabilitas tertinggi
  response_index = numpy.argmax(result)
  bot_answer = labels[response_index]
  # bot menjawab jika result > 0.6
  if result[0][response_index] > 0.6:
    for classes in data['intents']:
      if classes['tag'] == bot_answer:
        responses = classes['responses']
    return str(random.choices(responses)[0])
  else:
    return "Duh maaf, aku ngga ngerti"


def bot_action():
    print("Start talking with Me")
    print("========================")
    
    while True:
        inp=input("Kamu:")
        if inp.lower() == "quit":
            break
        result=model.predict([bag_words(inp)])
        # index tag dengan probabilitas tertinggi
        response_index=numpy.argmax(result)
        bot_answer=labels[response_index]
        # bot menjawab jika result > 0.7
        if result[0][response_index] > 0.6:
          for tg in data['intents']:
              if tg['tag']==bot_answer:
                  responses=tg['responses']
          print("Tukulsa:",str(random.choices(responses)[0]))
        else:
          print("Tukulsa: Duh, aku kudu jawab piye? Ngga ngerti aku")

bot_action()