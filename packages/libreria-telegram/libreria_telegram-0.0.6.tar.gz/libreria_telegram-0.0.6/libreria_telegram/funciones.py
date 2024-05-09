"""
    funcion para enviar mensjajes a telegram
"""

import requests

def enviar_mensaje(token, chat_id, mensaje):
    """_summary_

    Args:
        token (_type_): _description_
        chat_id (_type_): _description_
        mensaje (_type_): _description_
    """
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    datos = {"chat_id": chat_id, "text": mensaje}
    response = requests.post(url, data=datos,timeout=60)
    if response.status_code == 200:
        print("Mensaje enviado correctamente.")
    else:
        print("Error al enviar el mensaje:", response.text)
