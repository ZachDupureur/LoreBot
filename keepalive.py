# For hosting on replit.com only. Starts a webserver on the homepage.
# User will need to set up uptimebot.com to ping https address every 30 - 60 min

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def main():
  return "Your bot is alive!!"

def run():
  app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()
