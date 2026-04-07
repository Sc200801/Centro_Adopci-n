import pymysql as mysql

# Configuración de conexión. Cámbialo por tus credenciales.
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "adoption_user",
    "password": "B34ut1M4rk",
    "database": "CentroAdopcion"
}

def get_db_connection():
    try:
        conn = mysql.connect(**DB_CONFIG)
        return conn
    except mysql.Error as e:
        print(f"Error conectando a MySQL: {e}")
        return None