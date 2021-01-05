from flask import *
from configparser import ConfigParser
from tkinter import messagebox
import requests

api_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

app = Flask(__name__)

config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']

def get_weather(city):
    result = requests.get(api_url.format(city, api_key))
    if result:
        json = result.json()
        city = json['name']
        country = json['sys']['country']
        temp_kelvin = json['main']['temp']
        temp_celsius = round(temp_kelvin - 273.15, 2)
        temp_ferenheit = round(temp_celsius*9/5+32, 2)
        icon = "icons/"+(json['weather'][0]['icon'])+".png"
        weather = json['weather'][0]['main']
        final = (city, country, temp_celsius, temp_ferenheit, icon, weather)
        return final
    else:
        return None

@app.route('/', methods=["POST", "GET"])
def Weather_app():
    if request.method == "POST":
        city_name = request.form["city"]
        return redirect(url_for("city_weather", city=city_name))
    else:
        return render_template('index.html')


@app.route('/<city>')
def city_weather(city):
    city_info = get_weather(city)
    if city_info:
        return render_template('weatherOfCity.html', city_data = city_info)
    else:
        messagebox.showerror('[ERROR]',"Cannot Find City {}".format(city))


if __name__ == '__main__':
    app.run()
