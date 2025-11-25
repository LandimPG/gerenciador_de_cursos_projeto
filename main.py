import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.academicos.curso import Curso
from src.academicos.turma import Turma
from src.usuarios.aluno import Aluno
from src.academicos.matricula import Matricula

def main():
    print("=== Demonstração Entrega Semana 2: Classes e Encapsulamento ===\n")

    try:
        # 1. Instanciando Cursos (Testando __init__ e validações de Curso)
        print("--- 1. Criando Cursos ---")
        curso_poo = Curso(
            nome="Programação Orientada a Objetos",
            codigo_curso=101,
            carga_horaria=64,
            ementa="Conceitos de POO, Classes, Herança, Polimorfismo."
        )
        print(f"Curso Criado (Teste __str__):\n{curso_poo}") # 

        curso_bd = Curso("Banco de Dados", 102, 60, "SQL, Modelagem, Normalização")
        print("Curso de BD criado com sucesso.")

        # 2. Instanciando Alunos (Testando Pessoa e Aluno)
        print("\n--- 2. Criando Alunos ---")
        aluno1 = Aluno(nome="Carlos Silva", email="carlos@aluno.ufca.edu.br", codigo_matricula=2025001)
        aluno2 = Aluno(nome="Ana Pereira", email="ana@aluno.ufca.edu.br", codigo_matricula=2025002)
        print(f"Alunos criados: {aluno1.nome} e {aluno2.nome}")

        # 3. Instanciando Turma (Testando Oferta e Turma)
        print("\n--- 3. Criando Turma ---")
        horarios_poo = {"ter": "14:00-16:00", "qui": "14:00-16:00"}
        turma_poo = Turma(
            codigo_curso=curso_poo.codigo_curso,
            vagas_totais=30,
            semestre="2025.1",
            horarios=horarios_poo,
            codigo_turma=1,
            local="A01"
        )
        turma_poo.abrir_turma() # [cite: 16]
        print(f"Turma {turma_poo.codigo_turma} criada para o semestre {turma_poo.semestre}.")

        # 4. Realizando Matrículas (Testando Relacionamento e __len__)
        print("\n--- 4. Realizando Matrículas ---")
        
        # Criando objeto matrícula para o aluno 1
        matr1 = Matricula(aluno=aluno1, turma=turma_poo)
        turma_poo.adicionar_matricula(matr1)       # Adiciona na Turma
        aluno1.realizar_matricula(matr1)           # Adiciona no Aluno
        
        # Criando objeto matrícula para o aluno 2
        matr2 = Matricula(aluno=aluno2, turma=turma_poo)
        turma_poo.adicionar_matricula(matr2)
        aluno2.realizar_matricula(matr2)

        print(f"Ocupação da turma (Teste __len__): {len(turma_poo)} alunos matriculados.") # 

        # 5. Simulando Notas e Ordenação (Testando __lt__ e cálculo de CR)
        print("\n--- 5. Lançando Notas e Testando Ordenação (__lt__) ---")
        
        # Carlos tirou 9.0
        matr1.lancar_nota(9.0)
        aluno1.atualizar_historico() # Move para histórico para calcular CR (simulação)
        
        # Ana tirou 9.5
        matr2.lancar_nota(9.5)
        aluno2.atualizar_historico()

        print(f"CR do {aluno1.nome}: {aluno1.calcular_cr()}")
        print(f"CR da {aluno2.nome}: {aluno2.calcular_cr()}")

        # Teste do __lt__ 
        if aluno1 < aluno2:
            print(f"Ordenação: {aluno1.nome} vem antes de {aluno2.nome} (Menor CR ou Ordem Alfabética).") 
        else:
            print(f"Ordenação: {aluno2.nome} vem antes de {aluno1.nome}.")

    except (ValueError, TypeError) as e:
        print(f"\n[ERRO DE VALIDAÇÃO DETECTADO]: {e}")
    
    except Exception as e:
        print(f"\n[ERRO INESPERADO]: {e}")

    
    print("\n--- 6. Teste de Validação (Tentativa de Erro) ---")
    try:
        t_erro = Turma(101, 30, "semestre_errado", {}, 2)
    except ValueError as e:
        print(f"Sucesso! O sistema bloqueou o erro: {e}") 

if __name__ == "__main__":
    main()