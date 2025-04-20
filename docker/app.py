from flask import Flask, jsonify, request
import requests
import os
from datetime import datetime

app = Flask(__name__)


API_KEY = os.getenv('OPENWEATHER_API_KEY', '3315566e18ae92e23bbda690b1776827')
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

@app.route('/weather', methods=['GET'])
def get_weather():
    try:
        city = request.args.get('city')
        
        if not city:
            return jsonify({
                'status': 'error',
                'message': 'City parameter is required',
                'example': '/weather?city=Moscow'
            }), 400

        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric',
            'lang': 'ru'
        }

        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()  
        
        data = response.json()

        weather_info = {
            'status': 'success',
            'location': {
                'city': data.get('name'),
                'country': data.get('sys', {}).get('country'),
                'coordinates': {
                    'lat': data['coord']['lat'],
                    'lon': data['coord']['lon']
                }
            },
            'weather': {
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'condition': data['weather'][0]['main'],
                'description': data['weather'][0]['description'],
                'icon': f"https://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
            },
            'wind': {
                'speed': data['wind']['speed'],
                'direction': data['wind'].get('deg', 'N/A')
            },
            'timestamp': datetime.utcnow().isoformat()
        }

        return jsonify(weather_info)

    except requests.exceptions.RequestException as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to fetch weather data',
            'details': str(e)
        }), 500
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Internal server error',
            'details': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)  
