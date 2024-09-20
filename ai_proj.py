import customtkinter as ctk
import pyautogui
from PIL import Image, ImageTk
import tkinter.messagebox as messagebox
import speech_recognition as sr
import wikipedia
import pyttsx3
import webbrowser
import sqlite3
import requests

from requests_oauthlib import OAuth2Session
import json
from requests.auth import HTTPBasicAuth
# -------------------------------------------- Database functions ------------------------------------

def DB_login(username,password):

    # variable to return
    res = False

    # connecting py file to the database file
    connection = sqlite3.connect('../../DB/Users.db')

    # starts the running by making the cursor point to current db
    cursor = connection.cursor()

    # searching for the user by the UNIQUE username
    cursor.execute('SELECT username FROM users WHERE username = ?', [username])

    #reading the result of searching
    result = cursor.fetchone()

    if result is None:
        #print('There is no such username')
        messagebox.showerror("Login Failed", "There is no such username")
        res = False
    else:
        # reading the password
        cursor.execute('SELECT password FROM users WHERE username = ?', [username])

        # fetching the password
        result = cursor.fetchone()

        # comparing the input with the password
        if result[0] != password:
            #print('Wrong password.')
            messagebox.showerror("Login Failed", "Wrong password")
            res = False
        else:
            res = True

    connection.close()
    return res

def DB_sign_up(first_name,last_name,username,password, email,sub_period):

    connection = sqlite3.connect('../../DB/Users.db')
    cursor = connection.cursor()

    # searching for the user by the UNIQUE username
    cursor.execute('SELECT username FROM users WHERE username = ?', [username])

    #reading the result of searching
    result = cursor.fetchone()

    if result != None:
        #print('Username already taken.')
        messagebox.showerror("sign up Failed", "username is already taken")

    # inserting the data to the database
    cursor.execute('''INSERT INTO Users (FirstName, LastName , Username , password , email, subscriptionPeriod)
                    values (?,?,?,?,?,?)''', [first_name, last_name, username, password, email,sub_period])

    #print('User created successfully.')
    messagebox.showinfo("Statue", "Sign Up Complete")
    connection.commit()
    connection.close()
# -------------------------------------------- Database functions ------------------------------------

scrcr=0
tasks = []
listeningToTask = False

def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening for commands...")
        Speak("Waiting for command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print("You said:" + command)
        #Speak("You said:" + command)
        return command.lower()
    except sr.UnknownValueError:
        print("Could not understand audio. Please try again.")
        Speak("Could not understand audio. Please try again.")
        return None
    except sr.RequestError:
        print("Unable to access the Google Speech Recognition API.")
        Speak("Unable to access the Google Speech Recognition API.")
        return None


def Speak(txt):
    rate = 90
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', rate + 50)
    engine.say(txt)
    engine.runAndWait()


def body():
    global tasks
    global listeningToTask
    # respond("Hello, Jake. I hope you're having a nice day today.")
    while True:
        command = listen()
        triggerKeyword = "jarvis"

        if command and (triggerKeyword in command):
            if listeningToTask:
                tasks.append(command)
                listeningToTask = False
                Speak("Adding " + command + " to your task list. You have " + str(len(tasks)) + " currently in your list.")
            elif "add a task" in command:
                listeningToTask = True
                Speak("Sure, what is the task?")
                break
            elif "list tasks" in command:
                Speak("Sure. Your tasks are: ")
                for task in tasks:
                    Speak(task)
                break
            elif "take a screenshot" in command:
                pyautogui.screenshot("screenshot.png")
                Speak("I took a screenshot for you.")
                break
            elif "open browser" in command:
                Speak("Opening browser.")
                webbrowser.open("http://www.google.com/")
                break
            elif "search" in command:
                pass  # move to summaries frame
            elif "exit" in command:
                Speak("Goodbye Sir! , Hope I could help you.")
                break
            else:
                Speak("Sorry, I'm not sure how to handle that command.")


class AIProjectApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("AI Assistant")
        self.login_frame = LoginFrame(self)
        self.login_frame.pack(fill="both", expand=True)

        self.sign_up_frame = SignUpFrame(self)
        self.main_frame = MainFrame(self)
        self.voice_frame = VoiceFrame(self)

    def show_login(self):
        self.sign_up_frame.pack_forget()
        self.main_frame.pack_forget()
        self.voice_frame.pack_forget()
        self.login_frame.pack(fill="both", expand=True)

    def show_sign_up(self):
        self.login_frame.pack_forget()
        self.main_frame.pack_forget()
        self.voice_frame.pack_forget()
        self.sign_up_frame.pack(fill="both", expand=True)

    def show_main(self):
        self.login_frame.pack_forget()
        self.sign_up_frame.pack_forget()
        self.voice_frame.pack_forget()
        self.main_frame.pack(fill="both", expand=True)

    def show_voice(self):
        self.login_frame.pack_forget()
        self.sign_up_frame.pack_forget()
        self.main_frame.pack_forget()
        self.voice_frame.pack(fill="both", expand=True)


class LoginFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        # Load and resize the background image to fit the frame
        self.bg_image = Image.open("C:\\Me\\AIProject\\AIProject\\AI.PNG")
        self.bg_image = self.bg_image.resize((2000, 1000))
        self.bg_image_tk = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = ctk.CTkLabel(self, image=self.bg_image_tk)
        self.bg_label.place(relwidth=1, relheight=1)

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.place(relx=0.5, rely=0.5, anchor='center')

        label_width = 300  # Set your desired width here

        self.label = ctk.CTkLabel(self.container, text="Login", font=("Arial", 24), width=label_width)
        self.label.pack(pady=10)

        self.label2 = ctk.CTkLabel(self.container, text="Support", font=("Arial", 12), width=label_width)
        self.label2.pack(pady=0)

        self.label3 = ctk.CTkLabel(self.container, text="01067876014", font=("Arial", 10,"bold"), width=label_width)
        self.label3.pack(pady=1)


        self.username_entry = ctk.CTkEntry(self.container, placeholder_text="username")
        self.username_entry.pack(pady=5)

        self.password_entry = ctk.CTkEntry(self.container, placeholder_text="Password", show='*')
        self.password_entry.pack(pady=5)

        button_width = 150

        self.login_button = ctk.CTkButton(self.container, text="Login",font=("Arial", 12 , "bold"),text_color="black", command=self.login, width=button_width, fg_color="#f0f0f0", hover_color="#d0e3f1")
        self.login_button.pack(pady=5)

        self.google_button = ctk.CTkButton(self.container, text="Login with Google",font=("Arial", 12 , "bold"), text_color="black", command=self.google_login,fg_color="#f0f0f0", width=button_width, hover_color="red")
        self.google_button.pack(pady=5)

        # self.facebook_button = ctk.CTkButton(self.container, text="Login with Facebook", command=self.facebook_login, width=button_width, hover_color="blue")
        # self.facebook_button.pack(pady=5)

        self.sign_up_button = ctk.CTkButton(self.container, text="Sign Up",font=("Arial", 12 , "bold"),text_color="black", command=self.sign_up, width=button_width,fg_color="#f0f0f0", hover_color="green")
        self.sign_up_button.pack(pady=5)

        self.username_entry.bind("<Return>", lambda event: self.login())
        self.password_entry.bind("<Return>", lambda event: self.login())


    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        flag = DB_login(username,password)
        if flag:
            self.master.show_voice()

    def google_login(self):
        client_id = '830749082247-iopugsgb13hb36gkc7v76565s52q35ud.apps.googleusercontent.com'
        redirect_uri = 'http://localhost'
        scope = ['openid', 'email', 'profile']

        oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)

        authorization_url, state = oauth.authorization_url('https://accounts.google.com/o/oauth2/auth')

        webbrowser.open(authorization_url)

        redirect_response = input('Paste the full redirect URL here: ')
        token = oauth.fetch_token('https://oauth2.googleapis.com/token',
                                  authorization_response=redirect_response,
                                  client_secret='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')

        print("Access token:", token['access_token'])

        user_info_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
        response = oauth.get(user_info_url)
        if response.status_code == 200:
            user_info = response.json()
            print("User info:", user_info)
        else:
            messagebox.showerror("Failed to retrieve user info", response.text)

    def sign_up(self):
        self.master.show_sign_up()


class SignUpFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        self.master = master

        # Load and resize the background image to fit the frame
        self.bg_image = Image.open("C:\\Me\\AIProject\\AIProject\\ai2.jpeg")
        self.bg_image = self.bg_image.resize((2000, 1000))
        self.bg_image_tk = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = ctk.CTkLabel(self, image=self.bg_image_tk)
        self.bg_label.place(relwidth=1, relheight=1)

        self.container = ctk.CTkFrame(self, fg_color='transparent')
        self.container.place(relx=0.5, rely=0.5, anchor='center')

        label_width = 300  # Set your desired width here

        self.label = ctk.CTkLabel(self.container, text="Sign Up", font=("Arial", 24), width=label_width)
        self.label.pack(pady=10)

        self.first_name_entry = ctk.CTkEntry(self.container, placeholder_text="First Name")
        self.first_name_entry.pack(pady=5)

        self.last_name_entry = ctk.CTkEntry(self.container, placeholder_text="Last Name")
        self.last_name_entry.pack(pady=5)

        self.user_entry = ctk.CTkEntry(self.container, placeholder_text="Choose a unique user")
        self.user_entry.pack(pady=5)

        self.email_entry = ctk.CTkEntry(self.container, placeholder_text="Email")
        self.email_entry.pack(pady=5)

        self.password_entry = ctk.CTkEntry(self.container, placeholder_text="Password", show='*')
        self.password_entry.pack(pady=5)

        self.subscription_label = ctk.CTkLabel(self.container, text="Subscription Options:")
        self.subscription_label.pack(pady=5)

        self.subscription_var = ctk.IntVar(value=0)

        self.one_month_radio = ctk.CTkRadioButton(self.container, text="1 Month", variable=self.subscription_var, value=1)
        self.one_month_radio.pack(pady=5)

        self.three_months_radio = ctk.CTkRadioButton(self.container, text="3 Months", variable=self.subscription_var, value=3)
        self.three_months_radio.pack(pady=5)

        self.one_year_radio = ctk.CTkRadioButton(self.container, text="12 months", variable=self.subscription_var, value=12)
        self.one_year_radio.pack(pady=5)

        button_width = 200

        self.sign_up_button = ctk.CTkButton(self.container, text="Sign Up", command=self.sign_up, width=button_width)
        self.sign_up_button.pack(pady=5)

        self.back_button = ctk.CTkButton(self.container, text="Back to Login", command=self.back_to_login, width=button_width)
        self.back_button.pack(pady=10)


    def sign_up(self):
        if (self.first_name_entry.get() !="" and self.last_name_entry.get() !="" and self.user_entry.get()!="" and self.email_entry.get()!="" and self.password_entry.get()!="" and self.subscription_var.get()>0) :
            DB_sign_up(self.first_name_entry.get() , self.last_name_entry.get(), self.user_entry.get(), self.password_entry.get() ,self.email_entry.get(),self.subscription_var.get() )
            self.master.show_login()
        else:
            messagebox.showerror("Error", "Please enter missing data")

    def back_to_login(self):
        self.master.show_login()


class MainFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.container = ctk.CTkFrame(self, fg_color='transparent')
        self.container.pack(pady=10)

        self.search_entry = ctk.CTkEntry(self.container, placeholder_text="Search", width=500)
        self.search_entry.pack(side='left', padx=5)

        self.search_button = ctk.CTkButton(self.container, text="Search", command=self.search, width=80)
        self.search_button.pack(side='left', padx=5)

        self.mic_button = ctk.CTkButton(self.container, text="🎤", command=self.voice_search , width=30, height=30 , hover_color="green")
        self.mic_button.pack(side='left', padx=5)

        self.back_button = ctk.CTkButton(self.container, text="⬅️", command=self.master.show_voice , width=30, height=30 , hover_color="gray")
        self.back_button.pack(side='left', padx=5)

        self.result_text = ctk.CTkTextbox(self, wrap='word')
        self.result_text.pack(fill='both', expand=True, pady=10, padx=10)


        self.search_entry.bind("<Return>", lambda event: self.search())

    def search(self):
        query = self.search_entry.get()
        self.result_text.delete('1.0', 'end')
        rslt = wikipedia.summary("Line (" + self.search_entry.get() + ")")
        self.result_text.insert('end', rslt + "\n\n")


    def voice_search(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                print("Listening...")
                audio = recognizer.listen(source)
                query = recognizer.recognize_google(audio)
                self.search_entry.delete(0, 'end')
                self.search_entry.insert(0, query)
                self.search()
            except sr.RequestError:
                messagebox.showerror("Error", "Could not request results; check your network connection")
            except sr.UnknownValueError:
                messagebox.showerror("Error", "Could not understand audio")


class VoiceFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.container = ctk.CTkFrame(self, fg_color='transparent')
        self.container.place(relx=0.5, rely=0.5, anchor='center')

        self.mic_button = ctk.CTkButton(self.container, text="🎤", command=self.Main, width=300, height=280,
                                        font=("Arial", 100), hover_color="green")
        self.mic_button.pack(pady=10)

        self.summary_button = ctk.CTkButton(self.container, text="Summaries", command=self.show_summaries, width=200)
        self.summary_button.pack(pady=10)

        # self.stop_button= ctk.CTkButton(self.container, text="stop recording", width=200, font=("Arial", 20), hover_color="green", command=self.close_main())
        # self.stop_button.pack(pady=10)

    # def voice_search(self):
    #     recognizer = sr.Recognizer()
    #     with sr.Microphone() as source:
    #         try:
    #             print("Listening...")
    #             audio = recognizer.listen(source)
    #             query = recognizer.recognize_google(audio)
    #             messagebox.showinfo("Voice Input", f"You said: {query}")
    #             # Add further logic for processing the query
    #         except sr.RequestError:
    #             messagebox.showerror("Error", "Could not request results; check your network connection")
    #         except sr.UnknownValueError:
    #             messagebox.showerror("Error", "Could not understand audio")
    def show_login(self):
        self.master.show_login()
    def show_summaries(self):
        self.master.show_main()
    def close(self):
        self.master.destroy()
    def Main(self):
        global scrcr
        global tasks
        global listeningToTask
        # respond("Hello, Jake. I hope you're having a nice day today.")
        while True:
            command = listen()
            triggerKeyword = "jarvis"
            if command and (triggerKeyword in command):
                if listeningToTask:
                    #Speak("Waiting for your command Sir...")
                    tasks.append(command)
                    listeningToTask = False
                    Speak("Adding " + command + " to your task list. You have " + str(len(tasks)) + " currently in your list.")
                elif "add a task" in command:
                    listeningToTask = True
                    Speak("Sure, what is the task, sir?")
                elif "list tasks" in command:
                    Speak("Sure. Your tasks are:")
                    for task in tasks:
                        Speak(task)
                elif "take a screenshot" in command:
                    pyautogui.screenshot(f"screenshot{scrcr}.png")
                    Speak("I took a screenshot for you, sir..")
                    scrcr += 1
                    break
                elif "browser" in command:
                    Speak("Opening browser for you sir...")
                    webbrowser.open("http://www.google.com/")
                    break
                elif "search" in command:
                    Speak("Right Now Sir ... ")
                    self.show_summaries()
                    break# move to summaries frame
                elif "exit" in command:
                    Speak("Goodbye Sir! , Hope I could help you.")
                    break

                elif "login" in command:
                    Speak("Right now sir...")
                    self.show_login()
                    break

                elif "close" in command:
                    Speak("On it sir, I hope to see you soon.!")
                    self.close()
                    break

                else:
                    Speak("Sorry, I'm not sure how to handle that command.")




if __name__ == "__main__":
    app = AIProjectApp()

    window_width = 1000
    window_height = 700

    # Get the screen width and height
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    # Calculate the position to center the window
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    # Set the geometry to center the window
    app.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

    app.mainloop()