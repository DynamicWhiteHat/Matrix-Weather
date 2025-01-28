import requests
import board
import displayio
import framebufferio
import rgbmatrix
import time
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
import datetime

# Initialize the RGB matrix
matrix = rgbmatrix.RGBMatrix(
    width=64, height=32, bit_depth=1,
    rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
    addr_pins=[board.A5, board.A4, board.A3, board.A2],
    clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1)

display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

#setup for the display
g1 = displayio.Group()
display.root_group = g1
font = bitmap_font.load_font("cherry-10-b.bdf")
color = 0xFFFFFF

lat = x  # Latitude of the location
long = y  # Longitude of the location

base_url = "https://api.open-meteo.com/v1/forecast"


params = {
    "latitude": lat,
    "longitude": long,
    "current": ["temperature_2m", "relative_humidity_2m", "precipitation", "weather_code", "wind_speed_10m"],
	"temperature_unit": "fahrenheit",
	"wind_speed_unit": "mph",
	"precipitation_unit": "inch",
	"timezone": "America/New_York",
	"forecast_days": 1
    
}

# Declare global variables
temperature = None
wind_speed = None
weather_code = None

def get_weather_data():
    global temperature, wind_speed, weather_code  

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()

        print("Success")

        current = data.get('current', {})
        
        temperature = current.get('temperature_2m', 'N/A')
        wind_speed = current.get('wind_speed_10m', 'N/A')
        weather_code = current.get('weather_code', 'N/A')

        print("Current Weather Data:")
        print(f"Temperature: {temperature}°F")
        print(f"Wind Speed: {wind_speed} mph")
        print(f"Weather Code: {weather_code}")
    else:
        print("Error fetching weather data.")

# Initially get weather data
get_weather_data()

images = {
    0: "sunny.bmp",            # Clear sky
    1: "partlycloudy.bmp",     # Mainly clear
    2: "partlycloudy.bmp",     # Partly cloudy
    3: "partlycloudy.bmp",     # Overcast
    45: "partlycloudy.bmp",    # Fog
    48: "partlycloudy.bmp",    # Depositing rime fog
    51: "rainy.bmp",           # Light drizzle
    53: "rainy.bmp",           # Moderate drizzle
    55: "rainy.bmp",           # Dense drizzle
    56: "rainy.bmp",           # Light freezing drizzle
    57: "rainy.bmp",           # Dense freezing drizzle
    61: "rainy.bmp",           # Slight rain
    63: "rainy.bmp",           # Moderate rain
    65: "rainy.bmp",           # Heavy rain
    66: "rainy.bmp",           # Light freezing rain
    67: "rainy.bmp",           # Heavy freezing rain
    71: "snowy.bmp",           # Slight snowfall
    73: "snowy.bmp",           # Moderate snowfall
    75: "snowy.bmp",           # Heavy snowfall
    77: "snowy.bmp",           # Snow grains
    80: "rainy.bmp",           # Slight rain showers
    81: "rainy.bmp",           # Moderate rain showers
    82: "rainy.bmp",           # Violent rain showers
    85: "snowy.bmp",           # Slight snow showers
    86: "snowy.bmp"            # Heavy snow showers
}

bitmap = displayio.OnDiskBitmap(images.get(weather_code, "sunny.bmp"))  
image = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader, x=1, y=11)
g1.append(image)

# Create text labels
temp_area = label.Label(font, text="{} °F".format(temperature), color=color)
temp_area.x = 21
temp_area.y = 15
g1.append(temp_area)

wind_area = label.Label(font, text="{} mph".format(wind_speed), color=color)
wind_area.x = 21
wind_area.y = 25
g1.append(wind_area)

time_area = label.Label(font, text="{}".format(datetime.datetime.now().strftime("%H:%M:%S")), color=0xADD8E6)
time_area.x = 8
time_area.y = 4
g1.append(time_area)

seconds = 0

while True:
    seconds += 1
    if seconds == 30:
        get_weather_data()
        bitmap = displayio.OnDiskBitmap(images.get(weather_code, "sunny.bmp"))  
        image = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader, x=1, y=11)
        g1[0] = image  
        temp_area.text = "{} °F".format(temperature) 
        wind_area.text = "{} mph".format(wind_speed) 
        seconds = 0
    time_area.text = "{}".format(datetime.datetime.now().strftime("%H:%M:%S"))  # Update time
    display.refresh()
    time.sleep(1)
