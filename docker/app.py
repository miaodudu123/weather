from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

API_KEY = '3315566e18ae92e23bbda690b1776827'   
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    
    if not city:
        return jsonify({'error': 'City is required'}), 400
    
    url = f'{BASE_URL}?q={city}&appid={API_KEY}&units=metric&lang=ru'
    
    response = requests.get(url)
    
    if response.status_code != 200:
        return jsonify({'error': 'Could not retrieve weather data'}), 500
    
    data = response.json()
    
    if data.get('cod') != 200:
        return jsonify({'error': data.get('message', 'Unknown error')}), 400
    
    weather_info = {
        'city': data['name'],
        'temperature': data['main']['temp'],
        'description': data['weather'][0]['description'],
        'humidity': data['main']['humidity'],
        'wind_speed': data['wind']['speed'],
    }
    
    return jsonify(weather_info)

if __name__ == '__main__':
    app.run(debug=True)
