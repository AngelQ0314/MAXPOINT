from flask import Flask, jsonify
import pyodbc

app = Flask(__name__)

# Configuración de la base de datos
server = '127.0.0.1'
database = 'MAXPOINT'
username = 'angel_0314'
password = '0314'
conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

def obtener_datos():
    try:
        # Conectaxion a la base de datos
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Consulta SQL
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

        # Ejecutar la consulta
        cursor.execute(query)

        # Obtener los resultados
        results = cursor.fetchone()

        # Cerrar conexión
        conn.close()

        # Formatear los datos en JSON
        data = {
            "intFlag1": {
                "TOTAL_DE_REGISTROS_NULOS": results[0],
                
                "TOTAL_DE_REGISTROS_NULOS_MAYOR_A_5_MINUTOS": results[1]
            },
            "intFlag2": {
                "TOTAL_DE_REGISTROS_NULOS": results[2],

                "TOTAL_DE_REGISTROS_NULOS_MAYOR_A_5_MINUTOS": results[3]
            },
            "intFlag3": {
                "TOTAL_DE_REGISTROS_NULOS": results[4],

                "TOTAL_DE_REGISTROS_NULOS_MAYOR_A_5_MINUTOS": results[5]
            }
        }

        return data

    except Exception as e:
        return {"error": str(e)}

@app.route('/registros', methods=['GET'])
def obtener_resultados():
    return jsonify(obtener_datos())

if __name__ == '__main__':
    app.run(debug=True, port=3000)
