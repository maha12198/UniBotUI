#libraries needed for NLP
import nltk
nltk.download('punkt')
 #this is required to do the stemming
from nltk.stem.lancaster import LancasterStemmer
# creating an object and store it in stemmer
stemmer = LancasterStemmer()

#libraries needed for tensorflow
import numpy as np
import tflearn
#import tensorflow.compat.v1 as tf
#tf.disable_v2_behavior()
import random
#import json
import pickle


with open("data.pickle","rb") as f:
      #save all of these data in our pickle file
     data, words, labels, training, output = pickle.load(f)


net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

# Define the  model
model = tflearn.DNN(net)

model.load("model.tflearn")

# this is for the input, the prevoius one was for the ouptput
def bag_of_words(s, words):
   
   # bag of words
    bag = [0 for _ in range(len(words))]

    #tokenize the pattern
    s_words = nltk.word_tokenize(s)
    #stem each word
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
               # print ("found in bag: %se" % w)
            
    return np.array(bag)

def chat(msg):
    #print("Hi there, I am UniBot. How can I help you?")
    #while True:
        print(msg)
        #inp = input("You: ")
        inp = msg
        if inp.lower() == "quit":
            #break
           print("really worlking")
         
        # generate probabilities from the model
        #the [0] is important to start from 0 in new list and solve the problem of out of index
        results = model.predict([bag_of_words(inp, words)])[0]
       
        results_index = np.argmax(results) 
        tag = labels[results_index]

        #new if statement for customization to say sorry       
        if results[results_index] > 0.7:
            for tg in data["intents"]:
                # find a tag matching the first result?
                if tg['tag'] == tag:
                    responses = tg['responses']
                        
            return (random.choice(responses))
        else:
            answer="Sorry, I didn't get that. Try again or ask a different question."
            return (answer)