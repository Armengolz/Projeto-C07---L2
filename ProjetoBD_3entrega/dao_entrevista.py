from connection_dao import get_connection, close_connection
from mysql.connector import Error

def create_entrevista(data_hora, local, observacoes, id_visto):
    conn = get_connection()
    if not conn: return None
    cursor = conn.cursor()
    sql = "INSERT INTO entrevista (data_hora, local, observacoes, id_visto) VALUES (%s,%s,%s,%s)"
    try:
        cursor.execute(sql, (data_hora, local, observacoes, id_visto))
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"[ENTREVISTA CREATE] {e}")
        conn.rollback()
        return None
    finally:
        close_connection(conn, cursor)

def read_all_entrevistas():
    conn = get_connection()
    if not conn: return []
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id_entrevista, data_hora, local, observacoes, id_visto FROM entrevista")
        return cursor.fetchall()
    except Error as e:
        print(f"[ENTREVISTA READ] {e}")
        return []
    finally:
        close_connection(conn, cursor)

def update_entrevista(id_entrevista, data_hora, local, observacoes, id_visto):
    conn = get_connection()
    if not conn: return False
    cursor = conn.cursor()
    sql = "UPDATE entrevista SET data_hora=%s, local=%s, observacoes=%s, id_visto=%s WHERE id_entrevista=%s"
    try:
        cursor.execute(sql, (data_hora, local, observacoes, id_visto, id_entrevista))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(f"[ENTREVISTA UPDATE] {e}")
        conn.rollback()
        return False
    finally:
        close_connection(conn, cursor)

def delete_entrevista(id_entrevista):
    conn = get_connection()
    if not conn: return False
    cursor = conn.cursor()
    

    try:
        cursor.execute("SELECT id_entrevista FROM entrevista WHERE id_entrevista = %s", (id_entrevista,))
        if not cursor.fetchone():
            print(f"Entrevista com ID {id_entrevista} não encontrada.")
            return False
    except Error as e:
        print(f"[ENTREVISTA DELETE - VERIFICACAO] {e}")
        return False
    
    try:
        cursor.execute("SELECT COUNT(*) FROM funcionario_entrevista WHERE id_entrevista = %s", (id_entrevista,))
        count_funcionarios = cursor.fetchone()[0]
        if count_funcionarios > 0:
            print(f"ATENÇÃO: Esta entrevista possui {count_funcionarios} funcionário(s) associado(s) na tabela intermediária.")
            print("Excluir esta entrevista pode causar problemas de integridade referencial.")
            
            cursor.execute("""
                SELECT f.id_funcionario, f.nome 
                FROM funcionario f
                JOIN funcionario_entrevista fe ON f.id_funcionario = fe.id_funcionario
                WHERE fe.id_entrevista = %s
            """, (id_entrevista,))
            funcionarios = cursor.fetchall()
            print("\nFuncionários associados:")
            for func in funcionarios:
                print(f"ID: {func[0]}, Nome: {func[1]}")
            
            print("\nOpções:")
            print("1. Excluir apenas a entrevista (não recomendado - pode causar inconsistência)")
            print("2. Excluir a entrevista e os registros associados na tabela intermediária")
            print("3. Cancelar operação")
            
            opcao = input("Escolha uma opção (1/2/3): ")
            
            if opcao == '1':
                print("AVISO: Esta operação pode deixar o banco de dados em estado inconsistente!")
                confirm = input("Tem certeza que deseja continuar? (s/n): ")
                if confirm.lower() != 's':
                    return False
            elif opcao == '2':
                print("Excluindo registros associados na tabela intermediária...")
                try:
                    cursor.execute("DELETE FROM funcionario_entrevista WHERE id_entrevista = %s", (id_entrevista,))
                    conn.commit()
                    print(f"{cursor.rowcount} registro(s) excluído(s) da tabela intermediária.")
                except Error as e:
                    print(f"[ENTREVISTA DELETE - EXCLUIR FUNCIONARIO_ENTREVISTA] {e}")
                    conn.rollback()
                    return False
            else:
                print("Operação cancelada.")
                return False
    except Error as e:
        print(f"[ENTREVISTA DELETE - VERIFICACAO FUNCIONARIOS] {e}")
        return False
    
    try:
        sql = "DELETE FROM entrevista WHERE id_entrevista=%s"
        cursor.execute(sql, (id_entrevista,))
        conn.commit()
        
        if cursor.rowcount > 0:
            print(f"Entrevista ID {id_entrevista} excluída com sucesso.")
            return True
        else:
            print(f"Nenhuma entrevista foi excluída. ID {id_entrevista} pode não existir.")
            return False
    except Error as e:
        print(f"[ENTREVISTA DELETE] Erro ao excluir: {e}")
        conn.rollback()
        return False
    finally:
        close_connection(conn, cursor)