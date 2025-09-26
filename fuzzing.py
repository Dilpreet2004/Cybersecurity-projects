import socket

# Setting up the target
host = input("enter the ip address: ")
port = input("enter the port: ")

# Setting up the wordlist for fuzzing
wordlist = "/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt"

# Set up the request to the endpoint
def fuzz_endpoint(wordlist_file):
  try:
    # Open the wordlist file
    with open(wordlist_file, 'r') as file:
      for line in file:
        # clean up the new lines and spaces
        command = line.strip()

        # Establish connection to the server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
          s.connect((host, port))
          # Send the fuzzing command
          s.sendall(command.encode() + b'\n')
          # Receive the response from the server
          response = s.recv(1024).decode().strip()

          if response != "" and "is not defined" not in response and "leading zeroes" not in response and "invalid" not in response:
            print(f"Command: {command} | Response: {response}")
  except FileNotFoundError:
    print("File not found. Please check the wordlist path.")
  except Exception as e:
    print(f"An error occurred: {e}")
  
# Run the fuzzing function with the wordlist
fuzz_endpoint(wordlist)