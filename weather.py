#!/bin/python3

from flask import Flask, render_template, request # request for Flask endpoints, not HTTP
# from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests # to interact with API (HTTP)
import json
import folium

app = Flask(__name__) # telling Flask that all files are in curr dir
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqllite:///weather.db"
# db = SQLAlchemy(app)

# # create db model
# class Weather(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     date = db.Column(db.Datetime)

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
        
        m = folium.Map(
            location=[data["coord"]["lat"], data["coord"]["lon"]],
            tiles='OpenStreetMap',
            control_scale=True
        )
        
        folium.Marker(location=[data["coord"]["lat"], data["coord"]["lon"]]).add_to(m)
      
    
        m.save("static/map.html")
        
        
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


# app.route("/history", methods = ["POST"])
# def history():
    
#     lat = request.form.get("lat") 
#     lon = request.form.get("lon") 
    
#     start_str = request.form.get("start")
#     end_str = request.form.get("end")
    
    
#     # Validate that a date was provided
#     if not (start_str and end_str):
#         return "Please provide a valid date", 400
#     try:
#         start_dt = datetime.strptime(start_str, "%Y-%m-%d")
#         end_dt = datetime.strptime(end_str, "%Y-%m-%d")
        
#         unix_start = int(start_dt.timestamp())
#         unix_end = int(end_dt.timestamp())
        
#         url = f"https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&type=hour&start={unix_start}&end={unix_end}&appid={api_key}&units=imperial"
        
#         response = requests.get(url)
    
#         if response.status_code != 200:
#             return f"Invalid location or date: {response.status_code}"
#         else:
#             specific_data = {
#             "location" : data["name"],
#             "icon" : data["weather"][0]["icon"],
#             "temp" : data["main"]["temp"],
#             "main" : data["weather"][0]["main"],
#             "description" : data["weather"][0]["description"],
            
#             "min" : data["main"]["temp_min"],
#             "max" : data["main"]["temp_max"],
#             "humidity" : data["main"]["humidity"],
#             "w_speed": f"{data['wind']['speed']} mph",
#             # "forecast" : forecast
#         }
        
        
#         # return f"Unix Time: {unix_time}"
#     except ValueError:
#         return "Invalid date format", 400
    
app.run(host = "0.0.0.0", port = 5000)