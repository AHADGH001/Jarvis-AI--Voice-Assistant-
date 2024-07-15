import openai
import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from gtts import gTTS
import pygame
import os

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init() 
newsapi = "your key"

# Function to use pyttsx3 for speaking
def speak_old(text):
    engine.say(text)
    engine.runAndWait()

# Function to use gTTS and Pygame for speaking
def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 

# Function to process commands using OpenAI
def aiProcess(command):
    openai.api_key = "your key"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses, please"},
            {"role": "user", "content": command}
        ]
    )

    return response['choices'][0]['message']['content']

# Function to process specific commands
def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music.get(song, None)
        if link:
            webbrowser.open(link)
        else:
            speak("Song not found in the music library.")
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            for article in articles:
                speak(article['title'])
        else:
            speak("Unable to fetch news at the moment.")
    else:
        output = aiProcess(c)
        speak(output) 

if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        try:
            # Listen for the wake word "Jarvis"
            print("Recognizing...")
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                print("Listening...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            try:
                word = recognizer.recognize_google(audio)
                print(f"Recognized word: {word}")
                if word.lower() == "jarvis":
                    speak("Yes")
                    with sr.Microphone() as source:
                        print("Jarvis Active...")
                        recognizer.adjust_for_ambient_noise(source)
                        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                        try:
                            command = recognizer.recognize_google(audio)
                            print(f"Recognized command: {command}")
                            processCommand(command)
                        except sr.UnknownValueError:
                            print("Could not understand the command.")
                            speak("I didn't catch that. Can you please repeat?")
                        except sr.RequestError as e:
                            print(f"Could not request results from Google Speech Recognition service; {e}")
                            speak("I'm having trouble connecting to the recognition service.")
            except sr.UnknownValueError:
                print("Could not understand the wake word.")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                speak("I'm having trouble connecting to the recognition service.")
        except Exception as e:
            print(f"An error occurred: {e}")
            speak("An error occurred. Please try again.")
