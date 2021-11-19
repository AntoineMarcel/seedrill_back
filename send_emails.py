import requests
import os
print(os.getenv("ADMINTOKEN"))
r = requests.get("http://amarcel.pythonanywhere.com/send_email", headers={"Authorization" : os.getenv("ADMINTOKEN")})