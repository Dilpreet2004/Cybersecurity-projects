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
import requests
import json
import time
from typing import Optional
import psutil
import pywifi
from pywifi import const
import time
load_dotenv()

speaker = wincl.Dispatch("SAPI.SpVoice")
speaker.Rate = 3.4

spotify_query = ["play song", "play music", "play spotify", "play another song","play some music","play a song","play the song"]
talk_query = ["tell","give","what","how","explain","define","describe","who","where","when","why"]
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
def get_spotify_client() -> Optional[spotipy.Spotify]:
    """Handles Spotify authorization and returns an authenticated Spotify client object."""
    CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID", "<CLIENT_ID>") # replace <CLIENT_ID> with your client ID
    CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET", "<CLIENT_SECRET>") # replace <CLIENT_SECRET> with your client ID
    REDIRECT_URI = "http://localhost:8080/callback" # Must match your Spotify App settings
    
    # Scopes needed for playback control and queueing
    SCOPE = "user-read-playback-state,user-modify-playback-state"

    if not (CLIENT_ID and CLIENT_SECRET and CLIENT_ID != "<CLIENT_ID>"):
        print("ERROR: Spotify API credentials are missing. Set SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET.")
        return None
    
    try:
        auth_manager = SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope=SCOPE,
            open_browser=True # Opens the browser for login on first run
        )
        sp = spotipy.Spotify(auth_manager=auth_manager)
        return sp
    except Exception as e:
        print(f"\nAn error occurred during Spotify client setup: {e}")
        print("Ensure you have correctly set up the Authorization Code Flow.")
        return None

# The original play_spotify_song_by_name function is kept unchanged
def play_spotify_song_by_name(song_name: str, singer_name: str):
    # ... (function body remains unchanged) ...
    CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID")
    CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET")
    CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID", "<CLIENT_ID>") # replace <CLIENT_ID> with your client ID
    CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET", "<CLIENT_SECRET>") # replace <CLIENT_SECRET> with your client ID
    REDIRECT_URI = "http://localhost:8080/callback" 
    SCOPE = "user-read-playback-state,user-modify-playback-state"

    if not (CLIENT_ID and CLIENT_SECRET):
        print("ERROR: Spotify API credentials are missing. Set SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET.")
        return

    print(f"\n--- Spotify Player Controller ---")
    
    try:
        auth_manager = SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope=SCOPE,
            open_browser=True
        )
        sp = spotipy.Spotify(auth_manager=auth_manager)
        
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

        devices = sp.devices()
        active_device_id = None
        
        if devices and devices['devices']:
            for device in devices['devices']:
                if device['is_active']:
                    active_device_id = device['id']
                    break
            if not active_device_id:
                active_device_id = devices['devices'][0]['id']

        if active_device_id:
            sp.start_playback(device_id=active_device_id, uris=[spotify_uri])
            print("Playback started successfully.")
        else:
            print("WARNING: Could not find an active Spotify device. Please start the Spotify app.")
            webbrowser.open(spotify_uri)

    except Exception as e:
        print(f"\nAn error occurred during API or launch: {e}")
        print("Ensure you have correctly set up the Authorization Code Flow.")

# =====================================================================
# 2. NEW SPOTIFY CONTROL FUNCTIONS (skip_to_next_song and queue_spotify_track_by_name remain unchanged)
# =====================================================================

def skip_to_next_song():
    """Skips the currently playing track to the next one in the queue/playlist."""
    sp = get_spotify_client()
    if not sp:
        return

    print("\n--- Skipping to Next Song ---")
    try:
        sp.next_track()
        print("Successfully skipped to the next song.")
    except spotipy.SpotifyException as e:
        if e.http_status == 404:
            print("Error: No active device found. Please start the Spotify app on a device.")
        else:
            print(f"An error occurred while skipping track: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def queue_spotify_track_by_name(song_name: str, singer_name: str):
    """Searches for a track and adds it to the Spotify playback queue."""
    sp = get_spotify_client()
    if not sp:
        return

    print(f"\n--- Queueing Track: {song_name} by {singer_name} ---")
    
    try:
        query = f'track:"{song_name}" artist:"{singer_name}"'
        results = sp.search(q=query, limit=1, type='track')
        
        items = results['tracks']['items']
        if not items:
            print(f"Could not find a track matching '{song_name}' by '{singer_name}'.")
            return

        track = items[0]
        spotify_uri = track['uri']
        track_name = track['name']
        artist_name = track['artists'][0]['name']

        # Queues the track on the active device
        sp.add_to_queue(uri=spotify_uri)
        print(f"Successfully added '{track_name}' by {artist_name} to the queue.")

    except spotipy.SpotifyException as e:
        if e.http_status == 404:
            print("Error: No active device found. Please start the Spotify app on a device.")
        else:
            print(f"An error occurred while queueing track: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def queue_spotify_album_by_name(album_name: str, singer_name: str):
    """
    Searches for an album and queues ALL of its tracks one by one.
    This simulates queueing the whole album using multiple API calls.
    """
    sp = get_spotify_client()
    if not sp:
        return

    print(f"\n--- Attempting to Queue ALL Tracks of Album: {album_name} by {singer_name} ---")

    try:
        query = f'album:"{album_name}" artist:"{singer_name}"'
        results = sp.search(q=query, limit=1, type='album')
        
        items = results['albums']['items']
        if not items:
            print(f"Could not find an album matching '{album_name}' by '{singer_name}'.")
            return

        album = items[0]
        album_id = album['id']
        album_name_found = album['name']
        artist_name = album['artists'][0]['name']
        
        print(f"Found Album: '{album_name_found}' by {artist_name}")

        queued_count = 0
        
        # Paginate through the album's tracks (albums can have > 50 tracks)
        tracks_results = sp.album_tracks(album_id)
        tracks_to_queue = tracks_results['items']
        
        # The API response structure for album_tracks is different from search
        while tracks_to_queue:
            for track in tracks_to_queue:
                track_uri = track['uri']
                # Queue the individual track
                sp.add_to_queue(uri=track_uri)
                queued_count += 1
            
            # Fetch the next page of results if available
            if tracks_results['next']:
                tracks_results = sp.next(tracks_results)
                tracks_to_queue = tracks_results['items']
            else:
                tracks_to_queue = None

        if queued_count > 0:
            print(f"SUCCESS: Successfully queued {queued_count} tracks from the album '{album_name_found}'.")
        else:
             print(f"WARNING: Found album '{album_name_found}' but it contained no tracks to queue.")


    except spotipy.SpotifyException as e:
        if e.http_status == 404:
            print("Error: No active device found. Please start the Spotify app on a device.")
        else:
            print(f"An error occurred while queueing tracks: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# =====================================================================
# 3. MAIN EXECUTION LOOP (Modified menu text for clarity)
# =====================================================================

def get_input_details(prompt_message: str) -> Optional[tuple[str, str]]:
    """Helper to get and parse song/artist or album/artist input."""
    item = input(prompt_message)
    details = item.split(" by ")
    if len(details) != 2:
        print("Please enter in the format: <name> by <artist name>")
        return None
    name = details[0].strip()
    artist = details[1].strip()
    return name, artist
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

def generate_content_with_retry(prompt: str, retries: int = 0):
    """
    Calls the Gemini API with Google Search grounding and exponential backoff.

    Args:
        prompt: The user's text prompt.
        retries: The current retry attempt number.

    Returns:
        The parsed JSON response from the API.
    
    Raises:
        Exception: If the request fails after all retry attempts.
    """
    API_KEY = os.getenv("GEMINI_API_KEY")
    API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent"
    MAX_RETRIES = 3
    # 1. Define the system instructions and payload structure
    system_prompt = "You are a friendly, helpful, and creative assistant. Answer the user's query in a conversational and easy-to-understand manner."
    
    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ],
        # Enable Google Search grounding for real-time information
        "tools": [{"google_search": {}}],
        "systemInstruction": {
            "parts": [{"text": system_prompt}]
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    # 2. Add API key to the request parameters
    params = {
        "key": API_KEY
    }

    try:
        print(f"\n--- Sending request (Attempt {retries + 1}/{MAX_RETRIES}) ---")
        
        # 3. Make the API call
        response = requests.post(API_URL, headers=headers, params=params, data=json.dumps(payload))
        response.raise_for_status() # Raises an exception for bad status codes (4xx or 5xx)
        
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error during API call: {e}")
        
        if retries < MAX_RETRIES - 1:
            delay = 2 ** retries  # 1s, 2s, 4s
            print(f"Retrying in {delay} seconds...")
            time.sleep(delay)
            return generate_content_with_retry(prompt, retries + 1)
        else:
            raise Exception("Failed to connect to the AI service after multiple retries.")


def display_response(response_json):
    """
    Parses the generated text and sources and returns them as a single formatted string.
    """
    result_output = ""
    separator = "=" * 50
    
    candidate = response_json.get('candidates', [{}])[0]
    
    if not candidate:
        return "\n[ERROR] No candidate response received from the API."

    # Extract Text
    text = candidate.get('content', {}).get('parts', [{}])[0].get('text', '')

    if text:
        result_output += text
        result_output += "\n" # Ensure text ends with a newline
    else:
        result_output += "\n[INFO] Generated text was empty."
        return result_output

    # Extract Sources/Citations (Grounding Metadata)
    grounding_metadata = candidate.get('groundingMetadata', {})
    attributions = grounding_metadata.get('groundingAttributions', [])
    
    if attributions:
        sources = []
        for attr in attributions:
            web_info = attr.get('web', {})
            uri = web_info.get('uri')
            title = web_info.get('title')
            if uri and title:
                sources.append((title, uri))
        
        if sources:
            # Filter for unique URIs
            unique_sources = {}
            for title, uri in sources:
                unique_sources[uri] = title

            source_separator = "-" * 50
            result_output += f"\n{source_separator}\n"
            result_output += "Sources/Citations:\n"
            result_output += f"{source_separator}\n"
            
            for i, (uri, title) in enumerate(unique_sources.items(), 1):
                result_output += f"  {i}. {title} \n     URL: {uri}\n"
    
    return result_output

# --- Helper function for Spotify voice input ---
def get_spotify_details_from_voice():
    """Prompts the user to speak the song/album name and artist and parses it."""
    speak("Please tell me the name of the track or album along with the artist.")
    speak("Say 'song name by artist name'.")
    
    # Give the user a moment to prepare
    time.sleep(1) 
    
    details_query = take_command().lower()
    print(f"Details said: {details_query}")

    if "by" in details_query:
        parts = details_query.split("by")
        if len(parts) >= 2:
            name = parts[0].strip()
            artist = parts[1].strip()
            return name, artist
    
    speak("Sorry, I could not clearly understand the song and artist name. Please try again.")
    return None, None

# --- Helper function for routing specific Spotify commands ---
def spotify_command_router(query: str):
    """Routes the Spotify command to the correct function based on the query."""

    if 'skip' in query or 'next song' in query or 'next track' in query:
        skip_to_next_song()
    
    elif 'queue album' in query or 'add album' in query:
        speak("Which album would you like to queue?")
        print("Which album would you like to queue?")
        album_name, artist_name = get_spotify_details_from_voice()
        if album_name and artist_name:
            queue_spotify_album_by_name(album_name, artist_name)
    
    elif 'queue song' in query or 'queue track' in query or 'add song' in query:
        speak("Which song would you like to queue?")
        print("Which song would you like to queue?")
        song_name, singer_name = get_spotify_details_from_voice()
        if song_name and singer_name:
            queue_spotify_track_by_name(song_name, singer_name)
    
    elif any(q in query for q in spotify_query):
        # Default action: Play a song immediately
        speak("What would you like to play?")
        print("What would you like to play?")
        song_name, singer_name = get_spotify_details_from_voice()
        if song_name and singer_name:
          play_spotify_song_by_name(song_name, singer_name)
    
    else:
        speak("I heard a Spotify command, but I didn't recognize the specific action like play, skip, or queue.")
        print("I heard a Spotify command, but I didn't recognize the specific action like play, skip, or queue.")

def get_security_name(network):
    """
    Determines the human-readable security name for a network profile
    by mapping stable pywifi integer constants (AKM and Cipher types).
    """
    # Define standard mappings using integer constant values
    AKM_MAP = {
        const.AKM_TYPE_NONE: "Open",
        const.AKM_TYPE_WPA: "WPA",
        const.AKM_TYPE_WPAPSK: "WPA-PSK",
        const.AKM_TYPE_WPA2: "WPA2",
        const.AKM_TYPE_WPA2PSK: "WPA2-PSK",
        # Adding WPA3 for completeness, though may not be in older pywifi versions
        getattr(const, 'AKM_TYPE_WPA3PSK', 0x00000008): "WPA3-PSK", 
        getattr(const, 'AKM_TYPE_WPA3', 0x00000004): "WPA3",
    }
    
    CIPHER_MAP = {
        const.CIPHER_TYPE_NONE: "None",
        const.CIPHER_TYPE_WEP: "WEP",
        const.CIPHER_TYPE_TKIP: "TKIP",
        const.CIPHER_TYPE_CCMP: "CCMP/AES", 
    }

    # 1. Handle Open/WEP (Cipher-based security)
    if not network.akm or const.AKM_TYPE_NONE in network.akm:
        if network.cipher == const.CIPHER_TYPE_WEP:
            return "WEP"
        return "Open"

    # 2. Handle WPA/WPA2/WPA3 (AKM-based security)
    akm_protocols = []
    for akm_int in network.akm:
        akm_protocols.append(AKM_MAP.get(akm_int, f"Unknown AKM:{akm_int}"))
        
    # Join protocols (e.g., WPA/WPA2-PSK)
    akm_str = "/".join(sorted(set(p.replace('-PSK', '') for p in akm_protocols if 'PSK' in p) or akm_protocols))
    
    # Extract Cipher (Encryption) type
    cipher_str = CIPHER_MAP.get(network.cipher, f"Unknown Cipher:{network.cipher}")
    
    # Standard secured network format: Protocol/Cipher (e.g., WPA2-PSK/CCMP/AES)
    return f"{akm_str}/{cipher_str}"


def scan_wifi_networks():
    """
    Scans for and lists available Wi-Fi networks using the pywifi library.
    """
    try:
        # 1. Initialize the Wi-Fi interface object
        wifi = pywifi.PyWiFi()
        
        # Get the first Wi-Fi interface (usually wlan0 or similar)
        ifaces = wifi.interfaces()
        if not ifaces:
            speak("No Wi-Fi interface found. Please ensure Wi-Fi is enabled.")
            return

        iface = ifaces[0]
        
        # 2. Start the network scan
        speak("Starting Wi-Fi scan...")
        iface.scan()
        
        # 3. Wait for the scan to complete (can take a few seconds)
        time.sleep(4) 
        
        # 4. Retrieve the scan results
        results = iface.scan_results()
        
        if not results:
            speak("No networks found.")
            return

        # 5. Process and display the results
        speak("Here are the results:")
        print("\n" + "="*70)
        print(f"{'Available Wi-Fi Networks':^70}")
        print("="*70)
        
        # Use a set to store unique SSIDs to avoid duplicate listings from multiple BSSIDs/APs
        unique_ssids = set()
        
        # Sort by signal strength (RSSI) in descending order
        sorted_results = sorted(results, key=lambda x: x.signal, reverse=True)

        for network in sorted_results:
            ssid = network.ssid
            
            # Filter out hidden or already listed networks
            if ssid and ssid not in unique_ssids:
                
                signal_strength = network.signal # Signal is in dBm (negative values)
                
                # Determine the security type using the robust helper function
                security = get_security_name(network)
                

                print(f"SSID: {ssid:<35} | Signal: {signal_strength: >4} dBm | Security: {security}")
                unique_ssids.add(ssid)

        print("="*70)

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("This might be due to missing libraries or insufficient permissions.")
        print("Please ensure you have installed 'pywifi' and run the script with administrator/root privileges if necessary.")

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
    
    elif "the date" in query:
      strDate = datetime.datetime.now().strftime("%d:%m:%Y")
      speak(f"Sir, the current date is {strDate}")

    elif "the day" in query:
      strDay = datetime.datetime.now().strftime("%A")
      speak(f"Sir, today is {strDay}")
    
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

    elif any(talk in query for talk in talk_query):
      try:
        response_json = generate_content_with_retry(query)
        result = display_response(response_json)
        print(result)
        speak(result)
        
      except Exception as e:
        print(f"\n[FATAL ERROR] Operation failed: {e}")
        speak("Sorry, I am unable to process your request at the moment.")
    
    elif "send message to given number on whatsapp" in query:
      pass
    
    elif "List available wifi networks" in query:
      scan_wifi_networks()

    elif "check internet speed" in query:
      pass

    elif "download youtube video" in query:
      pass
    
    elif "tell battery percentage" in query:
      battery = psutil.sensors_battery()
      if battery:
        speak(f"Battery percentage is {battery.percent} percent")
      else:
        speak("Battery information not available.")

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
    
    elif any(q in query for q in spotify_query) or 'skip' in query or 'queue' in query or 'next song' in query or 'add' in query:
      spotify_command_router(query)

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
    
    elif "quit" in query or "exit" in query:
      speak("Exiting the program. Goodbye!")
      exit(0)