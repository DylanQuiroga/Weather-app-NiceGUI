from nicegui import ui
import requests

API_URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = "API_KEY"  # Aquí va tu clave de la API, obtenida en https://openweathermap.org/current

def fetch_weather():
    """Consulta la API con la ciudad ingresada por el usuario y actualiza la interfaz."""
    city = city_input.value.strip()  # Obtener el valor de entrada
    if not city:
        ui.notify("Por favor, ingresa una ciudad.", color="red")
        return

    params = {
        "q": city,          # Ciudad ingresada por el usuario
        "appid": API_KEY,   # Clave de la API
        "units": "metric",  # Unidades métricas (°C)
        "lang": "es",       # Idioma español
    }
    response = requests.get(API_URL, params=params)  # Consultar la API
    
    if response.status_code == 200:
        data = response.json()
        city_label.content = f"<b>Ciudad:</b> {data['name']} - {data['sys']['country']}"
        coord_label.content = f"<b>Coordenadas:</b> {data['coord']['lat']}, {data['coord']['lon']}"

        utc = data['timezone'] / 3600
        utc_label.content = f"<b>UTC:</b> {utc:+.1f} horas"
        temp_label.content = f"<b>Temperatura:</b> {data['main']['temp']} °C"
        humidity_label.content = f"<b>Humedad:</b> {data['main']['humidity']} %"
        clouds_label.content = f"<b>Nubosidad:</b> {data['clouds']['all']} %"
        wind_label.content = f"<b>Viento:</b> {data['wind']['speed']} m/s"

        # Hacer visibles las etiquetas
        city_label.visible = True
        coord_label.visible = True
        temp_label.visible = True
        utc_label.visible = True
        humidity_label.visible = True
        clouds_label.visible = True
    else:
        if response.status_code == 404:
            ui.notify("Ciudad no encontrada. Verifica el nombre ingresado.", color="red")
        if response.status_code == 401:
            ui.notify("Clave de API inválida. Verifica tu clave en el código.", color="red")
        if response.status_code == 429:
            ui.notify("Demasiadas solicitudes. Intenta nuevamente en unos minutos.", color="red")
        if response.status_code == 500 or 502 or 503 or 504:
            ui.notify("Error interno del servidor. Inténtalo más tarde o contactate con asistencia.", color="red")

# Interfaz gráfica con NiceGUI
ui.label("Consulta el clima").style("font-size: 24px; font-weight: bold; margin-bottom: 20px;")

# Contenedor horizontal para la imagen y el campo de entrada
with ui.row().style("align-items: center; margin-bottom: 10px;"):
    city_input = ui.input(label="Nombre de la ciudad", placeholder="Ej. Santiago")
    ui.image("image.png").style("width: 50px; height: 50px; margin-left: 10px;")

ui.button("Consultar clima", on_click=fetch_weather).props("color=blue")

# Etiquetas ocultas inicialmente, usando ui.html() para mayor personalización
city_label = ui.html("").style("margin-top: 10px;")
city_label.visible = False

coord_label = ui.html("")
coord_label.visible = False

utc_label = ui.html("")
utc_label.visible = False

temp_label = ui.html("")
temp_label.visible = False

humidity_label = ui.html("")
humidity_label.visible = False

clouds_label = ui.html("")
clouds_label.visible = False

wind_label = ui.html("")
wind_label.visible = False

# Ejecutar en modo escritorio
ui.run(native=True, title="Clima en tu ciudad", fullscreen=False, window_size=(300, 550))
