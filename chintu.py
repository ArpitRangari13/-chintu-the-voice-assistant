import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import time
import requests

# Initialize recognizer and TTS engine
r = sr.Recognizer()
engine = pyttsx3.init()

# Wake word
wake_word = "chintu"

# Common websites mapping
sites = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "github": "https://www.github.com",
    "facebook": "https://www.facebook.com"
}

# Speak function
def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

# Command functions
def open_website(command):
    website_name = command.replace("open", "").strip()
    if website_name in sites:
        webbrowser.open(sites[website_name])
        speak(f"Opening {website_name}.")
    elif website_name:
        if not website_name.startswith("http"):
            website_name = "http://" + website_name
        webbrowser.open(website_name)
        speak(f"Opening {website_name}.")
    else:
        speak("Please specify a website to open.")

def tell_time(_=None):
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"Samay hai {current_time}.")

def news(_=None):
    try:
        # Example using NewsAPI (replace YOUR_API_KEY with your key from https://newsapi.org)
        url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=YOUR_API_KEY"
        response = requests.get(url)
        data = response.json()
        if "articles" in data:
            headlines = [article["title"] for article in data["articles"][:3]]
            for h in headlines:
                speak(h)
        else:
            speak("Sorry, I could not fetch the latest news.")
    except Exception:
        speak("There was an error fetching the news.")

def call(command):
    contact_name = command.replace("call", "").strip()
    if contact_name:
        speak(f"{contact_name} ko call kar raha hoon...")
        # Simulated call – integrate Twilio/Skype/WhatsApp API for real calls
        speak("Sorry, the person is not responding.")
    else:
        speak("Please specify who to call.")

def play_music(command):
    song_name = command.replace("music", "").strip()
    if song_name:
        speak(f"Searching YouTube for {song_name}.")
        query_url = f"https://www.youtube.com/results?search_query={song_name.replace(' ', '+')}"
        webbrowser.open(query_url)
    else:
        speak("Playing default music.")
        webbrowser.open("https://youtube.com/shorts/HYqTLO0bhnE?si=6Ll60-ql765OBkn6")

# Command registry with Hindi phrases
commands = {
    "open": open_website,
    "time batao": tell_time,
    "news batao": news,
    "call": call,
    "music": play_music
}

# Listen for speech
def listen(source):
    try:
        audio = r.listen(source)
        command = r.recognize_google(audio).lower()
        print("You said:", command)
        return command
    except sr.UnknownValueError:
        speak("I didn't catch that. Could you please repeat?")
    except sr.RequestError:
        speak("There seems to be an issue with the speech recognition service.")
    return ""

# Main loop
def main():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        speak("Chintu is online and listening...")

        while True:
            print("Listening for wake word...")
            command = listen(source)

            if wake_word in command:
                speak("Bolo Sir ji")  # Changed response
                time.sleep(1)  # short pause so you can speak

                command = listen(source)

                if not command:
                    continue

                matched = False
                for keyword, func in commands.items():
                    if keyword in command:
                        func(command)
                        matched = True
                        break

                if not matched:
                    if "hello" in command:
                        speak("Hello! How can I assist you today?")
                    elif "bye" in command or "exit" in command or "stop" in command:
                        speak("Goodbye Sir ji!")
                        break
                    else:
                        speak("I'm sorry, I didn't understand that.")

if __name__ == "__main__":
    main()