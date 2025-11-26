from connection_dao import get_connection, close_connection
from mysql.connector import Error

def create_solicitante(nome, data_nascimento, nacionalidade, endereco, contato, id_passaporte):
    conn = get_connection()
    if not conn: return None
    cursor = conn.cursor()
    sql = """INSERT INTO solicitante (nome, data_nascimento, nacionalidade, endereco, contato, id_passaporte)
             VALUES (%s,%s,%s,%s,%s,%s)"""
    try:
        cursor.execute(sql, (nome, data_nascimento, nacionalidade, endereco, contato, id_passaporte))
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"[SOLICITANTE CREATE] {e}")
        conn.rollback()
        return None
    finally:
        close_connection(conn, cursor)

def read_all_solicitantes():
    conn = get_connection()
    if not conn: return []
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id_solicitante, nome, data_nascimento, nacionalidade, endereco, contato, id_passaporte FROM solicitante")
        return cursor.fetchall()
    except Error as e:
        print(f"[SOLICITANTE READ] {e}")
        return []
    finally:
        close_connection(conn, cursor)

def update_solicitante(id_solicitante, nome, data_nascimento, nacionalidade, endereco, contato, id_passaporte):
    conn = get_connection()
    if not conn: return False
    cursor = conn.cursor()
    sql = """UPDATE solicitante 
             SET nome=%s, data_nascimento=%s, nacionalidade=%s, endereco=%s, contato=%s, id_passaporte=%s 
             WHERE id_solicitante=%s"""
    try:
        cursor.execute(sql, (nome, data_nascimento, nacionalidade, endereco, contato, id_passaporte, id_solicitante))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(f"[SOLICITANTE UPDATE] {e}")
        conn.rollback()
        return False
    finally:
        close_connection(conn, cursor)

def delete_solicitante(id_solicitante):
    conn = get_connection()
    if not conn: return False
    cursor = conn.cursor()
   
    try:
        cursor.execute("SELECT id_solicitante FROM solicitante WHERE id_solicitante = %s", (id_solicitante,))
        if not cursor.fetchone():
            print(f"Solicitante com ID {id_solicitante} não encontrado.")
            return False
    except Error as e:
        print(f"[SOLICITANTE DELETE - VERIFICACAO] {e}")
        return False

    try:
        sql = "DELETE FROM solicitante WHERE id_solicitante=%s"
        cursor.execute(sql, (id_solicitante,))
        conn.commit()
        
        if cursor.rowcount > 0:
            print(f"Solicitante ID {id_solicitante} excluído com sucesso.")
            return True
        else:
            print(f"Nenhum solicitante foi excluído. ID {id_solicitante} pode não existir.")
            return False
    except Error as e:
        print(f"[SOLICITANTE DELETE] Erro ao excluir: {e}")
        conn.rollback()
        return False
    finally:
        close_connection(conn, cursor)