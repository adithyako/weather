#!/bin/python3

from flask import Flask, render_template, request # request for Flask endpoints, not HTTP
import requests # to interact with API (HTTP)
import json

app = Flask(__name__) # telling Flask that all files are in curr dir

api_key = "b2c6d667e225edcf1b924ec3ddf80d75"
# def get_meme():
#     url = "https://meme-api.com/gimme"
#     response = requests.get(url).json()
#     meme_large = response["preview"][-2]
#     subreddit = response["subreddit"]
#     return meme_large, subreddit

@app.route('/', methods = ["GET"])
def index():
    return render_template("weather.html")

@app.route("/search", methods = ["POST"])
def search():
    user_lat = request.form.get("user_lat")
    user_lon = request.form.get("user_lon")
    
    api_url = f"https://api.openweathermap.org/data/2.5/weather?lat={user_lat}&lon={user_lon}&appid={api_key}"
    
    response = requests.get(api_url)
    data = response.json()
    
    
    
    
    





app.run(host = "0.0.0.0", port = 6000)