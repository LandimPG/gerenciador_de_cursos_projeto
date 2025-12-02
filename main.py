import sys
import os

# Ajusta o caminho para importar os módulos corretamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.academicos.curso import Curso
from src.academicos.turma import Turma
from src.usuarios.aluno import Aluno
from src.academicos.matricula import Matricula
from src.dados.persistencia import salvar_dado, carregar_dados

# --- VARIÁVEIS GLOBAIS
lista_alunos = []
lista_cursos = []
lista_turmas = []
lista_matriculas = []

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


# --- FUNÇÕES DE CADASTRO ---

def cadastrar_curso():
    print("\n----Novo Curso----")
    try:
        nome = input("Nome do Curso: ")
        codigo_curso = int(input("Código(ID) do Curso: "))

        # Verifica duplicidade
        for curso in lista_cursos:
            if curso.codigo_curso == codigo_curso:
                print(f"Erro: Já existe um curso com o código {codigo_curso}")
                return
            
            if curso.nome.lower() == nome.strip().lower():
                print(f"Erro: Já existe um curso com o nome: {nome}.")
                return

        horas  = int(input("Carga Horária: "))
        ementa = input("Ementa/Descrição: ")

        novo_curso = Curso(nome, codigo_curso, horas, ementa)
        lista_cursos.append(novo_curso)
        print("Curso cadastrado com sucesso.")
    except ValueError as e:
        print("Erro: Código e Horas devem ser números inteiros")


def cadastrar_aluno():
    print("\n----Novo Aluno----")

    try:
        nome = input("Nome do Aluno: ")
        email = input("Email do Aluno: ")
        matricula = int(input("Número de Matrícula do Aluno: "))

        for aluno in lista_alunos:
            if aluno.codigo_matricula == matricula:
                print(f"Erro: Já existe um aluno com a matrícula: {matricula}")
                return

        novo_aluno = Aluno(nome, email, matricula)
        lista_alunos.append(novo_aluno)
        print("Aluno cadastrado com sucesso! :)")

    except ValueError as e:
        print(f"Erro de validação {e}") 

def nova_turma():
    print("\n----Abrir nova Turma----")
    if not lista_cursos:
        print("Cadastre um curso antes de abrir uma turma.")
        return
    
    try:
        # Listar cursos
        print("Cursos Disponíveis: ")
        for c in lista_cursos:
            print(f"Nome: {c.nome} | ID: {c.codigo_curso}")

        cod_curso = int(input("\nDigite o ID do curso para essa turma: "))

        curso_buscado = None
        for c in lista_cursos:
            if c.codigo_curso == cod_curso:
                curso_buscado = c
                break

        if not curso_buscado:
            print("Curso não foi encontrado. :(")
            return
        
        cod_turma = int(input("Código (ID) da Turma: "))
        vagas = int(input("Vagas totais: "))
        semestre = input("Semestre (ex: 2025.1): ")
        local = input("Local (Ex: A01): ")

        print("Formato obrigatório do horário: HH:MM-HH:MM (Ex: 18:00-22:00)")
        print("Dias: seg, ter, qua, qui, sex, sab, dom")
        
        dia = input("Dia da semana: ").strip().lower()
        hora = input("Horário: ").strip()
        
        horarios = {dia: hora} 

        nova_turma = Turma(cod_curso, vagas, semestre, horarios, cod_turma, local=local)
        nova_turma.abrir_turma() # abrir a turma
        lista_turmas.append(nova_turma)
        print("Turma aberta com sucesso.")

    except ValueError as e:
        print(f"Erro nos dados: {e}")

def realizar_matricula():
    print("\n--- Matricular Aluno ---")
    if not lista_alunos or not lista_turmas:
        print("Precisa-se ter alunos e turmas cadastrados no sistema.")
        return
    
    try:
        # Pegar como string direto e remover espaços
        input_aluno = input("Digite a matrícula do aluno: ").strip()
        input_turma = input("Digite o código da turma: ").strip()

        # 1. Busca Manual do Aluno
        aluno_obj = None
        for a in lista_alunos:
            if str(a.codigo_matricula).strip() == input_aluno:
                aluno_obj = a
                break
        
        # 2. Busca Manual da Turma
        turma_obj = None
        for t in lista_turmas:
            if str(t.codigo_turma).strip() == input_turma:
                turma_obj = t
                break

        # 3. Validações
        if aluno_obj is None:
            print(f"\nErro: Aluno com matrícula '{input_aluno}' não encontrado.")
            return
            
        if turma_obj is None:
            print(f"\nErro: Turma com código '{input_turma}' não encontrada.")
            return
        
        # 4. Verifica duplicidade
        for m in lista_matriculas:
            if str(m.aluno.codigo_matricula) == str(aluno_obj.codigo_matricula) and \
               str(m.turma.codigo_turma) == str(turma_obj.codigo_turma):
                print("\nErro: Este aluno já está matriculado nesta turma!")
                return

        # 5. Criação da Matrícula
        nova_matricula = Matricula(aluno_obj, turma_obj)
    
        # Tenta adicionar na turma (Valida vagas)
        turma_obj.adicionar_matricula(nova_matricula)
        
        # Tenta adicionar no aluno (Valida choque de horário)
        aluno_obj.realizar_matricula(nova_matricula)

        lista_matriculas.append(nova_matricula)
        # Salvar automático opcional, ou deixa para salvar ao sair

    except ValueError as e:
        print(f"Erro de Regra de Negócio: {e}")
        # Remove se deu erro no meio do processo para não corromper a lista
        if 'nova_matricula' in locals() and nova_matricula in lista_matriculas:
            lista_matriculas.remove(nova_matricula)

    except Exception as e:
        print(f"Erro inesperado: {e}")

def buscar_matricula():
    """
    Pede os IDs, busca e retorna o objeto Matrícula.
    Se não achar, retorna None.
    """
    try:
        print("\n ---- Buscando Matrícula ----")
        cod_aluno = int(input("Matrícula do Aluno: "))
        cod_turma = int(input("Turma do Aluno: "))

        for m in lista_matriculas:
            if m.aluno.codigo_matricula == cod_aluno and m.turma.codigo_turma == cod_turma:
                return m
            
        print("A matrícula deste aluno não foi encontrada para esta turma.")
        return None
        
    except ValueError:
        print("Código aluno e código turma precisam ser digitados como números inteiros.")


def lancar_notas():
    print("\n---- Lançar Notas ----")
    matricula = buscar_matricula()

    if matricula:
        print(f"Aluno: {matricula.aluno.nome}.| Turma: {matricula.turma.codigo_turma} | Notas: {matricula.notas}")

        try:
            nota = float(input("Digite a nota do aluno (0 a 10): "))
            matricula.lancar_nota(nota)

        except ValueError:
            print("Valor inserido para nota foi inválido.")
    
def lancar_frequencia():
    print("\n---- Lançar Frequência ----")
    matricula = buscar_matricula()

    if matricula:
        print(f"Aluno: {matricula.aluno.nome}.| Turma: {matricula.turma.codigo_turma} | Frequência: {matricula.frequencia}")

        try:
            frequencia = float(input("Digite a frequência atual do aluno(0 a 100): "))
            matricula.lancar_frequencia(frequencia)
        
        except ValueError:
            print("Valor para a frequência foi inválido.")

def listas_gerais():
    for turma in lista_turmas:
        print(f"\nTURMA: {turma.codigo_turma} | Semestre: {turma.semestre}")
        print(f"Lotação: {len(turma)}/{turma.vagas_totais} alunos")

        if turma.matriculas: 
            print("---- Alunos Matriculados ----")
            for matricula_obj in turma.matriculas:
                print(f"{matricula_obj.aluno.nome} (Matrícula: {matricula_obj.aluno.codigo_matricula}) - Status: {matricula_obj.estado}")
        else:
            print("Nenhum aluno matriculado nesta turma.")


def main():
    # 1. Carrega dados ao iniciar
    global lista_alunos, lista_cursos, lista_turmas, lista_matriculas

    lista_alunos, lista_cursos, lista_turmas, lista_matriculas = carregar_dados()

def menu():
    while True:
        limpar_tela()
        print("=== SISTEMA DE GESTÃO ACADÊMICA (UFCA) ===")
        print("1. Cadastrar Curso")
        print("2. Cadastrar Aluno")
        print("3. Abrir Turma")
        print("4. Realizar Matrícula")
        print("5. Lançar Notas")
        print("6. Lançar Frequência")
        print("7. Relatórios Gerais (Alunos por Turma)")
        print("0. Sair e Salvar")
        
        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            cadastrar_curso()
        elif opcao == '2':
            cadastrar_aluno()
        elif opcao == '3':
            nova_turma()
        elif opcao == '4':
            realizar_matricula()
        elif opcao == '5':
            lancar_notas()
        elif opcao == '6':
            lancar_frequencia()
        elif opcao == '7':
            listas_gerais()
        elif opcao == '0':
            print("Salvando dados...")
            
            salvar_dado(lista_alunos, lista_cursos, lista_turmas, lista_matriculas) 
            print("Saindo do sistema. Até logo!")
            break
        else:
            print("Opção inválida!")
        
        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main() # Carrega os dados iniciais
    menu() # Chama o loop do menu