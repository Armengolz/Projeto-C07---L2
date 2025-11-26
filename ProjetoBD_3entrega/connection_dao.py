import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    'host': 'localhost',
    'database': 'consuladodigital',
    'user': 'root',            # ou consulado_user
    'password': 'root'         # sua senha aqui
}


def get_connection():
    """Retorna conexão com o MySQL ou None em falha."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
        return None
    except Error as e:
        print(f"[CONN] Erro ao conectar ao MySQL: {e}")
        return None

def close_connection(connection, cursor=None):
    """Fecha cursor e conexão se existirem."""
    try:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
    except Error as e:
        print(f"[CONN] Erro ao fechar a conexão: {e}")
