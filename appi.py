import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime

# Initialize the speech recognition and text-to-speech engine
r = sr.Recognizer()
engine = pyttsx3.init()

# Set up wake-up keyword
wake_word = "chintu"

# Define function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Define function for opening a website
def open_website(command):
    if "open" in command:
        website_name = command.split("open")[-1].strip()
        if website_name:
            if not website_name.startswith("http"):
                website_name = "http://" + website_name
            webbrowser.open(website_name)
            speak(f"Opening {website_name}.")
        else:
            speak("Please specify a website to open.")
    else:
        speak("I'm not sure what you want me to open.")

# Define function for telling the time
def tell_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {current_time}.")
    
# Define function for telling the college news
def news():
    speak("The current news is that the college is having winter vacations.")
    speak("Arpit created a voice assistant like Jarvis named Chintu.")
    
# Define function to simulate a call
def call(command):
    if "call" in command:
        contact_name = command.split("call")[-1].strip()
        if contact_name:
            speak(f"Calling {contact_name}.")
            speak("beep " * 4)  # Simulate ringing
            speak("Sorry, the person is not responding.")
        else:
            speak("Please specify who to call.")
    else:
        speak("I'm not sure what you want me to do.")

# Main loop to keep the assistant running
def main():
    while True:
        with sr.Microphone() as source:
            print("Listening for wake word...")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

        try:
            command = r.recognize_google(audio).lower()
            print("You said: " + command)

            if wake_word in command:
                speak("Yes sir?")
                
                with sr.Microphone() as source:
                    print("Listening for command...")
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)

                try:
                    command = r.recognize_google(audio).lower()
                    print("You said: " + command)

                    if "open" in command:
                        open_website(command)
                    elif "hello" in command:
                        speak("Hello! How can I assist you today?")
                    elif "time" in command:
                        tell_time()
                    elif "news" in command:
                        news()
                    elif "call" in command:
                        call(command)
                    elif "exit" in command or "stop" in command:
                        speak("Goodbye!")
                        break
                    else:
                        speak("I'm sorry, I didn't understand that.")
               
                except sr.UnknownValueError:
                    print("Could not understand the audio.")
                    speak("I didn't catch that. Could you please repeat?")
                except sr.RequestError:
                    print("Could not request results from the speech recognition service.")
                    speak("There seems to be an issue with the speech recognition service.")

        except sr.UnknownValueError:
            print("Could not understand the audio.")
        except sr.RequestError:
            print("Could not request results from the speech recognition service.")

if __name__ == "__main__":
    main()