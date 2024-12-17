import time
from pyowm import OWM
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd2in13_V4
from pyowm.utils.config import get_default_config
import os
from datetime import datetime, timedelta

# ---------- WEATHER CONFIGURATION ---------------------

# Set the language to English for weather descriptions
config_dict = get_default_config()
config_dict['language'] = 'en'

# API key for OpenWeatherMap (replace with your valid API key)
owm = OWM("<YOUR_API_KEY>", config_dict)
mgr = owm.weather_manager()

# Get current weather for Messina, Italy
observation = mgr.weather_at_place('Messina,IT')
current_weather = observation.weather

# Extract current weather details
detailed_status = current_weather.detailed_status
wind = current_weather.wind()
humidity = current_weather.humidity
temperature = current_weather.temperature('celsius')['temp']
current_icon_code = current_weather.weather_icon_name  # Example: '10d'

# Get the weather forecast for Messina, Italy
forecast = mgr.forecast_at_place('Messina,IT', '3h').forecast.weathers

# Calculate tomorrow's date
today = datetime.now()
tomorrow_date = (today + timedelta(days=1)).date()

# Filter forecasts for the entire next day
tomorrow_forecasts = [w for w in forecast if w.reference_time('date').date() == tomorrow_date]

# Extract minimum and maximum temperatures for the next day
tomorrow_temperature_min = min(w.temperature('celsius')['temp_min'] for w in tomorrow_forecasts)
tomorrow_temperature_max = max(w.temperature('celsius')['temp_max'] for w in tomorrow_forecasts)

# Determine the prevailing weather status for the next day
tomorrow_status_list = [w.detailed_status for w in tomorrow_forecasts]
tomorrow_status = max(set(tomorrow_status_list), key=tomorrow_status_list.count)

# Use the first forecast icon of the next day as representative
tomorrow_icon_code = tomorrow_forecasts[0].weather_icon_name
tomorrow_icon_path = f"./iconebmp/{tomorrow_icon_code}.bmp"

# Paths for current weather icons
current_icon_path = f"./iconebmp/{current_icon_code}.bmp"

# ---------- DISPLAY CONFIGURATION ---------------------
def display_weather():
    try:
        # Initialize the display
        epd = epd2in13_V4.EPD()
        epd.init()
        epd.Clear(0xFF)

        # Create a black image on a white background
        image = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(image)

        # Load a font (ensure the path is correct)
        font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
        font = ImageFont.truetype(font_path, 14)

        # Load the current weather icon
        if os.path.exists(current_icon_path):
            current_icon = Image.open(current_icon_path)
            image.paste(current_icon, (180, 5))  # Position the current weather icon
        else:
            print(f"Icon {current_icon_path} not found")

        # Draw the text for current weather
        draw.text((5, 0), f"Messina {today.day}/{today.month} {today.hour}:{today.minute} :", font=font, fill=0)
        draw.text((5, 20), f"{detailed_status}", font=font, fill=0)
        draw.text((5, 40), f"{temperature} °C   {humidity}%", font=font, fill=0)
        draw.text((5, 60), f"Wind: {wind['speed']} m/s", font=font, fill=0)

        # Load the weather icon for tomorrow
        if os.path.exists(tomorrow_icon_path):
            tomorrow_icon = Image.open(tomorrow_icon_path)
            image.paste(tomorrow_icon, (180, 62))  # Position the weather icon for tomorrow
        else:
            print(f"Icon {tomorrow_icon_path} not found")

        draw.text((0, 62), f"______________________________________________", font=font, fill=0)
        # Draw the text for tomorrow's weather with max and min temperatures
        draw.text((5, 80), f"Tomorrow: {tomorrow_status}", font=font, fill=0)
        draw.text((5, 100), f"{tomorrow_temperature_max} °C  - {tomorrow_temperature_min} °C", font=font, fill=0)

        # Rotate the image 180 degrees for the display
        image = image.rotate(180)

        # Display the image on the screen
        epd.display(epd.getbuffer(image))
        time.sleep(2)

        # Put the display in sleep mode to save power
        epd.sleep()

    except Exception as e:
        print(f"Error: {e}")

# Execute the function
display_weather()
