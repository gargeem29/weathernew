import requests
import time
import datetime
import sqlite3
from flask import Flask, jsonify
from flask_cors import CORS
from threading import Thread

# Constants
API_KEY = '14f822bfb6925ccb893161e06145ac98'  # Replace with your OpenWeatherMap API key
CITIES = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]
CHECK_INTERVAL = 300  # Set interval to 5 minutes
DB_NAME = 'weather_data.db'

# Flask app
app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return "Welcome to the Weather Data API! Access /api/weather_summary for weather summaries."

@app.route('/api/weather_summary', methods=['GET'])
def weather_summary():
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute('''SELECT DISTINCT city, date, avg_temp, max_temp, min_temp, dominant_weather
                       FROM DailyWeatherSummary
                       WHERE date = ?''', (datetime.date.today().strftime('%Y-%m-%d'),))
        
        rows = cur.fetchall()
        weather_data = []
        for row in rows:
            weather_data.append({
                "city": row[0],
                "date": row[1],
                "avg_temp": row[2],
                "max_temp": row[3],
                "min_temp": row[4],
                "dominant_weather": row[5]
            })
        
        return jsonify(weather_data)

# Initialize the database with a table if it doesn't exist
def initialize_database():
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS DailyWeatherSummary (
                           city TEXT,
                           date TEXT,
                           avg_temp REAL,
                           max_temp REAL,
                           min_temp REAL,
                           dominant_weather TEXT
                       )''')
        # Table for storing alert thresholds for each city
        cur.execute('''CREATE TABLE IF NOT EXISTS AlertThresholds (
                           city TEXT UNIQUE,
                           temp_threshold REAL,
                           consecutive_updates INTEGER
                       )''')
        conn.commit()

# Function to fetch weather data with error handling
def fetch_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
    response = requests.get(url)
    data = response.json()
    
    if 'weather' in data and 'main' in data:
        temp = data['main']['temp'] - 273.15  # Kelvin to Celsius
        return {
            "city": city,
            "main": data['weather'][0]['main'],
            "temp": temp,
            "dt": data['dt']
        }
    else:
        print(f"Error fetching data for {city}: {data}")
        return None

# Function to set default alert thresholds for temperature
def set_default_thresholds():
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        for city in CITIES:
            cur.execute('''INSERT OR IGNORE INTO AlertThresholds (city, temp_threshold, consecutive_updates)
                           VALUES (?, ?, ?)''', (city,30, 2))  # Default: alert at 35°C after 2 consecutive readings
        conn.commit()

# Check and trigger alert if temperature exceeds threshold
def check_thresholds(city, current_temp):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute('SELECT temp_threshold, consecutive_updates FROM AlertThresholds WHERE city = ?', (city,))
        result = cur.fetchone()
        
        if result:
            temp_threshold, required_consecutive_updates = result
            if current_temp >= temp_threshold:
                cur.execute('''SELECT COUNT(*) FROM DailyWeatherSummary
                               WHERE city = ? AND date = ? AND max_temp >= ?''',
                               (city, datetime.date.today().strftime('%Y-%m-%d'), temp_threshold))
                
                consecutive_count = cur.fetchone()[0]
                if consecutive_count + 1 >= required_consecutive_updates:
                    trigger_alert(city, current_temp, temp_threshold, consecutive_count + 1)

# Trigger an alert
def trigger_alert(city, current_temp, threshold, consecutive_count):
    print(f"ALERT: {city} temperature has exceeded {threshold}°C for {consecutive_count} consecutive updates. Current temperature: {current_temp}°C.")

# Function to insert or update weather data into the database
def insert_weather_data(city, temp, weather_main):
    today_date = datetime.date.today().strftime('%Y-%m-%d')
    
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()

        # Check if data for today already exists
        cur.execute('''SELECT avg_temp, max_temp, min_temp, dominant_weather FROM DailyWeatherSummary 
                       WHERE city = ? AND date = ?''', (city, today_date))
        result = cur.fetchone()
        
        if result:
            # Update existing record
            existing_avg_temp, existing_max_temp, existing_min_temp, existing_dominant_weather, count = result
            new_avg_temp = (existing_avg_temp * count + temp) / (count + 1)  # Calculate new average
            new_max_temp = max(existing_max_temp, temp)
            new_min_temp = min(existing_min_temp, temp)
            count += 1
            
            cur.execute('''UPDATE DailyWeatherSummary SET avg_temp = ?, max_temp = ?, min_temp = ?, 
                           dominant_weather = ?, count = ? WHERE city = ? AND date = ?''',
                           (new_avg_temp, new_max_temp, new_min_temp, weather_main, count, city, today_date))
        else:
            # Insert new record
            avg_temp = temp  # For a new record, avg = temp
            max_temp = temp
            min_temp = temp
            dominant_weather = weather_main
            
            cur.execute('''INSERT INTO DailyWeatherSummary (city, date, avg_temp, max_temp, min_temp, dominant_weather, count) 
                           VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                           (city, today_date, avg_temp, max_temp, min_temp, dominant_weather, 1))
        
        conn.commit()

# Modify fetch_and_process_data to include database insertion
def fetch_and_process_data():
    while True:
        for city in CITIES:
            weather = fetch_weather_data(city)
            if weather:
                insert_weather_data(weather["city"], weather["temp"], weather["main"])
                check_thresholds(city, weather["temp"])
                print(f"Fetched weather for {city}: {weather}")
        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    # Initialize the database and set default thresholds
    initialize_database()
    set_default_thresholds()
    
    # Run Flask API in parallel with data processing
    Thread(target=fetch_and_process_data).start()
    app.run(port=5000)
