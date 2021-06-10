from flask import Blueprint, render_template, flash, redirect, url_for, request
import requests
from .models import City
from . import db

views = Blueprint('views', __name__)


@views.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        new_city = request.form.get('city')
        
        if new_city:
            new_city_obj = City(name=new_city)

            db.session.add(new_city_obj)
            db.session.commit()

    cities = City.query.all()

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid={ YOUR OPENWEATHER API KEY HERE }'
    
    weather_data = []

    for city in cities:
        r = requests.get(url.format(city.name)).json()
        weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }
        weather_data.append(weather)

    return render_template('weather.html', weather_data=weather_data)
