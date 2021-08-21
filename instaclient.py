from instagrapi import Client
from config import APP_CONFIG

# Instagram client 
cl = Client()
cl.login(APP_CONFIG['INSTA_LOGIN'], APP_CONFIG['INSTA_PASS'])