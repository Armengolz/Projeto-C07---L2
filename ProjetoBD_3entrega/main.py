import sys
import os
from dao_passaporte import create_passaporte, read_all_passaportes, update_passaporte, delete_passaporte
from dao_solicitante import create_solicitante, read_all_solicitantes, update_solicitante, delete_solicitante
from dao_visto import create_visto, read_all_vistos, update_visto, delete_visto
from dao_entrevista import create_entrevista, read_all_entrevistas, update_entrevista, delete_entrevista
from dao_funcionario import create_funcionario, read_all_funcionarios, update_funcionario, delete_funcionario

from connection_dao import get_connection, close_connection

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_cabecalho():
    print("=" * 60)
    print(" " * 20 + "SISTEMA CONSULADO" + " " * 20)
    print("=" * 60)

def exibir_rodape():
    print("\n" + "=" * 60)
    print(" " * 15 + "Sistema de Gerenciamento Consular" + " " * 15)
    print("=" * 60)

def menu():
    limpar_tela()
    exibir_cabecalho()
    print("\n=== MENU PRINCIPAL ===\n")
    print("[1] PASSAPORTE")
    print("  [1.1] Inserir Novo Passaporte")
    print("  [1.2] Listar Todos os Passaportes")
    print("  [1.3] Atualizar Passaporte")
    print("  [1.4] Excluir Passaporte")
    print("\n[2] SOLICITANTE")
    print("  [2.1] Inserir Novo Solicitante")
    print("  [2.2] Listar Todos os Solicitantes")
    print("  [2.3] Atualizar Solicitante")
    print("  [2.4] Excluir Solicitante")
    print("\n[3] VISTO")
    print("  [3.1] Inserir Novo Visto")
    print("  [3.2] Listar Todos os Vistos")
    print("  [3.3] Atualizar Visto")
    print("  [3.4] Excluir Visto")
    print("\n[4] ENTREVISTA")
    print("  [4.1] Inserir Nova Entrevista")
    print("  [4.2] Listar Todas as Entrevistas")
    print("  [4.3] Atualizar Entrevista")
    print("  [4.4] Excluir Entrevista")
    print("\n[5] FUNCIONÁRIO")
    print("  [5.1] Inserir Novo Funcionário")
    print("  [5.2] Listar Todos os Funcionários")
    print("  [5.3] Atualizar Funcionário")
    print("  [5.4] Excluir Funcionário")
    print("\n[6] UTILITÁRIOS")
    print("  [6.1] Exemplos de JOINs")
    print("\n[0] SAIR DO SISTEMA")
    exibir_rodape()
    return input("\nDigite a opção desejada: ")

def submenu(titulo, opcoes):
    while True:
        limpar_tela()
        exibir_cabecalho()
        print(f"\n=== {titulo} ===\n")
        for i, opcao in enumerate(opcoes, 1):
            print(f"[{i}] {opcao}")
        print("[0] Voltar ao Menu Principal")
        exibir_rodape()
        escolha = input("\nDigite a opção desejada: ")
        
        if escolha == '0':
            return None
        elif escolha.isdigit() and 1 <= int(escolha) <= len(opcoes):
            return escolha
        else:
            input("\nOpção inválida! Pressione Enter para continuar...")

def exemplos_joins():
    conn = get_connection()
    if not conn:
        print("Não foi possível conectar para executar JOINs.")
        return
    cursor = conn.cursor()

    limpar_tela()
    exibir_cabecalho()
    print("\n=== EXEMPLOS DE JOINs ===\n")

    print("\n--- JOINS SEM TABELA INTERMEDIÁRIA (joins diretos por FK) ---\n")
    try:
        cursor.execute("""
            SELECT s.nome, v.tipo_visto, v.status
            FROM solicitante s
            JOIN visto v ON s.id_solicitante = v.id_solicitante
            LIMIT 10
        """)
        print("1) Solicitante <-> Visto:")
        for r in cursor.fetchall():
            print(f"   {r}")
    except Exception as e:
        print("Erro join 1:", e)

    try:
        cursor.execute("""
            SELECT v.id_visto, v.tipo_visto, e.data_hora, e.local
            FROM visto v
            JOIN entrevista e ON v.id_visto = e.id_visto
            LIMIT 10
        """)
        print("\n2) Visto <-> Entrevista:")
        for r in cursor.fetchall():
            print(f"   {r}")
    except Exception as e:
        print("Erro join 2:", e)

    try:
        cursor.execute("""
            SELECT s.nome, v.tipo_visto, e.data_hora
            FROM solicitante s
            JOIN visto v ON s.id_solicitante = v.id_solicitante
            JOIN entrevista e ON v.id_visto = e.id_visto
            LIMIT 10
        """)
        print("\n3) Solicitante -> Visto -> Entrevista:")
        for r in cursor.fetchall():
            print(f"   {r}")
    except Exception as e:
        print("Erro join 3:", e)

    print("\n--- JOINS COM TABELA INTERMEDIÁRIA (funcionario_entrevista) ---\n")
    try:
        cursor.execute("""
            SELECT f.nome, e.id_entrevista, e.data_hora
            FROM funcionario f
            JOIN funcionario_entrevista fe ON f.id_funcionario = fe.id_funcionario
            JOIN entrevista e ON fe.id_entrevista = e.id_entrevista
            LIMIT 10
        """)
        print("4) Funcionario <-> Entrevista via funcionario_entrevista:")
        for r in cursor.fetchall():
            print(f"   {r}")
    except Exception as e:
        print("Erro join 4:", e)

    try:
        cursor.execute("""
            SELECT DISTINCT f.id_funcionario, f.nome, f.departamento
            FROM funcionario f
            JOIN funcionario_entrevista fe ON f.id_funcionario = fe.id_funcionario
            LIMIT 10
        """)
        print("\n5) Funcionarios que entrevistaram:")
        for r in cursor.fetchall():
            print(f"   {r}")
    except Exception as e:
        print("Erro join 5:", e)

    try:
        cursor.execute("""
            SELECT e.id_entrevista, e.data_hora, GROUP_CONCAT(f.nome SEPARATOR ', ') as funcionarios
            FROM entrevista e
            LEFT JOIN funcionario_entrevista fe ON e.id_entrevista = fe.id_entrevista
            LEFT JOIN funcionario f ON fe.id_funcionario = f.id_funcionario
            GROUP BY e.id_entrevista
            LIMIT 10
        """)
        print("\n6) Entrevista e funcionarios:")
        for r in cursor.fetchall():
            print(f"   {r}")
    except Exception as e:
        print("Erro join 6:", e)

    close_connection(conn, cursor)
    exibir_rodape()
    input("\nPressione Enter para voltar ao menu principal...")

def main_loop():
    while True:
        escolha = menu()
        
        if escolha == '1':
            opcao = submenu("MENU PASSAPORTE", [
                "Inserir Novo Passaporte",
                "Listar Todos os Passaportes",
                "Atualizar Passaporte",
                "Excluir Passaporte"
            ])
            
            if opcao == '1':
                limpar_tela()
                exibir_cabecalho()
                print("\n=== INSERIR NOVO PASSAPORTE ===\n")
                numero = input("Número do passaporte: ")
                di = input("Data de emissão (YYYY-MM-DD): ")
                dv = input("Data de validade (YYYY-MM-DD): ")
                pais = input("País emissor: ")
                pid = create_passaporte(numero, di, dv, pais)
                if pid:
                    print(f"\nPassaporte inserido com sucesso! ID: {pid}")
                else:
                    print("\nFalha ao inserir passaporte.")
                input("\nPressione Enter para continuar...")
                
            elif opcao == '2':
                limpar_tela()
                exibir_cabecalho()
                print("\n=== LISTAR TODOS OS PASSAPORTES ===\n")
                passaportes = read_all_passaportes()
                if passaportes:
                    for p in passaportes:
                        print(f"ID: {p[0]}, Número: {p[1]}, Emissão: {p[2]}, Validade: {p[3]}, País: {p[4]}")
                else:
                    print("Nenhum passaporte encontrado.")
                input("\nPressione Enter para continuar...")
                
            elif opcao == '3':
                limpar_tela()
                exibir_cabecalho()
                print("\n=== ATUALIZAR PASSAPORTE ===\n")
                id_pass = input("ID do passaporte a ser atualizado: ")
                
                conn = get_connection()
                if conn:
                    cursor = conn.cursor()
                    try:
                        cursor.execute("SELECT * FROM passaporte WHERE id_passaporte=%s", (id_pass,))
                        passaporte = cursor.fetchone()
                        if passaporte:
                            print(f"\nDados atuais:")
                            print(f"ID: {passaporte[0]}")
                            print(f"Número: {passaporte[1]}")
                            print(f"Data de Emissão: {passaporte[2]}")
                            print(f"Data de Validade: {passaporte[3]}")
                            print(f"País Emissor: {passaporte[4]}")
                        else:
                            print("Passaporte não encontrado!")
                            close_connection(conn, cursor)
                            input("\nPressione Enter para continuar...")
                            continue
                    except Exception as e:
                        print(f"Erro ao buscar passaporte: {e}")
                        close_connection(conn, cursor)
                        input("\nPressione Enter para continuar...")
                        continue
                    close_connection(conn, cursor)
                
                print("\nDeixe em branco para manter o valor atual")
                numero = input(f"Novo número do passaporte [{passaporte[1]}]: ") or passaporte[1]
                di = input(f"Nova data de emissão (YYYY-MM-DD) [{passaporte[2]}]: ") or passaporte[2]
                dv = input(f"Nova data de validade (YYYY-MM-DD) [{passaporte[3]}]: ") or passaporte[3]
                pais = input(f"Novo país emissor [{passaporte[4]}]: ") or passaporte[4]
                
                if update_passaporte(id_pass, numero, di, dv, pais):
                    print("\nPassaporte atualizado com sucesso!")
                else:
                    print("\nFalha ao atualizar passaporte.")
                input("\nPressione Enter para continuar...")
                
            elif opcao == '4':
                limpar_tela()
                exibir_cabecalho()
                print("\n=== EXCLUIR PASSAPORTE ===\n")
                id_pass = input("ID do passaporte a ser excluído: ")
                
                conn = get_connection()
                if conn:
                    cursor = conn.cursor()
                    try:
                        cursor.execute("SELECT * FROM passaporte WHERE id_passaporte=%s", (id_pass,))
                        passaporte = cursor.fetchone()
                        if not passaporte:
                            print("Passaporte não encontrado!")
                            close_connection(conn, cursor)
                            input("\nPressione Enter para continuar...")
                            continue
                        else:
                            print(f"\nDados do passaporte a ser excluído:")
                            print(f"ID: {passaporte[0]}")
                            print(f"Número: {passaporte[1]}")
                            print(f"Data de Emissão: {passaporte[2]}")
                            print(f"País Emissor: {passaporte[4]}")
                    except Exception as e:
                        print(f"Erro ao buscar passaporte: {e}")
                        close_connection(conn, cursor)
                        input("\nPressione Enter para continuar...")
                        continue
                    close_connection(conn, cursor)
                
                conn = get_connection()
                if conn:
                    cursor = conn.cursor()
                    try:
                        cursor.execute("SELECT COUNT(*) FROM solicitante WHERE id_passaporte=%s", (id_pass,))
                        count_solicitantes = cursor.fetchone()[0]
                        if count_solicitantes > 0:
                            print(f"\nATENÇÃO: Este passaporte possui {count_solicitantes} solicitante(s) associado(s).")
                            print("Excluir este passaporte pode causar problemas de integridade referencial.")
                            
                            cursor.execute("SELECT id_solicitante, nome FROM solicitante WHERE id_passaporte=%s", (id_pass,))
                            solicitantes = cursor.fetchall()
                            print("\nSolicitantes associados:")
                            for sol in solicitantes:
                                print(f"ID: {sol[0]}, Nome: {sol[1]}")
                            
                            print("\nOpções:")
                            print("1. Excluir apenas o passaporte (não recomendado - pode causar inconsistência)")
                            print("2. Excluir o passaporte e todos os solicitantes associados")
                            print("3. Cancelar operação")
                            
                            opcao = input("Escolha uma opção (1/2/3): ")
                            
                            if opcao == '1':
                                print("AVISO: Esta operação pode deixar o banco de dados em estado inconsistente!")
                                confirm = input("Tem certeza que deseja continuar? (s/n): ")
                                if confirm.lower() != 's':
                                    print("Operação cancelada.")
                                    input("\nPressione Enter para continuar...")
                                    continue
                                if delete_passaporte(id_pass):
                                    print("Passaporte excluído com sucesso!")
                                else:
                                    print("Falha ao excluir passaporte.")
                            elif opcao == '2':
                                confirm = input(f"Tem certeza que deseja excluir o passaporte e os {count_solicitantes} solicitantes associados? (s/n): ")
                                if confirm.lower() != 's':
                                    print("Operação cancelada.")
                                    input("\nPressione Enter para continuar...")
                                    continue
                                if delete_passaporte(id_pass, excluir_dependentes=True):
                                    print("Passaporte e solicitantes associados excluídos com sucesso!")
                                else:
                                    print("Falha ao excluir passaporte e solicitantes.")
                            else:
                                print("Operação cancelada.")
                        else:
                            confirm = input(f"Tem certeza que deseja excluir o passaporte ID {id_pass}? (s/n): ")
                            if confirm.lower() != 's':
                                print("Operação cancelada.")
                                input("\nPressione Enter para continuar...")
                                continue
                                
                            if delete_passaporte(id_pass):
                                print("Passaporte excluído com sucesso!")
                            else:
                                print("Falha ao excluir passaporte.")
                    except Exception as e:
                        print(f"Erro ao verificar solicitantes associados: {e}")
                    finally:
                        close_connection(conn, cursor)
                
                input("\nPressione Enter para continuar...")
        
        elif escolha == '2':
            opcao = submenu("MENU SOLICITANTE", [
                "Inserir Novo Solicitante",
                "Listar Todos os Solicitantes",
                "Atualizar Solicitante",
                "Excluir Solicitante"
            ])
            
            if opcao == '1':
                limpar_tela()
                exibir_cabecalho()
                print("\n=== INSERIR NOVO SOLICITANTE ===\n")
                nome = input("Nome: ")
                dn = input("Data de nascimento (YYYY-MM-DD): ")
                nat = input("Nacionalidade: ")
                end = input("Endereço: ")
                contato = input("Contato: ")
                idp = input("ID do passaporte: ")
                sid = create_solicitante(nome, dn, nat, end, contato, idp)
                if sid:
                    print(f"\nSolicitante inserido com sucesso! ID: {sid}")
                else:
                    print("\nFalha ao inserir solicitante.")
                input("\nPressione Enter para continuar...")
                
            elif opcao == '2':
                limpar_tela()
                exibir_cabecalho()
                print("\n=== LISTAR TODOS OS SOLICITANTES ===\n")
                solicitantes = read_all_solicitantes()
                if solicitantes:
                    for s in solicitantes:
                        print(f"ID: {s[0]}, Nome: {s[1]}, Nascimento: {s[2]}, Nacionalidade: {s[3]}, Endereço: {s[4]}, Contato: {s[5]}, ID Passaporte: {s[6]}")
                else:
                    print("Nenhum solicitante encontrado.")
                input("\nPressione Enter para continuar...")
                
            elif opcao == '3':
                limpar_tela()
                exibir_cabecalho()
                print("\n=== ATUALIZAR SOLICITANTE ===\n")
                id_sol = input("ID do solicitante a ser atualizado: ")
                
                conn = get_connection()
                if conn:
                    cursor = conn.cursor()
                    try:
                        cursor.execute("SELECT * FROM solicitante WHERE id_solicitante=%s", (id_sol,))
                        solicitante = cursor.fetchone()
                        if solicitante:
                            print(f"\nDados atuais:")
                            print(f"ID: {solicitante[0]}")
                            print(f"Nome: {solicitante[1]}")
                            print(f"Data de Nascimento: {solicitante[2]}")
                            print(f"Nacionalidade: {solicitante[3]}")
                            print(f"Endereço: {solicitante[4]}")
                            print(f"Contato: {solicitante[5]}")
                            print(f"ID Passaporte: {solicitante[6]}")
                        else:
                            print("Solicitante não encontrado!")
                            close_connection(conn, cursor)
                            input("\nPressione Enter para continuar...")
                            continue
                    except Exception as e:
                        print(f"Erro ao buscar solicitante: {e}")
                        close_connection(conn, cursor)
                        input("\nPressione Enter para continuar...")
                        continue
                    close_connection(conn, cursor)
                
                print("\nDeixe em branco para manter o valor atual")
                nome = input(f"Novo nome [{solicitante[1]}]: ") or solicitante[1]
                dn = input(f"Nova data de nascimento (YYYY-MM-DD) [{solicitante[2]}]: ") or solicitante[2]
                nat = input(f"Nova nacionalidade [{solicitante[3]}]: ") or solicitante[3]
                end = input(f"Novo endereço [{solicitante[4]}]: ") or solicitante[4]
                contato = input(f"Novo contato [{solicitante[5]}]: ") or solicitante[5]
                idp = input(f"Novo ID passaporte [{solicitante[6]}]: ") or solicitante[6]
                
                if update_solicitante(id_sol, nome, dn, nat, end, contato, idp):
                    print("\nSolicitante atualizado com sucesso!")
                else:
                    print("\nFalha ao atualizar solicitante.")
                input("\nPressione Enter para continuar...")
                
            elif opcao == '4':
                limpar_tela()
                exibir_cabecalho()
                print("\n=== EXCLUIR SOLICITANTE ===\n")
                id_sol = input("ID do solicitante a ser excluído: ")
                
                conn = get_connection()
                if conn:
                    cursor = conn.cursor()
                    try:
                        cursor.execute("SELECT * FROM solicitante WHERE id_solicitante=%s", (id_sol,))
                        solicitante = cursor.fetchone()
                        if not solicitante:
                            print("Solicitante não encontrado!")
                            close_connection(conn, cursor)
                            input("\nPressione Enter para continuar...")
                            continue
                        else:
                            print(f"\nDados do solicitante a ser excluído:")
                            print(f"ID: {solicitante[0]}")
                            print(f"Nome: {solicitante[1]}")
                            print(f"Data de Nascimento: {solicitante[2]}")
                    except Exception as e:
                        print(f"Erro ao buscar solicitante: {e}")
                        close_connection(conn, cursor)
                        input("\nPressione Enter para continuar...")
                        continue
                    close_connection(conn, cursor)
                
                conn = get_connection()
                if conn:
                    cursor = conn.cursor()
                    try:
                        cursor.execute("SELECT COUNT(*) FROM visto WHERE id_solicitante=%s", (id_sol,))
                        count_vistos = cursor.fetchone()[0]
                        if count_vistos > 0:
                            print(f"\nATENÇÃO: Este solicitante possui {count_vistos} visto(s) associado(s).")
                            print("Excluir este solicitante pode causar problemas de integridade referencial.")
                    except Exception as e:
                        print(f"Erro ao verificar vistos associados: {e}")
                    finally:
                        close_connection(conn, cursor)
                
                confirm = input(f"\nTem certeza que deseja excluir o solicitante ID {id_sol}? (s/n): ")
                if confirm.lower() != 's':
                    print("Operação cancelada.")
                    input("\nPressione Enter para continuar...")
                    continue
                    
                if delete_solicitante(id_sol):
                    print("Solicitante excluído com sucesso!")
                else:
                    print("Falha ao excluir solicitante. Verifique se não há registros dependentes.")
                input("\nPressione Enter para continuar...")
        
        elif escolha == '3':
            opcao = submenu("MENU VISTO", [
                "Inserir Novo Visto",
                "Listar Todos os Vistos",
                "Atualizar Visto",
                "Excluir Visto"
            ])
            
            if opcao == '1':
                limpar_tela()
                exibir_cabecalho()
                print("\n=== INSERIR NOVO VISTO ===\n")
                tipo = input("Tipo de visto: ")
                ds = input("Data de solicitação (YYYY-MM-DD): ")
                status = input("Status: ")
                idsol = input("ID do solicitante: ")
                vid = create_visto(tipo, ds, status, idsol)
                if vid:
                    print(f"\nVisto inserido com sucesso! ID: {vid}")
                else:
                    print("\nFalha ao inserir visto.")
                input("\nPressione Enter para continuar...")
                
            elif opcao == '2':
                limpar_tela()
                exibir_cabecalho()
                print("\n=== LISTAR TODOS OS VISTOS ===\n")
                vistos = read_all_vistos()
                if vistos:
                    for v in vistos:
                        print(f"ID: {v[0]}, Tipo: {v[1]}, Data Solicitação: {v[2]}, Status: {v[3]}, ID Solicitante: {v[4]}")
                else:
                    print("Nenhum visto encontrado.")
                input("\nPressione Enter para continuar...")
                
            elif opcao == '3':
                limpar_tela()
                exibir_cabecalho()
                print("\n=== ATUALIZAR VISTO ===\n")
                id_vis = input("ID do visto a ser atualizado: ")
                
                conn = get_connection()
                if conn:
                    cursor = conn.cursor()
                    try:
                        cursor.execute("SELECT * FROM visto WHERE id_visto=%s", (id_vis,))
                        visto = cursor.fetchone()
                        if visto:
                            print(f"\nDados atuais:")
                            print(f"ID: {visto[0]}")
                            print(f"Tipo: {visto[1]}")
                            print(f"Data de Solicitação: {visto[2]}")
                            print(f"Status: {visto[3]}")
                            print(f"ID Solicitante: {visto[4]}")
                        else:
                            print("Visto não encontrado!")
                            close_connection(conn, cursor)
                            input("\nPressione Enter para continuar...")
                            continue
                    except Exception as e:
                        print(f"Erro ao buscar visto: {e}")
                        close_connection(conn, cursor)
                        input("\nPressione Enter para continuar...")
                        continue
                    close_connection(conn, cursor)
                
                print("\nDeixe em branco para manter o valor atual")
                tipo = input(f"Novo tipo de visto [{visto[1]}]: ") or visto[1]
                ds = input(f"Nova data de solicitação (YYYY-MM-DD) [{visto[2]}]: ") or visto[2]
                status = input(f"Novo status [{visto[3]}]: ") or visto[3]
                idsol = input(f"Novo ID solicitante [{visto[4]}]: ") or visto[4]
                
                if update_visto(id_vis, tipo, ds, status, idsol):
                    print("\nVisto atualizado com sucesso!")
                else:
                    print("\nFalha ao atualizar visto.")
                input("\nPressione Enter para continuar...")
                
            elif opcao == '4':
                limpar_tela()
                exibir_cabecalho()
                print("\n=== EXCLUIR VISTO ===\n")
                id_vis = input("ID do visto a ser excluído: ")
                
                conn = get_connection()
                if conn:
                    cursor = conn.cursor()
                    try:
                        cursor.execute("SELECT * FROM visto WHERE id_visto=%s", (id_vis,))
                        visto = cursor.fetchone()
                        if not visto:
                            print("Visto não encontrado!")
                            close_connection(conn, cursor)
                            input("\nPressione Enter para continuar...")
                            continue
                        else:
                            print(f"\nDados do visto a ser excluído:")
                            print(f"ID: {visto[0]}")
                            print(f"Tipo: {visto[1]}")
                            print(f"Data de Solicitação: {visto[2]}")
                            print(f"Status: {visto[3]}")
                    except Exception as e:
                        print(f"Erro ao buscar visto: {e}")
                        close_connection(conn, cursor)
                        input("\nPressione Enter para continuar...")
                        continue
                    close_connection(conn, cursor)
                
                conn = get_connection()
                if conn:
                    cursor = conn.cursor()
                    try:
                        cursor.execute("SELECT COUNT(*) FROM entrevista WHERE id_visto=%s", (id_vis,))
                        count_entrevistas = cursor.fetchone()[0]
                        if count_entrevistas > 0:
                            print(f"\nATENÇÃO: Este visto possui {count_entrevistas} entrevista(s) associada(s).")
                            print("Excluir este visto pode causar problemas de integridade referencial.")
                    except Exception as e:
                        print(f"Erro ao verificar entrevistas associadas: {e}")
                    finally:
                        close_connection(conn, cursor)
                
                confirm = input(f"\nTem certeza que deseja excluir o visto ID {id_vis}? (s/n): ")
                if confirm.lower() != 's':
                    print("Operação cancelada.")
                    input("\nPressione Enter para continuar...")
                    continue
                    
                if delete_visto(id_vis):
                    print("Visto excluído com sucesso!")
                else:
                    print("Falha ao excluir visto. Verifique se não há registros dependentes.")
                input("\nPressione Enter para continuar...")
        
        elif escolha == '4':
            opcao = submenu("MENU ENTREVISTA", [
                "Inserir Nova Entrevista",
                "Listar Todas as Entrevistas",
                "Atualizar Entrevista",
                "Excluir Entrevista"
            ])
            
            if opcao == '1':
                limpar_tela()
                exibir_cabecalho()
                print("\n=== INSERIR NOVA ENTREVISTA ===\n")
                dh = input("Data e hora (YYYY-MM-DD HH:MM:SS): ")
                local = input("Local: ")
                obs = input("Observações: ")
                idv = input("ID do visto: ")
                eid = create_entrevista(dh, local, obs, idv)
                if eid:
                    print(f"\nEntrevista inserida com sucesso! ID: {eid}")
                else:
                    print("\nFalha ao inserir entrevista.")
                input("\nPressione Enter para continuar...")
                
            elif opcao == '2':
                limpar_tela()
                exibir_cabecalho()
                print("\n=== LISTAR TODAS AS ENTREVISTAS ===\n")
                entrevistas = read_all_entrevistas()
                if entrevistas:
                    for e in entrevistas:
                        print(f"ID: {e[0]}, Data/Hora: {e[1]}, Local: {e[2]}, Observações: {e[3]}, ID Visto: {e[4]}")
                else:
                    print("Nenhuma entrevista encontrada.")
                input("\nPressione Enter para continuar...")
                
            elif opcao == '3':
                limpar_tela()
                exibir_cabecalho()
                print("\n=== ATUALIZAR ENTREVISTA ===\n")
                id_ent = input("ID da entrevista a ser atualizada: ")
                
                conn = get_connection()
                if conn:
                    cursor = conn.cursor()
                    try:
                        cursor.execute("SELECT * FROM entrevista WHERE id_entrevista=%s", (id_ent,))
                        entrevista = cursor.fetchone()
                        if entrevista:
                            print(f"\nDados atuais:")
                            print(f"ID: {entrevista[0]}")
                            print(f"Data/Hora: {entrevista[1]}")
                            print(f"Local: {entrevista[2]}")
                            print(f"Observações: {entrevista[3]}")
                            print(f"ID Visto: {entrevista[4]}")
                        else:
                            print("Entrevista não encontrada!")
                            close_connection(conn, cursor)
                            input("\nPressione Enter para continuar...")
                            continue
                    except Exception as e:
                        print(f"Erro ao buscar entrevista: {e}")
                        close_connection(conn, cursor)
                        input("\nPressione Enter para continuar...")
                        continue
                    close_connection(conn, cursor)
                
                print("\nDeixe em branco para manter o valor atual")
                dh = input(f"Nova data/hora (YYYY-MM-DD HH:MM:SS) [{entrevista[1]}]: ") or entrevista[1]
                local = input(f"Novo local [{entrevista[2]}]: ") or entrevista[2]
                obs = input(f"Novas observações [{entrevista[3]}]: ") or entrevista[3]
                idv = input(f"Novo ID visto [{entrevista[4]}]: ") or entrevista[4]
                
                if update_entrevista(id_ent, dh, local, obs, idv):
                    print("\nEntrevista atualizada com sucesso!")
                else:
                    print("\nFalha ao atualizar entrevista.")
                input("\nPressione Enter para continuar...")
                
            elif opcao == '4':
                limpar_tela()
                exibir_cabecalho()
                print("\n=== EXCLUIR ENTREVISTA ===\n")
                id_ent = input("ID da entrevista a ser excluída: ")
                
                conn = get_connection()
                if conn:
                    cursor = conn.cursor()
                    try:
                        cursor.execute("SELECT * FROM entrevista WHERE id_entrevista=%s", (id_ent,))
                        entrevista = cursor.fetchone()
                        if not entrevista:
                            print("Entrevista não encontrada!")
                            close_connection(conn, cursor)
                            input("\nPressione Enter para continuar...")
                            continue
                        else:
                            print(f"\nDados da entrevista a ser excluída:")
                            print(f"ID: {entrevista[0]}")
                            print(f"Data/Hora: {entrevista[1]}")
                            print(f"Local: {entrevista[2]}")
                            print(f"Observações: {entrevista[3]}")
                    except Exception as e:
                        print(f"Erro ao buscar entrevista: {e}")
                        close_connection(conn, cursor)
                        input("\nPressione Enter para continuar...")
                        continue
                    close_connection(conn, cursor)
                
                if delete_entrevista(id_ent):
                    print("Entrevista excluída com sucesso!")
                else:
                    print("Falha ao excluir entrevista. Verifique se não há registros dependentes.")
                input("\nPressione Enter para continuar...")
        
        elif escolha == '5':
            opcao = submenu("MENU FUNCIONÁRIO", [
                "Inserir Novo Funcionário",
                "Listar Todos os Funcionários",
                "Atualizar Funcionário",
                "Excluir Funcionário"
            ])
            
            if opcao == '1':
                limpar_tela()
                exibir_cabecalho()
                print("\n=== INSERIR NOVO FUNCIONÁRIO ===\n")
                nome = input("Nome: ")
                cargo = input("Cargo: ")
                dep = input("Departamento: ")
                contato = input("Contato: ")
                salario = input("Salário (ex: 2500.00): ")
                fid = create_funcionario(nome, cargo, dep, contato, salario)
                if fid:
                    print(f"\nFuncionário inserido com sucesso! ID: {fid}")
                else:
                    print("\nFalha ao inserir funcionário.")
                input("\nPressione Enter para continuar...")
                
            elif opcao == '2':
                limpar_tela()
                exibir_cabecalho()
                print("\n=== LISTAR TODOS OS FUNCIONÁRIOS ===\n")
                funcionarios = read_all_funcionarios()
                if funcionarios:
                    for f in funcionarios:
                        print(f"ID: {f[0]}, Nome: {f[1]}, Cargo: {f[2]}, Departamento: {f[3]}, Contato: {f[4]}, Salário: {f[5]}")
                else:
                    print("Nenhum funcionário encontrado.")
                input("\nPressione Enter para continuar...")
                
            elif opcao == '3':
                limpar_tela()
                exibir_cabecalho()
                print("\n=== ATUALIZAR FUNCIONÁRIO ===\n")
                id_func = input("ID do funcionário a ser atualizado: ")
                
                conn = get_connection()
                if conn:
                    cursor = conn.cursor()
                    try:
                        cursor.execute("SELECT * FROM funcionario WHERE id_funcionario=%s", (id_func,))
                        funcionario = cursor.fetchone()
                        if funcionario:
                            print(f"\nDados atuais:")
                            print(f"ID: {funcionario[0]}")
                            print(f"Nome: {funcionario[1]}")
                            print(f"Cargo: {funcionario[2]}")
                            print(f"Departamento: {funcionario[3]}")
                            print(f"Contato: {funcionario[4]}")
                            print(f"Salário: {funcionario[5]}")
                        else:
                            print("Funcionário não encontrado!")
                            close_connection(conn, cursor)
                            input("\nPressione Enter para continuar...")
                            continue
                    except Exception as e:
                        print(f"Erro ao buscar funcionário: {e}")
                        close_connection(conn, cursor)
                        input("\nPressione Enter para continuar...")
                        continue
                    close_connection(conn, cursor)
                
                print("\nDeixe em branco para manter o valor atual")
                nome = input(f"Novo nome [{funcionario[1]}]: ") or funcionario[1]
                cargo = input(f"Novo cargo [{funcionario[2]}]: ") or funcionario[2]
                departamento = input(f"Novo departamento [{funcionario[3]}]: ") or funcionario[3]
                contato = input(f"Novo contato [{funcionario[4]}]: ") or funcionario[4]
                salario = input(f"Novo salário [{funcionario[5]}]: ") or funcionario[5]
                
                try:
                    salario = float(salario)
                except ValueError:
                    print("Salário inválido! Usando valor anterior.")
                    salario = funcionario[5]
                
                if update_funcionario(id_func, nome, cargo, departamento, contato, salario):
                    print("\nFuncionário atualizado com sucesso!")
                else:
                    print("\nFalha ao atualizar funcionário.")
                input("\nPressione Enter para continuar...")
                
            elif opcao == '4':
                limpar_tela()
                exibir_cabecalho()
                print("\n=== EXCLUIR FUNCIONÁRIO ===\n")
                id_func = input("ID do funcionário a ser excluído: ")
                
                confirm = input(f"Tem certeza que deseja excluir o funcionário ID {id_func}? (s/n): ")
                if confirm.lower() != 's':
                    print("Operação cancelada.")
                    input("\nPressione Enter para continuar...")
                    continue
                    
                if delete_funcionario(id_func):
                    print("Funcionário excluído com sucesso!")
                else:
                    print("Falha ao excluir funcionário.")
                input("\nPressione Enter para continuar...")
        
        elif escolha == '6':
            opcao = submenu("MENU UTILITÁRIOS", [
                "Exemplos de JOINs"
            ])
            
            if opcao == '1':
                exemplos_joins()
        
        elif escolha == '0':
            limpar_tela()
            exibir_cabecalho()
            print("\nObrigado por utilizar o Sistema Consular!\n")
            exibir_rodape()
            sys.exit(0)
        
        else:
            input("\nOpção inválida! Pressione Enter para continuar...")

if __name__ == '__main__':
    main_loop()