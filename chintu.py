import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import threading

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
    speak(f"The time is {current_time}.")

def news(_=None):
    speak("The current news is that the college is having winter vacations.")
    speak("Arpit created a voice assistant like Jarvis named Chintu.")

def call(command):
    contact_name = command.replace("call", "").strip()
    if contact_name:
        speak(f"Calling {contact_name}.")
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

# Command registry
commands = {
    "open": open_website,
    "time": tell_time,
    "news": news,
    "call": call,
    "music": play_music
}

# Listen for commands
def listen_command():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
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
    while True:
        print("Listening for wake word...")
        command = listen_command()
        if wake_word in command:
            speak("Yes sir?")
            command = listen_command()

            if not command:
                continue

            # Match command keywords
            matched = False
            for keyword, func in commands.items():
                if keyword in command:
                    func(command)
                    matched = True
                    break

            if not matched:
                if "hello" in command:
                    speak("Hello! How can I assist you today?")
                elif "exit" in command or "stop" in command:
                    speak("Goodbye!")
                    break
                else:
                    speak("I'm sorry, I didn't understand that.")

if __name__ == "__main__":
    # Run in a separate thread to avoid blocking
    assistant_thread = threading.Thread(target=main)
    assistant_thread.start()