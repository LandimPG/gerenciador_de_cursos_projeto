import os
import sys

from src.gerenciadores import gerenciador_sistema


class Cores:
    RESET = "\033[0m"      # Retorna à cor padrão
    VERMELHO = "\033[91m"  # Para erros
    VERDE = "\033[92m"     # Para sucesso
    AMARELO = "\033[93m"   # Para alertas ou inputs
    AZUL = "\033[94m"      # Para informações
    MAGENTA = "\033[95m"   # Para títulos
    CIANO = "\033[96m"     # Para tabelas/bordas
    NEGRITO = "\033[1m"    # Para destaque extra

class MenuCli:
    def __init__(self,sistema):
        self.sistema = sistema

    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def _ler_input_inteiro(self, mensagem, obrigatorio=True):
        mensagem_colorida = f"{Cores.AMARELO}{mensagem}{Cores.RESET}"
        entrada = input(mensagem_colorida).strip()
        
        # Se for obrigatório e estiver vazio
        if obrigatorio and not entrada:
            raise ValueError("Este campo é obrigatório e não pode ficar vazio.")
        
        # Se não for obrigatório e estiver vazio (ex: editar, deixar em branco)
        if not obrigatorio and not entrada:
            return None 

        # Tenta converter
        if not entrada.lstrip('-').isdigit(): # lstrip permite números negativos se precisar
             raise ValueError(f"Entrada inválida: '{entrada}'. Por favor, digite apenas números inteiros.")
        
        return int(entrada)

    def _ler_input_float(self, mensagem):
        mensagem_colorida = f"{Cores.AMARELO}{mensagem}{Cores.RESET}"
        entrada = input(mensagem_colorida).strip()
        if not entrada:
             raise ValueError("Este campo é obrigatório.")
        try:
            return float(entrada)
        except ValueError:
            raise ValueError(f"Entrada inválida: '{entrada}'. Digite um número decimal (ex: 8.5).")

    def iniciar(self):
        """
        Loop inicial do programa
        """
        while True:

            print("\n=== SISTEMA DE GESTÃO ACADÊMICA ===")
            print("1. Gestão de Cursos.")
            print("2. Gestão de Alunos.")
            print("3. Gestão de Turmas.")
            print("4. Gestão de Matrículas.")
            print("5. Relatórios e Estatísticas.")
            print("0. Sair e Salvar")
            
            opcao = input("Opção: ")

            if opcao == '1': self.menu_cursos()
            elif opcao == '2': self.menu_alunos()
            elif opcao == '3': self.menu_turmas()
            elif opcao == '4': self.menu_matriculas()
            elif opcao == '5': self.menu_relatorios()
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
            print("4. Editar Aluno")
            print("0. Voltar")
            
            op = input("Opção: ")
            if op == '1': self.tela_cadastrar_aluno()
            elif op == '2': self.tela_listar_alunos()
            elif op == '3': self.tela_excluir_aluno()
            elif op == '4': self.tela_editar_aluno()
            elif op == '0': break

            else:
                print("Opção inválida.")


    def menu_turmas(self): #TURMA
        while True:
            print("\n--- GESTÃO DE TURMAS---")
            print("1. Abrir Nova Turma")
            print("2. Listar Turmas")
            print("3. Editar Turmas (local / vagas)")
            print("4. Fechar/Reabrir Turma")
            print("5. Excluir Turma")
            print("0. Voltar")

            op = input("Opção: ")
            if op == '1': self.tela_nova_turma()
            elif op == '2': self.tela_listar_turmas()
            elif op == '3': self.tela_editar_turma()
            elif op == '4': self.tela_alterar_estado_turma()
            elif op == '5': self.tela_excluir_turma()
            elif op == '0': break

            else:
                print("Opção inválida.")

    def menu_matriculas(self): #MATRICULA
        while True:
            print("\n--- GESTÃO DE MATRÍCULAS ---")
            print("1. Matricular Aluno")
            print("2. Trancar Matrícula")
            print("3. Lançar Notas")
            print("4. Lançar Frequência")
            print("5. Calcular Situação Final")
            print("0. Voltar")

            op = input("Opção: ")
            if op == '1': self.tela_matricular()
            elif op == '2': self.tela_trancar_matricula()
            elif op == '3': self.tela_lancar_notas()
            elif op == '4': self.tela_lancar_frequencia()
            elif op == '5': self.tela_calcular_situacao()
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
            print(f"{'ID':<5} | {'Nome':<30} | {'Horas':<6} | {'Pré-Requisitos'}")
            print("-" * 70)
            for c in self.sistema.cursos:

                pre_req_texto = str(c.lista_pre_requisitos) if c.lista_pre_requisitos else "-"
                print(f"{c.codigo_curso:<5} | {c.nome:<30} | {c.carga_horaria:<6} | {pre_req_texto}")

    def tela_listar_alunos(self):
        print("\n--- Lista de Alunos ---")
        if not self.sistema.alunos:
            print("Nenhum aluno foi cadastrado.")
        else:
            for a in self.sistema.alunos:
                print(f"Matrícula: {a.codigo_matricula} | Nome: {a.nome}")

        
    def tela_excluir_curso(self):
        try:

            cod = int(input("ID do curso para excluir: "))
            self.sistema.remover_curso(cod)
            print("Curso removido com sucesso.")

        except ValueError as e:
            print(f"Erro: {e}")

    def tela_editar_curso(self):
        try:
            cod = self._ler_input_inteiro("ID do curso para editar: ")

            curso = self.sistema.buscar_curso(cod)
            if not curso:
                print("Curso não encontrado.")
                return
            
            print(f"--- Editando: {curso.nome} ---")
            print("Pressione [Enter] vazio para manter o valor atual.")

            #Nome
            print(f"Nome atual: {curso.nome}")
            novo_nome = input("Novo nome: ").strip()

            #Carga Horária
            print(f"Carga Horária atual: {curso.carga_horaria}h")
            nova_carga = self._ler_input_inteiro("Nova carga horária: ", obrigatorio=False)

            #Pré-requisitos 
            print(f"Pré-requisitos atuais: {curso.lista_pre_requisitos}")
            entrada_req = input("Novos IDs (sep. por vírgula) ou 'limpar' p/ remover todos: ").strip()


            #Tratando dos dados
            nome_enviar = novo_nome if novo_nome else None
            carga_enviar = int(nova_carga) if nova_carga else None

            lista_requisitos_enviar = None

            if entrada_req:

                if entrada_req.lower() == "limpar":
                    lista_requisitos_enviar = [] # Envia lista vazia para apagar tudo
                else:
                    try:
                        # Converte string "1, 2" em lista [1, 2]
                        lista_requisitos_enviar = [int(x.strip()) for x in entrada_req.split(",")]
                    except ValueError:
                        print("Erro: Digite apenas números separados por vírgula.")
                        return

            self.sistema.editar_curso(cod, nome_enviar, carga_enviar, lista_requisitos_enviar)

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

    def tela_editar_aluno(self):
        print("\n---- Editar Aluno ----")
        try:
            matricula_atual = self._ler_input_inteiro("Matrícula do aluno a editar: ")
            
            # Busca apenas para mostrar os dados atuais 
            aluno = self.sistema.buscar_aluno(matricula_atual)
            if not aluno:
                print("Aluno não encontrado.")
                return

            print(f"--- Editando: {aluno.nome} ---")
            print("Pressione [Enter] vazio para manter o valor atual.")

            # Coleta Nome
            print(f"Nome atual: {aluno.nome}")
            novo_nome = input("Novo nome: ").strip()

            # Coleta Email
            print(f"Email atual: {aluno.email}")
            novo_email = input("Novo email: ").strip()

            #Coleta Nova Matrícula
            print(f"Matrícula atual: {aluno.codigo_matricula}")
            nova_mat_str = input("Nova matrícula (Cuidado ao alterar): ").strip()

            # Tratamento
            nome_enviar = novo_nome if novo_nome else None
            email_enviar = novo_email if novo_email else None
            
            # Se digitou algo na matrícula, converte para int, senão manda None
            nova_mat_enviar = int(nova_mat_str) if nova_mat_str else None

            # Chama o gerenciador
            self.sistema.editar_aluno(matricula_atual, nome_enviar, email_enviar, nova_mat_enviar)
            
            print("Aluno atualizado com sucesso!")

        except ValueError as e:
            print(f"Erro: {e}")

# Telas de turma
    def tela_listar_turmas(self):

        print("\n--- Turmas Cadastradas ---")
        if not self.sistema.turmas:
            print("Nenhuma turma cadastrada.")
            return

        print(f"{'ID':<5} | {'Curso Nome':<15} | {'Semestre':<8} | {'Local':<6} | {'Ocupação':<10} | {'Status'}")
        print("-" * 75)
        
        for t in self.sistema.turmas:
            # Busca o nome do curso na hora de imprimir
            curso = self.sistema.buscar_curso(t.codigo_curso)
            nome_curso = curso.nome if curso else "Curso Desconhecido"
            # Trunca o nome se for muito longo para não quebrar a tabela
            nome_curso = (nome_curso[:22] + '..') if len(nome_curso) > 22 else nome_curso

            status = "ABERTA" if t.estado_aberta else "FECHADA"
            ocupacao = f"{len(t)}/{t.vagas_totais}"
            
            print(f"{t.codigo_turma:<5} | {nome_curso:<25} | {t.semestre:<8} | {ocupacao:<8} | {status}")

    def tela_editar_turma(self):
        try:
            cod = int(input("ID da Turma para editar: "))
            turma = self.sistema.buscar_turma(cod)
            if not turma:
                print("Turma não encontrada.")
                return

            print(f"Editando Turma {cod} (Semestre {turma.semestre})")
            print(f"Local atual: {turma.local} | Vagas: {turma.vagas_totais}")
            print("Deixe vazio para manter o atual.")

            novo_local = input("Novo Local (ex: B05): ").strip()
            novas_vagas_str = input("Nova Qtd Vagas: ").strip()

            local_enviar = novo_local if novo_local else None
            vagas_enviar = int(novas_vagas_str) if novas_vagas_str else None

            self.sistema.editar_turma(cod, local_enviar, vagas_enviar)
            print("Turma atualizada!")

        except ValueError as e:
            print(f"Erro: {e}")


    def tela_alterar_estado_turma(self):

        try:
            cod = self._ler_input_inteiro("ID da Turma: ")
            turma = self.sistema.buscar_turma(cod)
            if not turma:
                print("Turma não encontrada.")
                return

            status_atual = "ABERTA" if turma.estado_aberta else "FECHADA"
            print(f"Estado atual: {status_atual}")
            
            acao = input("Digite [A] para abrir ou [F] para fechar a turma: ").strip().lower()
            
            if acao == 'a':
                self.sistema.alterar_estado_turma(cod, 'abrir')
            elif acao == 'f':
                self.sistema.alterar_estado_turma(cod, 'fechar')
            else:
                print("Opção inválida.")

        except ValueError as e:
            print(f"Erro: {e}")

    def tela_excluir_turma(self):
        try:
            cod = int(input("ID da turma para excluir: "))
            self.sistema.excluir_turma(cod)
            print("Turma excluída com sucesso.")
        except ValueError as e:
            print(f"Erro: {e}")

#   Métodos de Tela
    def tela_cadastrar_curso(self):
        print("---- Novo Curso ----")
        try:
            nome = input("Nome do curso: ")
            codigo = self._ler_input_inteiro("Código(ID): ")
            horas = self._ler_input_inteiro("Carga Horária: ")

            ementa = input("Ementa: ")

            print("Pré-requisitos (Digite os IDs separados por vírgula ou Enter para nenhum):")
            entrada_req = input("IDs: ")

            lista_req = []
            if entrada_req.strip():

                try:
                    lista_req = [int(x.strip()) for x in entrada_req.split(",")]
                except ValueError:
                    raise ValueError("Os pré-requisitos devem ser números separados por vírgula.")

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

        print("\n[Passo 1] Escolha o Aluno:")
        self.tela_listar_alunos()

        try:
            cod_aluno_entrada = input(">> Digite a Matrícula do Aluno (ou Enter para sair): ")
            if not cod_aluno_entrada: return
            cod_aluno = int(cod_aluno_entrada)

            print("\n[Passo 2] Escolha a Turma:")
            self.tela_listar_turmas()

            cod_turma = int(input("ID da turma: "))


            nova_matricula = self.sistema.realizar_matricula(cod_aluno, cod_turma)

            
            id_curso = nova_matricula.turma.codigo_curso
            curso = self.sistema.buscar_curso(id_curso)
            nome_curso = curso.nome if curso else "Curso desconhecido"
            curso_nome = nova_matricula.turma.curso.nome if hasattr(nova_matricula.turma, 'curso') else "Disciplina"
            print(f"\nSucesso! {nova_matricula.aluno.nome} matriculado em {curso_nome}.")

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
            cod_aluno = self._ler_input_inteiro("Matrícula do Aluno: ")
            cod_turma = self._ler_input_inteiro("ID da Turma: ")

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
        