import nltk
nltk.download('punkt')
# Stemmer tool bahasa indonesia
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
factory = StemmerFactory()
stemmer = factory.create_stemmer()

import string
import re
import numpy
import tflearn
import tensorflow
import random
import json
import os
import pickle

context_chat = {
    "ping":"Kenape? Berisik amat",
    "salam":"kumsalaam",
    "halo":"haloo kak {}",
    "beli pulsa":"oke kak, boleh minta nomor hapenya? Formatnya 08xxxxxxx ya",
    "complaint":"Oke kak {}, saya akan bantu cek status pembeliannya ya kak",
    "terima kasih":"iya kak {}, sama-sama :)",
    "cek riwayat":"Oke kak {}, berikut riwayat transaksinya ya kak",
    "cek riwayat semua":"Oke kak {}, berikut riwayat transaksinya ya kak",
    "cek produk":"Lengkap kak, Ini daftar operatornya. Bisa dipilih",
    "cek produk spesifik":"Ini list pulsanya ya kak",
    "keluar konteks":"Sori cuy, ane cuma jual pulsa. Kalo mau beli langsung chat aja, jangan aneh-aneh",
    "tanya beneran":"aku Tukulsa, kerjaannya ya cuma nawarin pulsa sama jual pulsa. Jangan nanya doang, beli dong",
    "low prob":"Maksudnya apa tuh kak?",
    "admin login":"Silahkan, tuan {}"
}

with open("intents.json") as file:
  data = json.load(file)

try: 
  with open("chatbot.pickle", "rb") as c:
    words, labels, training,output=pickle.load(c)

except:
  initial_words = [] # list kata di pattern
  labels = [] # list tag
  docs_x = [] # list kalimat di pattern
  docs_y = [] # list tag dengan jumlah sama dengan jumlah pattern

  for intent in data ["intents"]:
    for pattern in intent["patterns"]:
      # Tokenized the data
      wrds = nltk.word_tokenize(pattern)
      initial_words.extend(wrds)
      docs_x.append(wrds)
      docs_y.append(intent["tag"])

    if intent["tag"] not in labels:
      labels.append(intent["tag"])

  # Stemming and cleaning the data (remove punctuation and make it all lower case)
  words = []
  list_of_punctuation = string.punctuation
  for word in initial_words:
    word = word.lower()
    word = re.sub('[%s]' % re.escape(list_of_punctuation), '', word)
    word = stemmer.stem(word)
    words.append(word)

  words = list(set(words))
  labels = labels

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
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)


if os.path.exists("model.tflearn.meta"):
  model.load("model.tflearn")
else:
  model.fit(training, output, n_epoch=1500, batch_size=8, show_metric=True)
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
    return bot_answer
  else:
    return "low prob"


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
          print(bot_answer)
          print("Tukulsa:", context_chat[bot_answer])
        else:
          print("Tukulsa: Duh, aku kudu jawab piye? Ngga ngerti aku")

if __name__ == "__main__":
  bot_action()
