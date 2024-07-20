import speech_recognition as sr

r = sr.Recognizer()

mic = sr.Microphone()

with mic as source:
    r.adjust_for_ambient_noise(source)
    print("I'm Listening -")
    audio = r.listen(source)
    print("Thinking")

    print(r.recognize_google(audio))