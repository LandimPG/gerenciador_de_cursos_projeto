import os
import sys

from src.gerenciadores import gerenciador_sistema

class MenuCli:
    def __init__(self,sistema):
        self.sistema = sistema

    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def exibir_menu(self):
        print("\n=== GESTÃO ACADÊMICA ===")
        print("1. Cadastrar Curso")
        print("2. Cadastrar Aluno")
        print("3. Abrir Turma")
        print("4. Realizar Matrícula")
        print("5. Lançar Notas")
        print("6. Lançar Frequência")
        print("7. Relatórios Gerais")
        print("8. Trancar Matrícula")
        print("9. Calcular Situação do Aluno.")
        print("0. Sair e Salvar")

    def iniciar(self):
        """
        Loop inicial do programa
        """
        while True:
            self.exibir_menu()
            opcao = input("Opção: ")

            if opcao == '1': self.tela_cadastrar_curso()
            elif opcao == '2': self.tela_cadastrar_aluno()
            elif opcao == '3': self.tela_nova_turma()
            elif opcao == '4': self.tela_matricular()
            elif opcao == '5': self.tela_lancar_notas()
            elif opcao == '6': self.tela_lancar_frequencia()
            elif opcao == '7': self.tela_relatorios()
            elif opcao == '8': self.tela_trancar_matricula()
            elif opcao == '9': self.tela_calcular_situacao()
            elif opcao == '0':
                print("Salvando dados.")
                self.sistema.salvar_tudo()
                print("Saindo do sistema!")
                break
            else:
                print("Opção inválida.")


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

        except ValueError as e:
            print(f"Erro: {e}")

        
    def tela_lancar_frequencia(self):
        print("\n---- Lançar Frequência ----")

        try:
            cod_aluno = int(input("Matrícula do aluno: "))
            cod_turma = int(input("ID da Turma: "))
            frequencia = float(input("Frequência (0 - 100): "))

            self.sistema.processar_frequencia(cod_aluno, cod_turma, frequencia)

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
            