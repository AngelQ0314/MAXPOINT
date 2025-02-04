import pyodbc

# Configuracion a la base de datos
server = '127.0.0.1'
database = 'MAXPOINT'
username = 'angel_0314'
password = '0314'
conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

try:
    # Conectar a la base de datos
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

    # Ejecutar la consulta
    cursor.execute(query)

    # Obtener los resultados
    results = cursor.fetchone()

    # Mostrar los resultados
    print(f"-intFlag1 :",f"TOTAL DE REGISTROS NULOS : {results[0]} ; " , f"TOTAL DE REGISTROS NULOS MAYOR A 5 MINUTOS : {results[1]}")
    print(f"-intFlag2 :",f"TOTAL DE REGISTROS NULOS : {results[2]} ; " , f"TOTAL DE REGISTROS NULOS MAYOR A 5 MINUTOS : {results[3]}")
    print(f"-intFlag3 :",f"TOTAL DE REGISTROS NULOS : {results[4]} ; " , f"TOTAL DE REGISTROS NULOS MAYOR A 5 MINUTOS : {results[5]}")

    # Cerrar conexión
    conn.close()

except Exception as e:
    print(f"Error al conectar: {e}")
