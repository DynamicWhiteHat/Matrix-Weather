# Matrix Weather

### Created for HackClub Neon

### Demo: https://youtu.be/zDOZUC2TzLo

## How it works:
- Uses the Open Meteo API to get current weather data for a predefined location (in latitude/longitude)
    - This returns a weather code which corresponds to a certain weather pattern, eg sunny or rainy
- The weather code is then matched to a 20x20 bmp image of the pattern to visualize the weather
- The image, current time, temperature, and wind speed are all displayed on a 32.64 matrix controlled by an Adafruit library

No API key is required as Open Meteo provides free access to their services without a login

## Usage
a. Copy the code onto a microcontroller connected to a 32x64 display and run it
b. Visit neon.hackclub.dev/editor and paste the code into the editor to see it run on your machine
