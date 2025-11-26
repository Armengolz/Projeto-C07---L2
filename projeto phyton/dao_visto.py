from connection_dao import get_connection, close_connection
from mysql.connector import Error

def create_visto(tipo_visto, data_solicitacao, status, id_solicitante):
    conn = get_connection()
    if not conn: return None
    cursor = conn.cursor()
    sql = "INSERT INTO visto (tipo_visto, data_solicitacao, status, id_solicitante) VALUES (%s,%s,%s,%s)"
    try:
        cursor.execute(sql, (tipo_visto, data_solicitacao, status, id_solicitante))
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"[VISTO CREATE] {e}")
        conn.rollback()
        return None
    finally:
        close_connection(conn, cursor)

def read_all_vistos():
    conn = get_connection()
    if not conn: return []
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id_visto, tipo_visto, data_solicitacao, status, id_solicitante FROM visto")
        return cursor.fetchall()
    except Error as e:
        print(f"[VISTO READ] {e}")
        return []
    finally:
        close_connection(conn, cursor)

def update_visto(id_visto, tipo_visto, data_solicitacao, status, id_solicitante):
    conn = get_connection()
    if not conn: return False
    cursor = conn.cursor()
    sql = "UPDATE visto SET tipo_visto=%s, data_solicitacao=%s, status=%s, id_solicitante=%s WHERE id_visto=%s"
    try:
        cursor.execute(sql, (tipo_visto, data_solicitacao, status, id_solicitante, id_visto))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(f"[VISTO UPDATE] {e}")
        conn.rollback()
        return False
    finally:
        close_connection(conn, cursor)

def delete_visto(id_visto):
    conn = get_connection()
    if not conn: return False
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id_visto FROM visto WHERE id_visto = %s", (id_visto,))
        if not cursor.fetchone():
            print(f"Visto com ID {id_visto} não encontrado.")
            return False
    except Error as e:
        print(f"[VISTO DELETE - VERIFICACAO] {e}")
        return False
    
    try:
        cursor.execute("SELECT COUNT(*) FROM entrevista WHERE id_visto = %s", (id_visto,))
        count_entrevistas = cursor.fetchone()[0]
        if count_entrevistas > 0:
            print(f"ATENÇÃO: Este visto possui {count_entrevistas} entrevista(s) associada(s).")
            print("Excluir este visto pode causar problemas de integridade referencial.")
    except Error as e:
        print(f"[VISTO DELETE - VERIFICACAO ENTREVISTAS] {e}")
    
    try:
        sql = "DELETE FROM visto WHERE id_visto=%s"
        cursor.execute(sql, (id_visto,))
        conn.commit()
        
        if cursor.rowcount > 0:
            print(f"Visto ID {id_visto} excluído com sucesso.")
            return True
        else:
            print(f"Nenhum visto foi excluído. ID {id_visto} pode não existir.")
            return False
    except Error as e:
        print(f"[VISTO DELETE] Erro ao excluir: {e}")
        conn.rollback()
        return False
    finally:
        close_connection(conn, cursor)