import win32com.client as wincl
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import platform
from dotenv import load_dotenv
load_dotenv()

speaker = wincl.Dispatch("SAPI.SpVoice")
speaker.Rate = 3.4
# Functions for speaking
def speak(audio):
  speaker.Speak(audio)

# Function to wish the user based on the time of day
def wish_me():
  hour = int(datetime.datetime.now().hour)
  if hour>=0 and hour<12:
    speak("Good Morning!")
  elif hour>=12 and hour<18:
    speak("Good Afternoon!")
  else:
    speak("Good Evening!")

  speak("I am Hacker. Please tell me how may I help you")

# Function to take command from microphone and return string output
def take_command():
  r = sr.Recognizer()
  with sr.Microphone() as source:
    print("listening...")
    r.pause_threshold = 1
    audio = r.listen(source)
  try:
    print("Recognizing...")
    query = r.recognize_google(audio, language='en-in')
    print(f"User said: {query}\n")
  except Exception as e:
    print("Say that again please...")
    return "None"
  return query

# Function to send email
def sendEmail(to: str, subject: str, body: str):
    """
    Sends an email using Gmail's SMTP server with an App Password.

    Args:
        to (str): The recipient's email address.
        subject (str): The subject of the email.
        body (str): The plain text content of the email.
    """
    SENDER_PASSWORD = "your_app_password"  # Replace with your 8-character Google App Password
    if SENDER_PASSWORD == "your_app_password":
        print("ERROR: Please replace 'your_app_password' with a valid 16-character Google App Password.")
        return

    # 1. Create the email message object (MIMEMultipart is best practice)
    message = MIMEMultipart()
    message['From'] = "your_email@gmail.com"
    message['To'] = to
    message['Subject'] = subject
    
    # Attach the plain text body
    message.attach(MIMEText(body, 'plain'))

    print(f"Attempting to send email to: {to}...")

    try:
        # 2. Use 'with' statement for guaranteed server close (modern practice)
        # Port 587 with starttls is standard for secure SMTP
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            # server.ehlo() is redundant if using 'with' and starttls()
            server.starttls() 
            server.login("your_email@gmail.com", "your_app_password")
            
            # 3. Use message.as_string() to send the properly formatted MIME message
            server.sendmail("your_email@gmail.com", to, message.as_string())
            print("Email sent successfully!")

    except smtplib.SMTPAuthenticationError:
        print("Authentication Error: Login failed. Did you use a 8-character App Password?")
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to play a song on Spotify by name and singer using Spotify API
def play_spotify_song_by_name(song_name: str, singer_name: str):
    # --- 1. SPOTIFY API CREDENTIALS AND SCOPES ---
    # It is highly recommended to use environment variables for security
    CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID")
    CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET")
    CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID", "<CLIENT_ID>") # replace <CLIENT_ID> with your client ID
    CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET", "<CLIENT_SECRET>") # replace <CLIENT_SECRET> with your client ID
    REDIRECT_URI = "http://localhost:8080/callback" # Must match your Spotify App settings
    
    # Scopes needed for playback control
    SCOPE = "user-read-playback-state,user-modify-playback-state"

    if not (CLIENT_ID and CLIENT_SECRET):
        print("ERROR: Spotify API credentials are missing. Set SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET.")
        return

    print(f"\n--- Spotify Player Controller ---")
    
    try:
        # 2. Authorization Code Flow with Scopes
        auth_manager = SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope=SCOPE,
            open_browser=True # Opens the browser for login on first run
        )
        sp = spotipy.Spotify(auth_manager=auth_manager)
        
        # --- 3. SEARCH AND GET URI (Same as before) ---
        query = f'track:"{song_name}" artist:"{singer_name}"'
        results = sp.search(q=query, limit=1, type='track')
        
        items = results['tracks']['items']
        if not items:
            print(f"\nCould not find a track matching '{song_name}' by '{singer_name}'.")
            return

        track = items[0]
        spotify_uri = track['uri']
        track_name = track['name']
        artist_name = track['artists'][0]['name']

        print(f"\nFound Track: '{track_name}' by {artist_name}")

        # --- 4. CRITICAL CHANGE: START PLAYBACK VIA API ---
        # Get the ID of the current active device (Spotify app)
        devices = sp.devices()
        active_device_id = None
        
        if devices and devices['devices']:
            # Prioritize the active device, or just pick the first one
            for device in devices['devices']:
                if device['is_active']:
                    active_device_id = device['id']
                    break
            if not active_device_id:
                active_device_id = devices['devices'][0]['id']

        if active_device_id:
            # Force the player to start playing the new track immediately
            sp.start_playback(device_id=active_device_id, uris=[spotify_uri])
        else:
            print("WARNING: Could not find an active Spotify device. Please start the Spotify app.")
            # Fallback to the old method (non-guaranteed)
            webbrowser.open(spotify_uri)

    except Exception as e:
        print(f"\nAn error occurred during API or launch: {e}")
        print("Ensure you have correctly set up the Authorization Code Flow.")

# Main program loop
if __name__ == "__main__":
  wish_me()
  while True:
    query = take_command().lower()

  # Logic for executing tasks based on query
    if 'wikipedia' in query:
      speak('Searching Wikipedia...')
      query = query.replace("wikipedia", "")
      results = wikipedia.summary(query, sentences = 5)
      speak("According to Wikipedia")
      print(results)
      speak(results)
    
    elif "open youtube" in query:
      speak("opening youtube")
      webbrowser.open("youtube.com")
    
    elif "open google" in query:
      speak("opening google")
      webbrowser.open("google.com")
    
    elif "the time" in query:
      strTime = datetime.datetime.now().strftime("%H:%M:%S")
      speak(f"Sir, the time is {strTime}")
    
    elif "open code" in query:
      codePath = "C:\\Users\\Hp\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
      os.startfile(codePath)
    
    elif "open hianime" in query:
      webbrowser.open("https://hianimes.ro/")

    elif "open netflix" in query:
      webbrowser.open("https://www.netflix.com/in/")
    
    elif "open prime video" in query:
      webbrowser.open("https://www.primevideo.com/")

    elif "open github" in query:
      webbrowser.open("https://github.com/Dilpreet2004")

    elif "switch to gemini" in query:
      pass
    
    elif "switch to chatgpt" in query:
      pass
    
    elif "switch to deepseek" in query:
      pass
    
    elif "send message to given number on whatsapp" in query:
      pass
    
    elif "List available wifi networks" in query:
      pass

    elif "check internet speed" in query:
      pass

    elif "download youtube video" in query:
      pass
    
    elif "tell battery percentage" in query:
      pass

    elif "scan for vulnerabilities" in query:
      pass

    elif "perform penetration test" in query:
      pass

    elif "configure firewall settings" in query:
      pass

    elif "monitor network traffic" in query:
      pass

    elif "set up vpn connection" in query:
      pass

    elif "check for updates" in query:
      pass

    elif "install security patches" in query:
      pass

    elif "prepare SIEM reports" in query:
      pass

    elif "analyze security logs" in query:
      pass

    elif "tell me a joke" in query:
      pass

    elif "create a reminder" in query:
      pass

    elif "set an alarm" in query:
      pass

    elif "weather report" in query:
      pass

    elif "news update" in query:
      pass

    elif "perform brute force attack" in query:
      pass

    elif "perform sql injection" in query:
      pass

    elif "perform xss attack" in query:
      pass

    elif "perform ddos attack" in query:
      pass

    elif "perform mitm attack" in query:
      pass

    elif "perform phishing attack" in query:
      pass

    elif "hack wifi network" in query:
      pass

    elif "bypass firewall" in query:
      pass

    elif "email to me" in query:
      try:
        speak("What should I say?")
        content = take_command()
        to = "Paldilpreet4@gmail.com"
        sendEmail(to, content)
        speak("Email has been sent!")
      except Exception as e:
        print(e)
        speak("Sorry my friend. I am not able to send this email")
    
    elif "play song" in query or "play music" in query or "play spotify" in query or "play another song" in query:
      speak("Which song would you like to play?")
      song_name = take_command()
      speak("Who is the singer?")
      singer_name = take_command()
      play_spotify_song_by_name(song_name, singer_name)
    
    elif "shutdown system" in query:
      if platform.system() == "Windows":
        os.system("shutdown /s /t 5")
      elif platform.system() == "Linux":
        os.system("sudo shutdown -h +5")
        speak("Enter your password to proceed with shutdown.")
      speak("Shutting down the system in 5 seconds.")
    
    elif "restart system" in query:
      os.system("shutdown /r /t 5")
      print("Restarting the system in 5 seconds.")
    
    elif "quit" in query:
      speak("Exiting the program. Goodbye!")
      break
