import time
from pyowm import OWM
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd2in13_V4
from pyowm.utils.config import get_default_config
import os
from datetime import datetime, timedelta

# ---------- CONFIGURAZIONE METEO ---------------------

# Impostazione della lingua in italiano per le descrizioni meteo
config_dict = get_default_config()
config_dict['language'] = 'it'
city='Messina,IT'
# API key per OpenWeatherMap (sostituisci con la tua API key valida)
owm = OWM("a07362be40821a534e187a92f784d011", config_dict)
mgr = owm.weather_manager()

# Ottieni il meteo attuale per Messina, Italia
observation = mgr.weather_at_place(city)
current_weather = observation.weather

# Estrai i dettagli del meteo attuale
detailed_status = current_weather.detailed_status
wind = current_weather.wind()
humidity = current_weather.humidity
temperature = current_weather.temperature('celsius')['temp']
current_icon_code = current_weather.weather_icon_name  # Es: '10d'

# Ottieni le previsioni meteo per Messina, Italia
forecast = mgr.forecast_at_place(city, '3h').forecast.weathers

# Calcola la data di domani
today = datetime.now()
tomorrow_date = (today + timedelta(days=1)).date()

# Filtra le previsioni per l'intero giorno successivo
tomorrow_forecasts = [w for w in forecast if w.reference_time('date').date() == tomorrow_date]

# Estrai temperatura minima e massima per il giorno successivo
tomorrow_temperature_min = min(w.temperature('celsius')['temp_min'] for w in tomorrow_forecasts)
tomorrow_temperature_max = max(w.temperature('celsius')['temp_max'] for w in tomorrow_forecasts)

# Determina lo stato meteo prevalente per il giorno successivo
tomorrow_status_list = [w.detailed_status for w in tomorrow_forecasts]
tomorrow_status = max(set(tomorrow_status_list), key=tomorrow_status_list.count)

# Usa l'icona della prima previsione del giorno successivo come rappresentativa
tomorrow_icon_code = tomorrow_forecasts[0].weather_icon_name
tomorrow_icon_path = f"./iconebmp/{tomorrow_icon_code}.bmp"

# Percorsi delle icone locali per il meteo attuale
current_icon_path = f"./iconebmp/{current_icon_code}.bmp"

# ---------- CONFIGURAZIONE DISPLAY ---------------------
def display_weather():
    try:
        # Inizializza il display
        epd = epd2in13_V4.EPD()
        epd.init()
        epd.Clear(0xFF)

        # Crea un'immagine nera su sfondo bianco
        image = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(image)

        # Carica un font (assicurati che il percorso sia corretto)
        font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
        font = ImageFont.truetype(font_path, 14)

        # Carica l'icona meteo attuale
        if os.path.exists(current_icon_path):
            current_icon = Image.open(current_icon_path)
            image.paste(current_icon, (180, 5))  # Posiziona l'icona meteo attuale
        else:
            print(f"Icona {current_icon_path} non trovata")

        # Disegna il testo per il meteo attuale
        draw.text((5, 0), f"Messina {today.day}/{today.month} {today.hour}:{today.minute}", font=font, fill=0)
        draw.text((5, 20), f"{detailed_status}", font=font, fill=0)
        draw.text((5, 40), f"{temperature} °C   {humidity}%", font=font, fill=0)
        draw.text((5, 60), f"Vento: {wind['speed']} m/s", font=font, fill=0)

        # Carica l'icona del meteo di domani
        if os.path.exists(tomorrow_icon_path):
            tomorrow_icon = Image.open(tomorrow_icon_path)
            image.paste(tomorrow_icon, (180, 62))  # Posiziona l'icona meteo di domani
        else:
            print(f"Icona {tomorrow_icon_path} non trovata")

        draw.text((0, 62), f"______________________________________________", font=font, fill=0)
        # Disegna il testo per il meteo di domani con massima e minima
        draw.text((5, 80), f"Domani: {tomorrow_status}", font=font, fill=0)
        draw.text((5, 100), f"{tomorrow_temperature_max} °C  - {tomorrow_temperature_min} °C", font=font, fill=0)

        # Ruota l'immagine di 180 gradi per il display
        image = image.rotate(180)

        # Mostra l'immagine sul display
        epd.display(epd.getbuffer(image))
        time.sleep(2)

        # Mette il display in modalità sleep per risparmiare energia
        epd.sleep()

    except Exception as e:
        print(f"Errore: {e}")

# Esegui la funzione
display_weather()
