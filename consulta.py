import pyodbc

# Configura los detalles de tu base de datos
server = '127.0.0.1'  
database = 'MAXPOINT'
username = 'angel_0314'
password = '0314'

# Crear la conexión
conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

try:
    conn = pyodbc.connect(conn_str)
    print("Conexión exitosa a SQL Server")
    conn.close()
except Exception as e:
    print(f"Error al conectar: {e}")


