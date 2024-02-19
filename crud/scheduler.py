
import schedule
import time
import threading
from django.core.cache import cache
import requests

def my_daily_function():
    # Llamada a la API
    response = requests.get('https://v6.exchangerate-api.com/v6/'+'e85fc845c035937ad4ed26a6'+'/latets/PEN')
    if response.status_code == 200:
        # Guardar la respuesta en caché por un día (86400 segundos)
        cache.set('api_response', response.json(), timeout=86400)

def runSchedule():
    schedule.every().day.at("09:01").do(my_daily_function)  # Ejecutar todos los días a las 03:00
    while True:
        schedule.run_pending()
        time.sleep(60)  
# scheduler_thread = threading.Thread(target=runSchedule)
# scheduler_thread.daemon = True
# scheduler_thread.start()
