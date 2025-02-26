Project Overview:
The AI Assistant is a voice-controlled application that can execute various tasks, including:
- Taking screenshots.
- Opening a web browser.
- Searching and adding tasks to a task list.
- Displaying and speaking the user's task list.
- Handling user login and sign-up processes through a database.

Technologies Used:
- Python 3.x
- tkinter (CustomTkinter)
- pyautogui (for taking screenshots)
- speech_recognition (for recognizing voice commands)
- pyttsx3 (for text-to-speech functionality)
- requests (for making HTTP requests)
- sqlite3 (for handling database connections)
- requests_oauthlib (for OAuth2 support)

Key Features:
1. **Voice Recognition**: The assistant listens for user commands and responds accordingly using speech recognition.
2. **Task Management**: Users can add tasks, list tasks, and interact with their task list.
3. **Database Management**: Supports user login and sign-up, storing user data securely in a local SQLite database.
4. **Voice Feedback**: Provides voice responses to the user for actions such as confirming tasks or executing commands.
5. **Web Interaction**: Can open a browser and perform searches through recognized commands.
6. **Screenshot Functionality**: Takes screenshots of the current screen when triggered by the user.

Project Structure:
- **Database**: The project uses a local SQLite database (`Users.db`) for storing user data (login credentials, task lists, etc.).
- **Voice Command Handling**: The `listen()` function listens for voice commands and executes corresponding actions, such as adding tasks or opening the browser.
- **GUI**: The application uses the `CustomTkinter` library for the user interface, with multiple frames for login, signup, and task interaction.

Classes and Functions:
1. **DB_login(username, password)**: Authenticates a user against the database.
2. **DB_sign_up(...)**: Registers a new user in the database.
3. **listen()**: Listens to and recognizes user commands.
4. **Speak(txt)**: Converts text to speech.
5. **body()**: Main function for continuously listening for commands and executing the relevant tasks.
6. **AIProjectApp**: The main application class that manages the GUI and various frames (login, signup, tasks, etc.).

Usage:
1. Run the script to launch the AI Assistant application.
2. Login using your credentials or sign up as a new user.
3. Use voice commands to interact with the assistant:
   - "add a task" to add a new task to the list.
   - "list tasks" to view your current tasks.
   - "take a screenshot" to capture your screen.
   - "open browser" to open a web browser.
   - "exit" to exit the application.

Requirements:
- Python 3.x
- Libraries:
  - customtkinter
  - pyautogui
  - speech_recognition
  - pyttsx3
  - sqlite3
  - requests
  - requests_oauthlib
- Install dependencies via `pip`:
  pip install customtkinter pyautogui speech_recognition pyttsx3 requests requests_oauthlib

License:
This project is open-source. but cite me Youssef Kotb, Youssef Amaar.
https://github.com/Youssef-kotb/Jarvis_

