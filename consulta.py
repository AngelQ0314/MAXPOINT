import requests
import pyodbc
import time

# Configuración del bot de Telegram
TELEGRAM_BOT_TOKEN = "7949767892:AAGb0rrxLo5OQlUoYLnafr3qioxPEGnYLsU" 
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

# Configuración de la base de datos SQL Server
server = '127.0.0.1'
database = 'MAXPOINT'
username = 'angel_0314'
password = '0314'
conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Variable para rastrear el último mensaje procesado
LAST_UPDATE_ID = None

def enviar_mensaje_telegram(chat_id, mensaje):
    """Envía un mensaje al chat de Telegram."""
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": mensaje, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def obtener_datos():
    """Ejecuta la consulta en SQL Server y devuelve los datos formateados."""
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        query = """
        WITH HoraCalculada AS (
            SELECT Fecha, Hora, 
                   RIGHT(Fecha, 12) AS HoraDesdeFecha,  
                   Hora AS HoraOriginal,  
                   DATEDIFF(MINUTE, 
                            TRY_CONVERT(TIME, RIGHT(Fecha, 12)),  
                            TRY_CONVERT(TIME, Hora)  
                   ) AS Minutos_Transcurridos,
                   intFlag1,
                   intFlag2,
                   intFlag3
            FROM dbo.UpdateStore
        )
        SELECT 
            COUNT(CASE WHEN intFlag1 IS NULL THEN 1 END) AS Total_NULL_intFlag1,
            COUNT(CASE WHEN intFlag1 IS NULL AND HC.Minutos_Transcurridos > 5 THEN 1 END) AS NULL_Mayor_5_Minutos_intFlag1,
            COUNT(CASE WHEN intFlag2 IS NULL THEN 1 END) AS Total_NULL_intFlag2,
            COUNT(CASE WHEN intFlag2 IS NULL AND HC.Minutos_Transcurridos > 5 THEN 1 END) AS NULL_Mayor_5_Minutos_intFlag2,
            COUNT(CASE WHEN intFlag3 IS NULL THEN 1 END) AS Total_NULL_intFlag3,
            COUNT(CASE WHEN intFlag3 IS NULL AND HC.Minutos_Transcurridos > 5 THEN 1 END) AS NULL_Mayor_5_Minutos_intFlag3
        FROM HoraCalculada HC;
        """

        cursor.execute(query)
        results = cursor.fetchone()
        conn.close()
        mensaje = (
            f"📊 *Reporte de Registros Nulos*\n\n"
            f"*intFlag1:*\n"
            f"- Total Nulos: {results[0]}\n"
            f"- Nulos mayores a 5 Minutos: {results[1]}\n\n"
            f"*intFlag2:*\n"
            f"- Total Nulos: {results[2]}\n"
            f"- Nulos mayores 5 Minutos: {results[3]}\n\n"
            f"*intFlag3:*\n"
            f"- Total Nulos: {results[4]}\n"
            f"- Nulos mayores 5 Minutos: {results[5]}"
        )

        return mensaje

    except Exception as e:
        return f"⚠️ Error al obtener datos: {str(e)}"

def escuchar_mensajes():
    """Consulta los mensajes en Telegram y responde si el usuario envía '/start' o 'Verificar registros'."""
    global LAST_UPDATE_ID

    url = f"{TELEGRAM_API_URL}/getUpdates"
    response = requests.get(url).json()

    if "result" in response:
        for update in response["result"]:
            update_id = update["update_id"]
            chat_id = update["message"]["chat"]["id"]
            texto = update["message"].get("text", "").strip().lower()

            if LAST_UPDATE_ID is None or update_id > LAST_UPDATE_ID:
                LAST_UPDATE_ID = update_id  # Guardar el último mensaje procesado

                if texto == "/start":
                    mensaje_bienvenida = (
                        "👋 *Bienvenido al Bot de Registros!*\n\n"
                        "Para consultar los registros en la base de datos, envía el mensaje:\n"
                        "`Verificar registros`"
                    )
                    enviar_mensaje_telegram(chat_id, mensaje_bienvenida)

                elif texto == "verificar registros":
                    respuesta = obtener_datos()
                    enviar_mensaje_telegram(chat_id, respuesta)
                else:
                    enviar_mensaje_telegram(chat_id, "Envía *Verificar registros* para obtener el reporte.")

if __name__ == "__main__":
    print("Bot de Telegram en ejecución...")
    while True:
        escuchar_mensajes()
        time.sleep(5)  
