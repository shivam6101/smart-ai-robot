import pyttsx3
import speech_recognition as sr
r = sr.Recognizer()
mic = sr.Microphone()

engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", 180)
print(voices)
while True:
    with mic as source:
        print('say')
        r.adjust_for_ambient_noise(source)
        audio = r.record(source,duration=2)
    try:
        a=r.recognize_google(audio)
        print(a)
        engine.say(a)
        engine.runAndWait()
    except:
        print('wrong')
    

