from flask import Flask, render_template, request
import json
import urllib.request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def weather():
    if request.method == 'POST':
        city = request.form.get("city")
    else:
        city = 'Nairobi'  # Default city

    api = 'e5518d681c054b7c949150042252407'

    try:
        url = f'https://api.weatherapi.com/v1/current.json?key={api}&q={city}'
        source = urllib.request.urlopen(url).read()
        weather_data = json.loads(source)

        data = {
            "City": weather_data['location']['name'],
            "Country": weather_data['location']['country'],
            "Region": weather_data['location']['region'],
            "Coordinates": f"{weather_data['location']['lat']}, {weather_data['location']['lon']}",
            "Temperature": str(weather_data['current']['temp_c']) + " °C",
            "Pressure": str(weather_data['current']['pressure_mb']) + " hPa",
            "Humidity": str(weather_data['current']['humidity']) + "%",
            "Condition": weather_data['current']['condition']['text'],
            "Wind": f"{weather_data['current']['wind_kph']} kph {weather_data['current']['wind_dir']}"
        }

    except Exception as e:
        data = {"Error": "Could not fetch weather data. Please check the city name or API key."}
        print("Error:", e)

    return render_template("index.html", data=data)

if __name__ == '__main__':
    app.run(debug=True)
