import requests
from bs4 import BeautifulSoup
import telegram

def verificar_precio_bajo(url, precio_limite, chat_id, bot_token):
    # Obtener el contenido HTML de la página
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrar el elemento que contiene el precio
    # Esto depende de la estructura HTML de la página específica
    precio_elemento = soup.find('span', {'class': 'precio'})

    # Obtener el valor del precio como una cadena
    precio_str = precio_elemento.text.strip()

    # Convertir el valor del precio a un número
    precio = float(precio_str)

    # Verificar si el precio es menor que el límite establecido
    if precio < precio_limite:
        # Inicializar el bot de Telegram
        bot = telegram.Bot(token=bot_token)

        # Enviar el mensaje de alerta al chat_id especificado
        mensaje = f"¡Alerta! El precio en {url} es más bajo de lo esperado."
        bot.send_message(chat_id=chat_id, text=mensaje)

# Ejemplo de uso
url = 'https://www.ejemplo.com/producto'
precio_limite = 50.0
chat_id = 'TU_CHAT_ID'  # Reemplaza con el chat_id válido
bot_token = 'TU_BOT_TOKEN'  # Reemplaza con el token de tu bot

verificar_precio_bajo(url, precio_limite, chat_id, bot_token)
