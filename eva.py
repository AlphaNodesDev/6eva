import speech_recognition as sr
from gtts import gTTS
import os
import openai
import pygame
import time

openai.api_key = "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"

def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        return None

def generate_response(prompt):
    try:
        if "Who is your Father" in prompt.lower():
            return "I am an artificial intelligent bot created by UKF College of Engineering."

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100
        )
        return response.choices[0].text.strip()

    except openai.error.RateLimitError as rate_limit_error:
        return "I'm currently experiencing high demand. Please try again later."

def speak(text):
    tts = gTTS(text=text, lang="en")
    tts.save("response.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load("response.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(1)

    pygame.mixer.quit()

def main():
    assistant_name = "eva"
    assistant_description = "I am your virtual assistant created by UKF College students."
    print(f"Hello! I am {assistant_name}. {assistant_description}")

    while True:
        user_input = recognize_speech()

        if user_input:
            if user_input.lower() == "exit":
                print("Goodbye!")
                break

            prompt = f"{assistant_name}: {assistant_description}\nUser: {user_input}\n{assistant_name}:"
            response = generate_response(prompt)
            print(f"{assistant_name}: {response}")
            speak(response)

if __name__ == "__main__":
    main()
