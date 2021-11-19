import requests
import os

r = requests.get("http://amarcel.pythonanywhere.com/send_email", headers={"Authorization" : os.getenv("ADMINTOKEN")})