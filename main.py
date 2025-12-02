import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.academicos.curso import Curso
from src.academicos.turma import Turma
from src.usuarios.aluno import Aluno
from src.academicos.matricula import Matricula

# --- VARIÁVEIS GLOBAIS (O "Banco de Dados" na Memória RAM) ---
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
        horas  = int(input("Carga Horária: "))
        ementa = input("Ementa/Descrição: ")

        novo_curso = Curso(nome, codigo_curso, horas, ementa)
        lista_cursos.append(novo_curso)
        print("Curso cadastro.")
    except ValueError as e:
        print("Erro: Código e Horas devem ser números inteiros")


def cadastrar_aluno():
    print("\n----Novo Aluno----")

    try:
        nome = input("Nome do Aluno: ")
        email = input("Email do Aluno: ")
        matricula = int(input("Número de Matrícula do Aluno: "))

        novo_aluno = Aluno(nome, email, matricula)
        lista_alunos.append(novo_aluno)
        print("Aluno cadastrado com sucesso! :)")

    except ValueError as e:
        print(f"Erro de validação {e}") #Tirar dúvida sobre a diferença dessa validação para a de cadastrar curso

def abrir_turma():
    print("\n----Abrir nova Turma----")
    if not lista_cursos:
        print("Cadastre um curso antes de abrir uma turma.")
        return
    
    try:
        #Listar cursos:
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

        #Explicação de como digitar o horário para o usuário

        print("Horário segue o exemplo: seg 18:00-21:00")
        dia = input("Dia ex(seg|ter...): ")
        hora = input("Duração ex(HH:MM-HH:MM|10:00-11:00)")
        horarios = {dia:hora}

        nova_turma = Turma(cod_curso, vagas, semestre, horarios,cod_turma,local=local)
        nova_turma.abrir_turma() #abrir a turma
        lista_turmas.append(nova_turma)
        print("Turma aberta com sucesso.")

    except ValueError as e:
        print(f"Erro nos dados: {e}")

def realizar_matricula():
    print("\n--- Matricular Aluno ---")
    if not lista_alunos or not lista_alunos:
        print("Precisa-se ter alunos e turmas cadastrados no sistema.")
        return
    
    try:
        cod_aluno = int(input("Digite a matrícula do aluno: "))
        cod_turma = int(input("Digite o código da turma: "))

        aluno_obj = next((a for a in lista_alunos if a.codigo_matricula == cod_aluno), None)
        turma_obj = next((t for t in lista_turmas if t.codigo_turma == cod_turma), None)

        if not aluno_obj:
            print("Aluno não encontrado.")
            return
        if not turma_obj:
            print("Turma não encontrada.")
            return
        
        nova_matricula = Matricula(aluno_obj, turma_obj)
        lista_matriculas.append(nova_matricula)
        turma_obj.adicionar_matricula(nova_matricula)
        aluno_obj.realizar_matricula(nova_matricula)

        print(f"Matricula realizada. Aluno: {aluno_obj.nome} em ID turma: {turma_obj.codigo_turma}")

    except ValueError as e:
        print(f"Erro: {e}")

    except Exception as e:
        print(f"Erro inesperado: {e}")









def main():
    print("=== Demonstração Entrega Semana 2: Classes e Encapsulamento ===\n")

cadastrar_aluno()