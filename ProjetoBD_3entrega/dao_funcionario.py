from connection_dao import get_connection, close_connection
from mysql.connector import Error

def create_funcionario(nome, cargo, departamento, contato, salario=0.00):
    conn = get_connection()
    if not conn: return None
    cursor = conn.cursor()
    sql = "INSERT INTO funcionario (nome, cargo, departamento, contato, salario) VALUES (%s,%s,%s,%s,%s)"
    try:
        cursor.execute(sql, (nome, cargo, departamento, contato, salario))
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"[FUNCIONARIO CREATE] {e}")
        conn.rollback()
        return None
    finally:
        close_connection(conn, cursor)

def read_all_funcionarios():
    conn = get_connection()
    if not conn: return []
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id_funcionario, nome, cargo, departamento, contato, salario FROM funcionario")
        return cursor.fetchall()
    except Error as e:
        print(f"[FUNCIONARIO READ] {e}")
        return []
    finally:
        close_connection(conn, cursor)

def update_funcionario(id_funcionario, nome, cargo, departamento, contato, salario):
    conn = get_connection()
    if not conn: return False
    cursor = conn.cursor()
    sql = "UPDATE funcionario SET nome=%s, cargo=%s, departamento=%s, contato=%s, salario=%s WHERE id_funcionario=%s"
    try:
        cursor.execute(sql, (nome, cargo, departamento, contato, salario, id_funcionario))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(f"[FUNCIONARIO UPDATE] {e}")
        conn.rollback()
        return False
    finally:
        close_connection(conn, cursor)

def delete_funcionario(id_funcionario):
    conn = get_connection()
    if not conn: return False
    cursor = conn.cursor()
    sql = "DELETE FROM funcionario WHERE id_funcionario=%s"
    try:
        cursor.execute(sql, (id_funcionario,))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(f"[FUNCIONARIO DELETE] {e}")
        conn.rollback()
        return False
    finally:
        close_connection(conn, cursor)