import os
import speech_recognition as sr
import pyttsx3
import openai
import requests
import cv2
import tensorflow as tf
import torch
import transformers 
import pipeline
from fastapi import FastAPI
import uvicorn


recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()
chatbot = pipeline("text-generation", model="gpt2")


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "AIOS is running"}

def ai_assistant():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio).lower()
            print("User said:", command)
            response = chatbot(command, max_length=50, num_return_sequences=1)[0]['generated_text']
            print("AIOS:", response)
            tts_engine.say(response)
            tts_engine.runAndWait()
        except sr.UnknownValueError:
            print("Could not understand the audio")
        except sr.RequestError:
            print("Error with speech recognition")

def ai_camera():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('AI Camera', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def check_security():
    response = requests.get("https://api.hackertarget.com/iplookup/?q=8.8.8.8")
    print("Security Check:", response.text)

if __name__ == "__main__":
    print("AI Operating System is starting...")
    ai_assistant()
    ai_camera()
    check_security()
    uvicorn.run(app, host="0.0.0.0", port=8000)