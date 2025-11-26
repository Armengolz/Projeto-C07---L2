from connection_dao import get_connection, close_connection
from mysql.connector import Error

def create_passaporte(numero, data_emissao, data_validade, pais_emissor):
    conn = get_connection()
    if not conn: return None
    cursor = conn.cursor()
    sql = "INSERT INTO passaporte (numero_passaporte, data_emissao, data_validade, pais_emissor) VALUES (%s,%s,%s,%s)"
    try:
        cursor.execute(sql, (numero, data_emissao, data_validade, pais_emissor))
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"[PASSAPORTE CREATE] {e}")
        conn.rollback()
        return None
    finally:
        close_connection(conn, cursor)

def read_all_passaportes():
    conn = get_connection()
    if not conn: return []
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id_passaporte, numero_passaporte, data_emissao, data_validade, pais_emissor FROM passaporte")
        return cursor.fetchall()
    except Error as e:
        print(f"[PASSAPORTE READ] {e}")
        return []
    finally:
        close_connection(conn, cursor)

def update_passaporte(id_passaporte, numero, data_emissao, data_validade, pais_emissor):
    conn = get_connection()
    if not conn: return False
    cursor = conn.cursor()
    sql = "UPDATE passaporte SET numero_passaporte=%s, data_emissao=%s, data_validade=%s, pais_emissor=%s WHERE id_passaporte=%s"
    try:
        cursor.execute(sql, (numero, data_emissao, data_validade, pais_emissor, id_passaporte))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(f"[PASSAPORTE UPDATE] {e}")
        conn.rollback()
        return False
    finally:
        close_connection(conn, cursor)

def delete_passaporte(id_passaporte, excluir_dependentes=False):
    conn = get_connection()
    if not conn: return False
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id_passaporte FROM passaporte WHERE id_passaporte = %s", (id_passaporte,))
        if not cursor.fetchone():
            print(f"Passaporte com ID {id_passaporte} não encontrado.")
            return False
    except Error as e:
        print(f"[PASSAPORTE DELETE - VERIFICACAO] {e}")
        return False
    
    try:
        cursor.execute("SELECT COUNT(*) FROM solicitante WHERE id_passaporte = %s", (id_passaporte,))
        count_solicitantes = cursor.fetchone()[0]
        
        if count_solicitantes > 0:
            print(f"ATENÇÃO: Este passaporte possui {count_solicitantes} solicitante(s) associado(s).")
            
            if not excluir_dependentes:
                print("Para excluir este passaporte, você precisa primeiro:")
                print("1. Excluir os solicitantes associados, ou")
                print("2. Atualizar os solicitantes para usar outro passaporte")
                return False
            
            print("Excluindo solicitantes associados...")
            try:
                cursor.execute("DELETE FROM solicitante WHERE id_passaporte = %s", (id_passaporte,))
                conn.commit()
                print(f"{cursor.rowcount} solicitante(s) excluído(s).")
            except Error as e:
                print(f"[PASSAPORTE DELETE - EXCLUIR SOLICITANTES] {e}")
                conn.rollback()
                return False
    except Error as e:
        print(f"[PASSAPORTE DELETE - VERIFICACAO SOLICITANTES] {e}")
        return False
    
    try:
        sql = "DELETE FROM passaporte WHERE id_passaporte=%s"
        cursor.execute(sql, (id_passaporte,))
        conn.commit()
        
        if cursor.rowcount > 0:
            print(f"Passaporte ID {id_passaporte} excluído com sucesso.")
            return True
        else:
            print(f"Nenhum passaporte foi excluído. ID {id_passaporte} pode não existir.")
            return False
    except Error as e:
        print(f"[PASSAPORTE DELETE] Erro ao excluir: {e}")
        conn.rollback()
        return False
    finally:
        close_connection(conn, cursor)