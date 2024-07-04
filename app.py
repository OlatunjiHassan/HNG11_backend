from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<h1>Hello, World!</h1>"

@app.route("/api")
def home_page():
    return "<h1>This is the home page</h1>"

@app.route("/api/hello")
def hello_page():
    return "<h1>This is the hello page</h1>"

@app.route("/api/hello/<visitor_name>", methods=['GET'])
def get_info(visitor_name):
    # client_ip = request.remote_addr
    client_ip = "102.89.33.219"
    url_ip_api = f"http://ip-api.com/json/{client_ip}?fields=status,message,country,regionName,city,lat,lon"
    # url_ip_api = f"http://ip-api.com/json/{client_ip}?fields=city,lat,lon"
    location_response = requests.get(url_ip_api)
    location_data = location_response.json()

    if location_data["status"] != "success":
        return jsonify({"error":"Could not retrive info on this IP"})

    lat = location_data['lat']
    lon = location_data['lon']

    city = location_data['city']

    weather_api_key = "g"
    url_weather_api = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={weather_api_key}"
    weather_response = requests.get(url_weather_api)
    weather_data = weather_response.json()

    if weather_response.status_code != 200:
        return jsonify({"error": "Could not retrieve weather data"}), 500

    degree = weather_data["main"]['temp']

    greeting = f"Hello {visitor_name}!, the temperature is {degree} degrees Celcius in {city}"
    return jsonify({
        "client_ip": client_ip,
        "location": city,
        "greeting": greeting
    })


if __name__ == "__main__":
    app.run(debug=True)
    # return jsonify({
    #     "ip" : client_ip,
    #     "location" : location_data,
    #     "temperature" : temp
    # })

# @app.route("/api/hello/<visitor_name>")
# def answer(visitor_name):
#     degree = 11
#     location = 'New York'
#     greeting = f"Hello {visitor_name}!, the temperature is {degree} degrees Celcius in {location}"
#     return {
#         "client_ip" : "127.0.0.1",
#         "location" : location,
#         "greeting" : greeting
#     }