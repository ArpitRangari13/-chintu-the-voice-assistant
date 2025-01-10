import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import tkinter as tk
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk
import cv2

# Initialize the speech recognition and text-to-speech engine
r = sr.Recognizer()
engine = pyttsx3.init()

# Set up wake-up keyword
wake_word = "chintu"

# Define function to convert text to speech
def speak(text):
    print(f"Assistant: {text}")  # Print what the assistant is saying
    chat_area.insert(tk.END, f"Assistant: {text}\n")
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
    messagebox.showinfo("Current Time", f"The time is {current_time}.")

# Define function for telling the college news
def college_news():
    speak("The current news is that the college is having winter vacations.")
    speak("Arpit created a voice assistant like Jarvis named Chintu.")
    speak("Arpit is currently the fifth topper with sgpa 9.26")
    speak("Arpit is working on women saftey as smart india hackathon topic")


# Define function to simulate a call
def call(command):
    if "call" in command:
        contact_name = command.split("call")[-1].strip()
        if contact_name:
            speak(f"Calling {contact_name}.")
            speak("Sorry, the person is not responding.")
        else:
            speak("Please specify who to call.")
    else:
        speak("I'm not sure what you want me to do.")

# Function for playing music
def play_music(command):
    if "music" in command:
        website_name = "https://youtube.com/shorts/HYqTLO0bhnE?si=6Ll60-ql765OBkn6"
        webbrowser.open(website_name)
        speak("Playing music.")
    else:
        speak("Please specify a command to play music.")

# Function to listen for commands
def listen_command():
    with sr.Microphone() as source:
        print("Listening for command...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).lower()
        print("You said: " + command)
        chat_area.insert(tk.END, f"You: {command}\n")

        process_command(command)
    except sr.UnknownValueError:
        print("Could not understand the audio.")
        speak("I didn't catch that. Could you please repeat?")
    except sr.RequestError:
        print("Could not request results from the speech recognition service.")
        speak("There seems to be an issue with the speech recognition service.")
        
def how_to_contact(command):
    if "contact" in command:
        speak("You can contact {command} sending an email to arpit@gmail.com or by calling on 1234567890.")
    

def process_command(command):
    if "open" in command:
        open_website(command)
    elif "hello" in command:
        speak("Hello! How can I assist you today?")
    elif "time" in command:
        tell_time()
    elif "news" in command:
        college_news()
    elif "call" in command:
        call(command)
    elif "music" in command:
        play_music(command)
    elif "exit" in command or "stop" in command:
        speak("Goodbye!")
        root.quit()
    elif "contact" in command:
        how_to_contact(command)
    else:
        # Direct the unrecognized command to Google
        search_query = command.replace(" ", "+")  # Replace spaces with '+' for the URL
        google_search_url = f"https://www.google.com/search?q={search_query}"
        webbrowser.open(google_search_url)
        speak(f"Searching Google for {command}.")

def send_command(event=None):
    command = entry_field.get()
    if command:
        chat_area.insert(tk.END, f"You: {command}\n")
        entry_field.delete(0, tk.END)
        process_command(command.lower())

# Function to play video
class VideoPlayer:
    def __init__(self, window, video_source):
        self.window = window
        self.window.title("Voice Assistant with Video")
        self.label = tk.Label(window, bg='black')
        self.label.grid(row=0, column=0, sticky="nsew")  # Fill the entire window

        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        # Set the desired width and height for the video
        self.width = 640
        self.height = 480

        # Start the video playback
        self.update()

    def update(self):
        # Get the next frame from the video
        ret, frame = self.vid.read()
        if not ret:
            # If the video has ended, reset to the beginning
            self.vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.vid.read()
        
        if ret:
            # Resize the frame to the specified dimensions
            frame = cv2.resize(frame, (self.width, self.height))
            # Convert the frame to RGB format
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Convert the frame to a PhotoImage
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)
        # Call this function again after 20 ms
        self.label.after(20, self.update)

    def on_closing(self):
        # Release the video capture object when closing
        self.vid.release()

# Create the main window
root = tk.Tk()
root.title("Voice Assistant with Video")
root.configure(bg='black')  # Set the background color to black

# Configure grid layout
root.grid_rowconfigure(0, weight=1)  # Video row
root.grid_rowconfigure(1, weight=0)  # Chat area row
root.grid_rowconfigure(2, weight=0)  # Entry field row
root.grid_rowconfigure(3, weight=0)  # Button row
root.grid_columnconfigure(0, weight=1)  # Single column

# Path to the local video file
video_path = r"C:\Users\arpit\Downloads\79593-570048633_small.mp4"  # Change this to your local video file path

# Create a VideoPlayer object
video_player = VideoPlayer(root, video_path)

# Create a canvas for transparency effect
canvas = tk.Canvas(root, bg='black', highlightthickness=0)
canvas.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

# Create a solid rectangle
canvas.create_rectangle(0, 0, 640, 100, fill="black", outline="")  # Use solid black for the rectangle

# Create a scrolled text area for conversation
chat_area = scrolledtext.ScrolledText(canvas, wrap=tk.WORD, bg='black', fg='white', insertbackground='white', font=('Helvetica', 12))
chat_area.place(relwidth=1, relheight=1)  # Position the chat area

# Create an entry field for user input
entry_field = tk.Entry(canvas, bg='black', fg='white', insertbackground='white', font=('Helvetica', 12))
entry_field.place(relwidth=1, rely=0.9, relheight=0.1)  # Position the entry field

entry_field.bind("<Return>", send_command)  # Bind the Enter key to send command

# Create a button to listen for commands
listen_button = tk.Button(root, text="Listen", command=listen_command, padx=20, pady=10, bg='gray', fg='white', font=('Helvetica', 12))
listen_button.grid(row=3, column=0, sticky="ew", padx=10, pady=5)  # Position the listen button

# Start the Tkinter event loop
root.mainloop()