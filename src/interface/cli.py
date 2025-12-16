import os
import sys

from src.gerenciadores import gerenciador_sistema

class MenuCli:
    def __init__(self,sistema):
        self.sistema = sistema

    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def iniciar(self):
        """
        Loop inicial do programa
        """
        while True:

            print("\n=== SISTEMA DE GESTÃO ACADÊMICA ===")
            print("1. Gestão de Cursos.")
            print("2. Gestão de Alunos.")
            print("3. Gestão de Turmas e Matrículas.")
            print("4. Relatórios e Estatísticas.")
            print("0. Sair e Salvar")
            
            opcao = input("Opção: ")

            if opcao == '1': self.menu_cursos()
            elif opcao == '2': self.menu_alunos()
            elif opcao == '3': self.menu_turmas()
            elif opcao == '4': self.menu_relatorios()
            elif opcao == '0':
                print("Salvando dados.")
                self.sistema.salvar_tudo()
                print("Saindo do sistema!")
                break
            else:
                print("Opção inválida.")

    def menu_cursos(self):
        while True:
            print("\n--- GESTÃO DE CURSOS ---")
            print("1. Criar Novo Curso")
            print("2. Listar Cursos")
            print("3. Editar Curso")
            print("4. Excluir Curso")
            print("0. Voltar")
            
            opcao = input("Opção: ")
            if opcao == '1': self.tela_cadastrar_curso()
            elif opcao == '2': self.tela_listar_cursos()
            elif opcao == '3': self.tela_editar_curso()
            elif opcao == '4': self.tela_excluir_curso()
            elif opcao == '0': break

            else:
                print("Opção inválida.")

    def menu_alunos(self):
        while True:
            print("\n--- GESTÃO DE ALUNOS ---")
            print("1. Cadastrar Aluno")
            print("2. Listar Alunos") # criar esse método depois
            print("3. Excluir Aluno")
            print("0. Voltar")
            
            op = input("Opção: ")
            if op == '1': self.tela_cadastrar_aluno()
            elif op == '2': self.tela_listar_alunos()
            elif op == '3': self.tela_excluir_aluno()
            elif op == '0': break

            else:
                print("Opção inválida.")


    def menu_turmas(self):
        while True:
            print("\n--- TURMAS E MATRÍCULAS ---")
            print("1. Abrir Nova Turma")
            print("2. Matricular Aluno")
            print("3. Trancar Matrícula")
            print("4. Lançar Notas")
            print("5. Lançar Frequência")
            print("6. Calcular Situação Final")
            print("0. Voltar")

            op = input("Opção: ")
            if op == '1': self.tela_nova_turma()
            elif op == '2': self.tela_matricular()
            elif op == '3': self.tela_trancar_matricula()
            elif op == '4': self.tela_lancar_notas()
            elif op == '5': self.tela_lancar_frequencia()
            elif op == '6': self.tela_calcular_situacao()
            elif op == '0': break

            else:
                print("Opção inválida.")

    def menu_relatorios(self):
        while True:
            print("\n--- RELATÓRIOS ---")
            print("1. Relatório Geral (Por Turma)")
            print("2. Alunos em Risco")
            print("3. Top Melhores Alunos (CR)")
            print("0. Voltar")

            op = input("Opção: ")
            if op == '1': self.tela_relatorios() # O antigo tela_relatorios
            elif op == '2': self.tela_alunos_risco()
            elif op == '3': self.tela_top_alunos()
            elif op == '0': break

            else:
                print("Opção inválida.")

#Métodos de tela CRUD

    def tela_listar_cursos(self):
        print("\n--- Lista de Cursos ---")
        if not self.sistema.cursos:
            print("Nenhum curso cadastrado.")
        else:
            print(f"{'ID':<5} | {'Nome':<30} | {'Horas':<5}")
            print("-" * 45)
            for c in self.sistema.cursos:
                print(f"{c.codigo_curso:<5} | {c.nome:<30} | {c.carga_horaria}h")

    def tela_listar_alunos(self):
        print("\n--- Lista de Alunos ---")
        if not self.sistema.alunos:
            print("Nenhum aluno foi cadastrado.")
        else:
            for a in self.sistema.alunos:
                print(f"Matr: {a.codigo_matricula} | Nome: {a.nome}")

        
    def tela_excluir_curso(self):
        try:

            cod = int(input("ID do curso para excluir: "))
            self.sistema.remover_curso(cod)
            print("Curso removido com sucesso.")

        except ValueError as e:
            print(f"Erro: {e}")

    def tela_editar_curso(self):
        try:
            cod = int(input("ID do curso para editar: "))

            curso = self.sistema.buscar_curso(cod)
            if not curso:
                print("Curso não encontrado.")
                return
            
            print(f"Editando: {curso.nome} (Deixe em branco para manter)")
            novo_nome = input("Novo nome: ").strip()
            nova_carga = input("Nova carga horária: ").strip()
            nome_para_enviar = novo_nome if novo_nome else None
            carga_para_enviar = int(nova_carga) if nova_carga else None

            self.sistema.editar_curso(cod, nome_para_enviar, carga_para_enviar)

            print("Curso atualizado com sucesso!")

        except ValueError as e:
            print(f"Erro: {e}")

    def tela_excluir_aluno(self):
        try:
            matricula = int(input("Matrícula do aluno para excluir: "))
            self.sistema.remover_aluno(matricula)
            print("aluno removido com sucesso")
        
        except ValueError as e:
            print(f"Erro: {e}")

#   Métodos de Tela
    def tela_cadastrar_curso(self):
        print("---- Novo Curso ----")
        try:
            nome = input("Nome do curso: ")
            codigo = int(input("Código(ID): "))
            horas = int(input("Carga Horária: "))
            ementa = input("Ementa: ")

            print("Pré-requisitos (Digite os IDs separados por vírgula ou Enter para nenhum):")
            entrada_req = input("IDs: ")

            lista_req = []
            if entrada_req.strip():

                try:
                    lista_req = [int(x.strip()) for x in entrada_req.split(",")]
                except ValueError:
                    print("Erro: digite apenas números separados por vírgula")
                    return


            self.sistema.criar_curso(nome, codigo, horas, ementa, lista_req)
            print("Curso cadastrado com sucesso!")

        except ValueError as e:
            print(f"Erro: {e}")

        except Exception as e:
            print(f"Erros inesperado.")
        
    
    def tela_cadastrar_aluno(self):
        print("\n---- Novo Aluno ----")
        try:
            nome = input("Nome: ")
            email = input("Email: ")
            matricula = int(input("Mátricula: "))

            self.sistema.criar_aluno(nome, email, matricula)
            print("Aluno cadastrado com sucesso!")

        except ValueError as e:
            print(f"Erro: {e}")
        
    def tela_nova_turma(self):
        print("\n---- Nova Turma ----")

        if not self.sistema.cursos:
            print("Nenhum curso foi cadastrado.")
            return
        print("Cursos disponíveis: ")

        for c in self.sistema.cursos:
            print(f"Nome: {c.nome} | ID: {c.codigo_curso}.")
        
        try:
            cod_curso = int(input("\nID curso: "))
            cod_turma = int(input("ID turma: "))
            vagas = int(input("Vagas totais: "))
            semestre = input("Semestre (ex: 2026.1): ")
            local = input("Local (ex: A02): ")

            print("Horário (Ex: 18:00-22:00) | Dias: seg, ter, qua...")
            dia = input("Dia: ").strip().lower()
            horario = input("Horário: ").strip()
            horarios = {dia: horario}

            self.sistema.criar_turma(cod_curso, cod_turma, vagas, semestre, local, horarios )
            print("Turma aberta com sucesso!")

        except ValueError as e:
            print(f"Erro: {e}")

    
    def tela_matricular(self):
        print("\n---- Matricular Aluno ---- ")

        try:
            cod_aluno = int(input("Matrícula do Aluno: "))
            cod_turma = int(input("ID da turma: "))
            nova_matricula = self.sistema.realizar_matricula(cod_aluno, cod_turma)
            id_curso = nova_matricula.turma.codigo_curso
            curso = self.sistema.buscar_curso(id_curso)
            nome_curso = curso.nome if curso else "Curso desconhecido"

            print(f"\nAluno: {nova_matricula.aluno.nome}")
            print(f"Matriculado com sucesso em: {nome_curso} | Id Turma: {nova_matricula.turma.codigo_turma}")

        except ValueError as e:
            print(f"Erro: {e}")

    def tela_lancar_notas(self):
        print("\n---- Lançar Notas ----")
        try:
            cod_aluno = int(input("Matrícula do aluno: "))
            cod_turma = int(input("ID da Turma: "))
            nota = float(input("Nota (0 - 10): "))

            self.sistema.processar_notas(cod_aluno, cod_turma, nota)

            print(f"Nota {nota:.2f} adicionada com sucesso.") 

        except ValueError as e:
            print(f"Erro: {e}")

        
    def tela_lancar_frequencia(self):
        print("\n---- Lançar Frequência ----")

        try:
            cod_aluno = int(input("Matrícula do aluno: "))
            cod_turma = int(input("ID da Turma: "))
            frequencia = float(input("Frequência (0 - 100): "))

            self.sistema.processar_frequencia(cod_aluno, cod_turma, frequencia)

            print(f"Frequência atualizada para {self.frequencia:.1f}% com sucesso.")

        except ValueError as e:
            print(f"Erro: {e}")


    def tela_relatorios(self):
        print("\n---- Relatórios Gerais ----")

        turmas = self.sistema.turmas

        if not turmas:
            print("Nenhuma turma foi cadastrada")
            return
        
        for turma in turmas:
            print(f"\nTurma: {turma.codigo_turma} | Disciplina ID: {turma.codigo_curso}")
            print(f"Lotação: {len(turma)} / {turma.vagas_totais}")

        #--- Lista Alunos ----
            if turma.matriculas:
                for m in turma.matriculas:
                    print(f"---- Aluno: {m.aluno.nome} | Situação: {m.estado} | Notas: {m.notas}")
            else:
                print("  --   (Sem alunos na turma.)  --  ")

        # Estatísticas Matemáticas 

            print(f"\n[Estatísticas da Turma]")

            taxa = turma.ver_taxa_aprovacao_turma()
            print(f"Taxa de Aprovação: {taxa}%")

          #Distribuição de Notas:
            status = turma.ver_distribuicao_notas()

            if status:
                print(f"--- Média da Turma: {status['media_geral']}")
                print(f"--- Melhor Média: {status['maior_nota']}")
                print(f"--- Menor Média: {status['menor_nota']}")
                print(f"--- Desvio Padrão: {status['desvio_padrao']}")
            else:
                print("\n---- Notas Insuficientes para gerar estatísticas. ----")

            print(f"{'=' * 40}")



    def tela_trancar_matricula(self):
        print("\n---- Trancar Matrícula ----")
        try:
            cod_aluno = int(input("Matrícula do aluno: "))
            cod_turma = int(input("ID da Turma: "))

            confirmacao = input("Tem certeza que deseja trancar ? (s/n): ").lower()
            if confirmacao == "s":
                self.sistema.processar_trancamento(cod_aluno, cod_turma)
                print("Matrícula trancada com sucesso.")
            else:
                print("Operação cancelada.")

        except ValueError as e:
            print(f"Erro: {e}")

    def tela_calcular_situacao(self):
        print("\n---- Calcular Situação ----")
        try:
            cod_aluno = int(input("Matrícula do Aluno: "))
            cod_turma = int(input("ID da Turma: "))

            situacao = self.sistema.ver_situacao_aluno(cod_aluno, cod_turma)

            print(f"Cálculo realizado com sucesso!")
            print(f"Nova Situação do Aluno: {situacao}")
            
            if situacao == "CURSANDO":
                print("(Atenção: O aluno continua cursando pois não atingiu critérios de aprovação/reprovação ainda)")

        except ValueError as e:
            print(f"Erro: {e}")
            
    def tela_alunos_risco(self):
        print("\n---- Relatório de Alunos em Risco ----")

        try:
            cod_turma = int(input("Código Turma: "))

            turma, lista_risco = self.sistema.relatorio_alunos_em_risco(cod_turma)

            print(f"\nAnálise de risco - TURMA: {turma.codigo_turma} | CURSO ID: {turma.codigo_curso}")

            if not lista_risco:
                print(f"Nenhum aluno está em risco nessa turma. (Todos estão com notas e frequências acima ou igual ás medias)")
            else:
                print(f"ALERTA: {len(lista_risco)} aluno(s) precisa(m) de atenção.\n")
                for item in lista_risco:
                    motivos = " e ".join(item["motivo"])
                    print(f" Nome: {item["nome"]} |Matrícula: {item["matricula"]}")
                    print(f" Motivo: {motivos}")
                    print(f"{"=" * 40}")

        except ValueError as e:
            print(f"Erro: {e}")

    def tela_top_alunos(self):
        print("\n---- Top Melhores Alunos (CR) ----")
        
        try:
            qtd_input = input("Quantos alunos deseja ver ? (Padrão 3): ")
            n = int(qtd_input) if qtd_input.strip() else 3

            if not qtd_input:
                n = 3

            elif qtd_input.isdigit():
                n = int(qtd_input)
            
            else:
                print("Entrada inválida: Usando o valor padrão de 3 alunos.")
                n = 3

            top_lista = self.sistema.relatorio_top_alunos(n)

            if not top_lista:
                print("Nenhum aluno cadastrado para gerar ranking.")
                return
        
            print(f"\nRANKING: TOP {len(top_lista)} ALUNOS")
            print(f"{'Pos':<5} | {'Nome':<20} | {'CR':<5}")
            print("-" * 35)

            for i, aluno in enumerate(top_lista, start=1):
                cr = aluno.calcular_cr()
                print(f"#{i:<4} | {aluno.nome:<20} | {cr:.2f}")
                
        except ValueError as e:
            print(f"Erro: {e}")
        