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

            print(f"\n{Cores.MAGENTA}{Cores.NEGRITO}=== SISTEMA DE GESTÃO ACADÊMICA ==={Cores.RESET}")
            print("1. Gestão de Cursos.")
            print("2. Gestão de Alunos.")
            print("3. Gestão de Turmas.")
            print("4. Gestão de Matrículas.")
            print("5. Relatórios e Estatísticas.")
            print("0. Sair e Salvar")
            
            opcao = input(f"{Cores.AMARELO}Opção: {Cores.RESET}")

            if opcao == '1': self.menu_cursos()
            elif opcao == '2': self.menu_alunos()
            elif opcao == '3': self.menu_turmas()
            elif opcao == '4': self.menu_matriculas()
            elif opcao == '5': self.menu_relatorios()
            elif opcao == '0':
                print(f"{Cores.VERDE}Salvando dados.{Cores.RESET}")
                self.sistema.salvar_tudo()
                print("Saindo do sistema!")
                break
            else:
                print(f"{Cores.VERMELHO}Opção inválida.{Cores.RESET}")

    def menu_cursos(self):
        while True:
            print(f"\n{Cores.MAGENTA}{Cores.NEGRITO}--- GESTÃO DE CURSOS ---{Cores.RESET}")
            print("1. Criar Novo Curso")
            print("2. Listar Cursos")
            print("3. Editar Curso")
            print("4. Excluir Curso")
            print("0. Voltar")
            
            opcao = input(f"{Cores.AMARELO}Opção: {Cores.RESET}")
            if opcao == '1': self.tela_cadastrar_curso()
            elif opcao == '2': self.tela_listar_cursos()
            elif opcao == '3': self.tela_editar_curso()
            elif opcao == '4': self.tela_excluir_curso()
            elif opcao == '0': break

            else:
                print("Opção inválida.")

    def menu_alunos(self):
        while True:
            print(f"\n{Cores.MAGENTA}{Cores.NEGRITO}--- GESTÃO DE ALUNOS ---{Cores.RESET}")
            print("1. Cadastrar Aluno")
            print("2. Listar Alunos") # criar esse método depois
            print("3. Excluir Aluno")
            print("4. Editar Aluno")
            print("0. Voltar")
            
            op = input(f"{Cores.AMARELO}Opção: {Cores.RESET}")
            if op == '1': self.tela_cadastrar_aluno()
            elif op == '2': self.tela_listar_alunos()
            elif op == '3': self.tela_excluir_aluno()
            elif op == '4': self.tela_editar_aluno()
            elif op == '0': break

            else:
                print("Opção inválida.")


    def menu_turmas(self): #TURMA
        while True:
            print(f"\n{Cores.MAGENTA}{Cores.NEGRITO}--- GESTÃO DE TURMAS---{Cores.RESET}")
            print("1. Abrir Nova Turma")
            print("2. Listar Turmas")
            print("3. Editar Turmas (local / vagas)")
            print("4. Fechar/Reabrir Turma")
            print("5. Excluir Turma")
            print("0. Voltar")

            op = input(f"{Cores.AMARELO}Opção: {Cores.RESET}")
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
            print(f"\n{Cores.MAGENTA}{Cores.NEGRITO}--- GESTÃO DE MATRÍCULAS ---{Cores.RESET}")
            print("1. Matricular Aluno")
            print("2. Trancar Matrícula")
            print("3. Lançar Notas")
            print("4. Lançar Frequência")
            print("5. Calcular Situação Final")
            print("0. Voltar")

            op = input(f"{Cores.AMARELO}Opção: {Cores.RESET}")
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
            print(f"\n{Cores.MAGENTA}{Cores.NEGRITO}--- RELATÓRIOS ---{Cores.RESET}")
            print("1. Relatório Geral (Por Turma)")
            print("2. Alunos em Risco")
            print("3. Top Melhores Alunos (CR)")
            print("0. Voltar")

            op = input(f"{Cores.AMARELO}Opção: {Cores.RESET}")
            if op == '1': self.tela_relatorios() # O antigo tela_relatorios
            elif op == '2': self.tela_alunos_risco()
            elif op == '3': self.tela_top_alunos()
            elif op == '0': break

            else:
                print("Opção inválida.")

#Métodos de tela CRUD

    def tela_listar_cursos(self):
        print(f"\n{Cores.MAGENTA}{Cores.NEGRITO}--- Lista de Cursos ---{Cores.RESET}")
        if not self.sistema.cursos:
            print("Nenhum curso cadastrado.")
        else:
            print(f"{Cores.CIANO}{'ID':<5} | {'Nome':<30} | {'Horas':<6} | {'Pré-Requisitos'}{Cores.RESET}")
            print("-" * 70)
            for c in self.sistema.cursos:

                pre_req_texto = str(c.lista_pre_requisitos) if c.lista_pre_requisitos else "-"
                print(f"{c.codigo_curso:<5} | {c.nome:<30} | {c.carga_horaria:<6} | {pre_req_texto}")

    def tela_listar_alunos(self):
        print(f"\n{Cores.MAGENTA}{Cores.NEGRITO}--- Lista de Alunos ---{Cores.RESET}")
        if not self.sistema.alunos:
            print("Nenhum aluno foi cadastrado.")
        else:
            for a in self.sistema.alunos:
                print(f"Matrícula: {a.codigo_matricula} | Nome: {a.nome}")

        
    def tela_excluir_curso(self):
        try:

            cod = int(input(f"{Cores.AMARELO}ID do curso para excluir: {Cores.RESET}"))
            self.sistema.remover_curso(cod)
            print("Curso removido com sucesso.")

        except ValueError as e:
            print(f"Erro: {e}")

    def tela_editar_curso(self):
        try:
            cod = self._ler_input_inteiro(f"{Cores.AMARELO}ID do curso para editar: {Cores.RESET}")

            curso = self.sistema.buscar_curso(cod)
            if not curso:
                print("Curso não encontrado.")
                return
            
            print(f"--- Editando: {curso.nome} ---")
            print("Pressione [Enter] vazio para manter o valor atual.")

            #Nome
            print(f"Nome atual: {curso.nome}")
            novo_nome = input(f"{Cores.AMARELO}Novo nome: {Cores.RESET}").strip()

            #Carga Horária
            print(f"Carga Horária atual: {curso.carga_horaria}h")
            nova_carga = self._ler_input_inteiro(f"{Cores.AMARELO}Nova carga horária: {Cores.RESET}", obrigatorio=False)

            #Pré-requisitos 
            print(f"Pré-requisitos atuais: {curso.lista_pre_requisitos}")
            entrada_req = input(f"{Cores.AMARELO}Novos IDs (sep. por vírgula) ou 'limpar' p/ remover todos: {Cores.RESET}").strip()


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
            matricula = int(input(f"{Cores.AMARELO}Matrícula do aluno para excluir: {Cores.RESET}"))
            self.sistema.remover_aluno(matricula)
            print("aluno removido com sucesso")
        
        except ValueError as e:
            print(f"Erro: {e}")

    def tela_editar_aluno(self):
        print("\n---- Editar Aluno ----")
        try:
            matricula_atual = self._ler_input_inteiro(f"{Cores.AMARELO}Matrícula do aluno a editar: {Cores.RESET}")
            
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

        print(f"\n{Cores.MAGENTA}--- Turmas Cadastradas ---{Cores.RESET}")
        if not self.sistema.turmas:
            print("Nenhuma turma cadastrada.")
            return

        print(f"{Cores.CIANO}{'ID':<5} | {'Curso Nome':<15} | {'Semestre':<8} | {'Local':<6} | {'Ocupação':<10} | {'Status'}{Cores.RESET}")
        print("-" * 75)
        
        for t in self.sistema.turmas:
            # Busca o nome do curso na hora de imprimir
            curso = self.sistema.buscar_curso(t.codigo_curso)
            nome_curso = curso.nome if curso else "Curso Desconhecido"
            # Trunca o nome se for muito longo para não quebrar a tabela
            nome_curso = (nome_curso[:22] + '..') if len(nome_curso) > 22 else nome_curso

            status_cor = Cores.VERDE if t.estado_aberta else Cores.VERMELHO
            status_texto = "ABERTA" if t.estado_aberta else "FECHADA"

            ocupacao = f"{len(t)}/{t.vagas_totais}"
            
            print(f"{t.codigo_turma:<5} | {nome_curso:<20} | {t.semestre:<8} | {t.local:<6} | {ocupacao:<10} | {status_cor}{status_texto}{Cores.RESET}")

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
            cod_curso = self._ler_input_inteiro("ID do Curso: ")
            cod_turma = self._ler_input_inteiro("ID da Nova Turma: ")
            vagas = self._ler_input_inteiro("Vagas totais: ")

            semestre = input(f"{Cores.AMARELO}Semestre (ex: 2026.1): {Cores.RESET}").strip()
            local = input(f"{Cores.AMARELO}Local (ex: A02): {Cores.RESET}").strip()

            print("Horário (Ex: 18:00-22:00) | Dias: seg, ter, qua...")
            dia = input("Dia: ").strip().lower()
            horario = input("Horário: ").strip()
            horarios = {dia: horario}

            self.sistema.criar_turma(cod_curso, cod_turma, vagas, semestre, local, horarios )
            print("Turma aberta com sucesso!")

        except ValueError as e:
            print(f"Erro: {e}")

    
    def tela_matricular(self):
        print(f"\n{Cores.MAGENTA}---- Matricular Aluno ---- {Cores.RESET}")

        print(f"\n{Cores.AZUL}[Passo 1] Escolha o Aluno:{Cores.RESET}")
        self.tela_listar_alunos()

        try:
            cod_aluno = self._ler_input_inteiro(f"{Cores.AMARELO}>> Digite a Matrícula do Aluno (ou Enter para sair): {Cores.RESET}", obrigatorio=False)

            if cod_aluno is None: 
                return # Sai se for vazio

            print(f"\n{Cores.AZUL}[Passo 2] Escolha a Turma:{Cores.RESET}")
            self.tela_listar_turmas()

            cod_turma = self._ler_input_inteiro("ID da turma: ")


            nova_matricula = self.sistema.realizar_matricula(cod_aluno, cod_turma)

            curso_nome = nova_matricula.turma.curso.nome if hasattr(nova_matricula.turma, 'curso') else "Disciplina"
            print(f"\n{Cores.VERDE}Sucesso! {nova_matricula.aluno.nome} matriculado em {curso_nome}.{Cores.RESET}")

        except ValueError as e:
            print(f"{Cores.VERMELHO}Erro: {e}{Cores.RESET}")

    def tela_lancar_notas(self):
        print(f"\n{Cores.MAGENTA}---- Lançar Notas ----{Cores.RESET}")
        try:
            cod_aluno = self._ler_input_inteiro("Matrícula do aluno: ")
            cod_turma = self._ler_input_inteiro("ID da Turma: ")

            nota = self._ler_input_float("Nota (0 - 10): ")

            self.sistema.processar_notas(cod_aluno, cod_turma, nota)

            print(f"{Cores.VERDE}Nota {nota:.2f} adicionada com sucesso.{Cores.RESET}") 

        except ValueError as e:
            print(f"{Cores.VERMELHO}Erro: {e}{Cores.RESET}")

        
    def tela_lancar_frequencia(self):
        print(f"\n{Cores.MAGENTA}---- Lançar Frequência ----{Cores.RESET}")

        try:
            cod_aluno = self._ler_input_inteiro("Matrícula do aluno: ")
            cod_turma = self._ler_input_inteiro("ID da Turma: ")

            frequencia = self._ler_input_float("Frequência (0 - 100): ")

            self.sistema.processar_frequencia(cod_aluno, cod_turma, frequencia)

            print(f"{Cores.VERDE}Frequência atualizada para {frequencia:.1f}% com sucesso.{Cores.RESET}")

        except ValueError as e:
            print(f"{Cores.VERMELHO}Erro: {e}{Cores.RESET}")


    def tela_relatorios(self):
        print(f"\n{Cores.MAGENTA}---- Relatórios Gerais ----{Cores.RESET}")

        turmas = self.sistema.turmas

        if not turmas:
            print("Nenhuma turma foi cadastrada")
            return
        
        for turma in turmas:

            #Busca nome do curso para legibiligade do usuário
            curso = self.sistema.buscar_curso(turma.codigo_curso)
            nome_curso = curso.nome if curso else "Curso Desconhecido"

            print(f"\n{Cores.CIANO}{Cores.NEGRITO}Turma: {turma.codigo_turma} | Disciplina: {nome_curso} (ID: {turma.codigo_curso}){Cores.RESET}")
            print(f"Lotação: {len(turma)} / {turma.vagas_totais}")

        #--- Lista Alunos ----
            if turma.matriculas:
                print(f"  {Cores.NEGRITO}Lista de Alunos:{Cores.RESET}")
                
                for m in turma.matriculas:
                    # 2. MELHORIA: Colorir o status (Aprovado=Verde, Reprovado=Vermelho, Cursando=Azul)
                    if m.estado == "APROVADO":
                        cor_status = Cores.VERDE
                    elif "REPROVADO" in m.estado:
                        cor_status = Cores.VERMELHO
                    elif "TRANCADA" == m.estado:
                        cor_status = Cores.AMARELO
                    else:
                        cor_status = Cores.AZUL # Cursando
                    
                    # Formata as notas bonitinhas (ex: 8.0, 9.5)
                    notas_str = ", ".join([f"{n:.1f}" for n in m.notas]) if m.notas else "Sem notas"
                    
                    print(f"   -> Aluno: {m.aluno.nome:<25} | Situação: {cor_status}{m.estado:<15}{Cores.RESET} | Notas: {notas_str}")
            else:
                print(f"{Cores.AMARELO}   --   (Sem alunos na turma.)  --   {Cores.RESET}")

            # Estatísticas Matemáticas 
            print(f"\n{Cores.AZUL}[Estatísticas da Turma]{Cores.RESET}")

            taxa = turma.ver_taxa_aprovacao_turma()
            # Pinta a taxa de verde se for alta (>70%), vermelha se baixa
            cor_taxa = Cores.VERDE if taxa >= 70 else Cores.VERMELHO
            print(f"Taxa de Aprovação: {cor_taxa}{taxa}%{Cores.RESET}")

            # Distribuição de Notas:
            status = turma.ver_distribuicao_notas()

            if status:
                print(f"   Média da Turma: {status['media_geral']}")
                print(f"   Melhor Média:   {Cores.VERDE}{status['maior_nota']}{Cores.RESET}")
                print(f"   Menor Média:    {Cores.VERMELHO}{status['menor_nota']}{Cores.RESET}")
                print(f"   Desvio Padrão:  {status['desvio_padrao']}")
            else:
                print(f"{Cores.AMARELO}   ---- Notas Insuficientes para gerar estatísticas. ----{Cores.RESET}")

            print(f"{Cores.MAGENTA}{'=' * 60}{Cores.RESET}")



    def tela_trancar_matricula(self):
        print(f"\n{Cores.MAGENTA}---- Trancar Matrícula ----{Cores.RESET}")
        try:
            cod_aluno = self._ler_input_inteiro("Matrícula do aluno: ")
            cod_turma = self._ler_input_inteiro("ID da Turma: ")

            confirmacao = input(f"{Cores.AMARELO}Tem certeza que deseja trancar ? (s/n): {Cores.RESET}").lower().strip()
            if confirmacao == "s":
                self.sistema.processar_trancamento(cod_aluno, cod_turma)
                print(f"{Cores.VERDE}Matrícula trancada com sucesso.{Cores.RESET}")
            else:
                print(f"{Cores.AMARELO}Operação cancelada.{Cores.RESET}")

        except ValueError as e:
            print(f"{Cores.VERMELHO}Erro: {e}{Cores.RESET}")


    def tela_calcular_situacao(self):
        print(f"\n{Cores.MAGENTA}---- Calcular Situação ----{Cores.RESET}")
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
        print(f"\n{Cores.MAGENTA}---- Relatório de Alunos em Risco ----{Cores.RESET}")

        try:
            cod_turma = self._ler_input_inteiro("Código Turma: ")

            turma, lista_risco = self.sistema.relatorio_alunos_em_risco(cod_turma)

            curso = self.sistema.buscar_curso(turma.codigo_curso)
            nome_curso = curso.nome if curso else "Curso Desconhecido"
            
            print(f"\nAnálise de risco - TURMA: {turma.codigo_turma} | DISCIPLINA: {Cores.CIANO}{nome_curso}{Cores.RESET}")

            if not lista_risco:
                print(f"Nenhum aluno está em risco nessa turma. (Todos estão com notas e frequências acima ou igual ás medias)")
            else:
                print(f"{Cores.VERMELHO}ALERTA: {len(lista_risco)} aluno(s) precisa(m) de atenção.\n{Cores.RESET}")
                for item in lista_risco:
                    motivos = " e ".join(item["motivo"])

                    print(f" Nome: {item['nome']} |Matrícula: {item['matricula']}")
                    print(f" Motivo: {Cores.VERMELHO}{motivos}{Cores.RESET}")
                    print(f"{Cores.MAGENTA}{'=' * 40}{Cores.RESET}")

        except ValueError as e:
            print(f"{Cores.VERMELHO}Erro: {e}{Cores.RESET}")

    def tela_top_alunos(self):
        print(f"\n{Cores.MAGENTA}---- Top Melhores Alunos (CR) ----{Cores.RESET}")
        
        try:
            n_input = self._ler_input_inteiro("Quantos alunos deseja ver? (Padrão 3): ", obrigatorio=False)
            # Se veio None (vazio) ou se o número é <= 0, usa 3. Caso contrário, usa o número.
            n = n_input if (n_input is not None and n_input > 0) else 3

            top_lista = self.sistema.relatorio_top_alunos(n)


            if not top_lista:
                print("Nenhum aluno cadastrado para gerar ranking.")
                return
        
            print(f"\nRANKING: TOP {len(top_lista)} ALUNOS")
            print(f"{'Pos':<5} | {'Nome':<20} | {'CR':<5}")
            print("-" * 45)

            for i, aluno in enumerate(top_lista, start=1):
                cr = aluno.calcular_cr()
                print(f"#{i:<4} | {aluno.nome:<20} | {cr:.2f}")
                
        except ValueError as e:
            print(f"Erro: {e}")
        