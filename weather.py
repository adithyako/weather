#!/bin/python3

from flask import Flask, render_template, request # request for Flask endpoints, not HTTP
import requests # to interact with API (HTTP)
import json

app = Flask(__name__) # telling Flask that all files are in curr dir

api_key = "b2c6d667e225edcf1b924ec3ddf80d75"
api_url = ""
five_day_url = ""

@app.route('/', methods = ["GET"])
def index():
    return render_template("weather.html")

@app.route("/search", methods = ["POST"])
def search():
    user_lat = request.form.get("user_lat") 
    user_lon = request.form.get("user_lon") 
    city_name = request.form.get("city_name") 
    state = request.form.get("state") 
    zip_code = request.form.get("zip_code")
    country_code = request.form.get("country_code")
    type = "weather?"
    
    
    if user_lat and user_lon:
        api_url = f"https://api.openweathermap.org/data/2.5/{type}lat={user_lat}&lon={user_lon}&appid={api_key}&units=imperial"
    elif city_name:
        if country_code:
            api_url = f"https://api.openweathermap.org/data/2.5/{type}q={city_name},{country_code}&appid={api_key}&units=imperial"
        else:
            if state:
                api_url = f"https://api.openweathermap.org/data/2.5/{type}q={city_name},{state},USA&appid={api_key}&units=imperial"
            else:
                api_url = f"https://api.openweathermap.org/data/2.5/{type}q={city_name},&appid={api_key}&units=imperial"
    elif zip_code:
        if country_code:
            api_url = f"https://api.openweathermap.org/data/2.5/{type}zip={zip_code},{country_code}&appid={api_key}&units=imperial"
        else:
            api_url = f"https://api.openweathermap.org/data/2.5/{type}zip={zip_code}&appid={api_key}&units=imperial"
    else:
        return "Provide GPS coordinates, a city name, or a zip code.", 400


    

    response = requests.get(api_url)
    
    if response.status_code == 200:
        
        
        data = response.json() # Current forecast
        
        # type = "forecast?"
        # response2 = requests.get(api_url) # Five-day forecast
        # data2 = response2.json()
        # print(json.dumps(data2, indent=2))

        
        # count = 1
        
        # forecast = f""
        
        # for i in data2["list"]:
        #     date = i["dt_txt"]
        #     temp = i["main"]["temp"]
        #     icon = i["weather"][0]["icon"]
            
        #     forecast += f"Day: {date}<br>{icon}<br>{temp}°<br>"
            
        #     count += 1
            
        
        specific_data = {
            "location" : data["name"],
            "icon" : data["weather"][0]["icon"],
            "temp" : data["main"]["temp"],
            "main" : data["weather"][0]["main"],
            "description" : data["weather"][0]["description"],
            
            "min" : data["main"]["temp_min"],
            "max" : data["main"]["temp_max"],
            "humidity" : data["main"]["humidity"],
            "w_speed": f"{data['wind']['speed']} mph",
            # "forecast" : forecast
        }
        
        return render_template("results.html", **specific_data)
        
        
        
    else:
        return f"Location not found: {response.status_code}"
    
app.run(host = "0.0.0.0", port = 5000)