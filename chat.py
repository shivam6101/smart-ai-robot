import nltk
import pyttsx3
engine = pyttsx3.init()
from nltk.stem import WordNetLemmatizer
lemmatizer=WordNetLemmatizer()
import pickle
import numpy as np
import speech_recognition as sr
r=sr.Recognizer()
mic=sr.Microphone()

import tensorflow as tf
from tensorflow.keras.models import load_model
model=load_model('chatbot_model.h5')
import json
import random

intents=json.loads(open('intents.json').read())
words=pickle.load(open('words.pkl','rb'))
classes=pickle.load(open('classes.pkl','rb'))

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words
def bow(sentence,words):
    sentence_output=clean_up_sentence(sentence)
    bag=[0]*len(words)
    for s in sentence_output:
        for i,w in enumerate(words):
            if w==s:
                bag[i]=1
    return(np.array(bag))
def predict_class(sentence,model):
    p=bow(sentence,words)
    output=model.predict(np.array([p]))[0]
    threshold=0.25
    result=[[i,r] for i,r in enumerate(output) if r>threshold]
    result.sort(key=lambda x: x[1],reverse=True)
    return_list=[]
    answer=[]
    for r in result:
        return_list.append({"intent":classes[r[0]],'probability':str(r[1])})
        for intent in intents['intents']:
            if classes[r[0]]==intent['tag']:
                answer=(random.choice(intent['responses']))
                voices = engine.getProperty("voices")
                engine.setProperty("voice", voices[1].id)
                engine.setProperty("rate", 180)
                engine.say(answer)
                engine.runAndWait()
                #print(f"Alexa: {random.choice(intent['responses'])}")
                print(f"Alexa: {answer}")


while True:
    with mic as source:
        print('Alexa: Say something')
        r.adjust_for_ambient_noise(source)
        audio = r.record(source,duration=2)
    try:
        a=r.recognize_google(audio)
        #sentence=input('you: type message  ')
        print(f'you: {a}')
        if a=='ok bye':
            text="see you sir have a nice day"
            voices=engine.getProperty('voices')
            engine.setProperty("voice", voices[1].id)
            engine.setProperty('rate',180)
            engine.say(text)
            engine.runAndWait()
            break
        p=predict_class(a,model)
    except:
        text="I Do Not Understand"
        print(f"Alexa: {text}")


