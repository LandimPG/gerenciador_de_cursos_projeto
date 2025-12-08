import sys
import os

from src.academicos.curso import Curso
from src.academicos.turma import Turma
from src.usuarios.aluno import Aluno
from src.academicos.matricula import Matricula
from src.dados.persistencia import salvar_dado, carregar_dados

class GerenciadorSistema:
    """
    Controlador central do sistema (Facade).
    Responsável por manter o estado (listas) e executar as regras de negócio.
    Não deve conter 'input()' ou 'print()' diretos, apenas retornar dados ou erros.
    """

    def __init__(self):
        # Carrega os dados assim que o sistema inicia
        self.alunos, self. cursos, self.turmas, self.matriculas = carregar_dados()

    def salvar_tudo(self):
        salvar_dado(self.alunos, self.cursos, self.turmas, self.matriculas)

    # --- MÉTODOS DE BUSCA  ---

    def buscar_curso(self, codigo_curso:int):
        for c in self.cursos:
            if c.codigo_curso == codigo_curso:
                return c
        return None
    
    def buscar_aluno(self, matricula:int):
        for a in self.alunos:
            if a.codigo_matricula == matricula:
                return a
        return None
    
    def buscar_turma(self, codigo_turma: int):
        for t in self.turmas:
            if t.codigo_turma == codigo_turma:
                return t
        return None

    def buscar_matricula(self, cod_aluno: int, cod_turma:int):
        for m in self.matriculas:
            if m.aluno.codigo_matricula == cod_aluno and m.turma.codigo_turma == cod_turma:
                return m
        return None
    
    # --- MÉTODOS DE ESCRITA (Lógica de Negócio)

    def criar_curso(self, nome, codigo_curso, horas, ementa):

        #validar codigo duplicado

        if self.buscar_curso(codigo_curso):
            raise ValueError(f"Já existe um curso com o código {codigo_curso}")
        
        #Validar nome duplicado

        for c in self.cursos:
            if c.nome.lower() == nome.strip().lower():
                raise ValueError(f"Já existe um curso com o nome: {nome}.")
            
        novo_curso = Curso(nome, codigo_curso, horas, ementa)
        self.cursos.append(novo_curso)
        return novo_curso
    
    def criar_aluno(self, nome, email, matricula):
        if self.buscar_aluno(matricula):
            raise ValueError(f"Já existe um aluno com a matrícula: {matricula}.")
        
        novo_aluno = Aluno(nome, email, matricula)
        self.alunos.append(novo_aluno)

    def criar_turma(self, cod_curso, cod_turma, vagas, semestre, local, horarios):
        curso = self.buscar_curso(cod_curso)
        if not curso:
            raise ValueError("Curso não encontrado.")
        if self.buscar_turma(cod_turma):
            raise ValueError(f"Já existe uma turma com o código: {self.criar_turma}")
        
        nova_turma = Turma(cod_curso, vagas, semestre, horarios, cod_turma, local = local)
        nova_turma.abrir_turma() #Realmente abrir a turma logo de cara ? Talvez não seja a melhor abordagem. Ponto para pensar depois
        self.turmas.append(nova_turma)
        return nova_turma
    
    def realizar_matricula(self, cod_aluno, cod_turma):
        aluno = self.buscar_aluno(cod_aluno)
        
        #verifica existência do aluno
        if not aluno:
            raise ValueError(f"Aluno {cod_aluno} não encontrado.")
        
        #Verifica existência da turma
        turma = self.buscar_turma(cod_turma)
        if not turma:
            raise ValueError(f"Turma {cod_turma} não encontrada.")

        #verifica duplicidade de matricualação
        if self.buscar_matricula(cod_aluno, cod_turma):
            raise ValueError(f"Aluno já matriculado nessa turma.")
        
        #Criação de matricula
        nova_matricula = Matricula(aluno, turma)

        # As classes Turma e Aluno já validam vagas e choque de horário

        turma.adicionar_matricula(nova_matricula)
        aluno.realizar_matricula(nova_matricula)

        self.matriculas.append(nova_matricula)
        return nova_matricula
    
    def processar_notas(self, cod_aluno, cod_turma, nota):
        matricula = self.buscar_matricula(cod_aluno, cod_turma)
        if not matricula:
            raise ValueError("Matrícula não encontrada.")
        
        matricula.lancar_notas(nota)
        return matricula
    
    def processar_frequencia(self, cod_aluno, cod_turma, frequencia):
        matricula = self.buscar_matricula(cod_aluno, cod_turma)
        if not matricula:
            raise ValueError("Matrícula não encontrada")
        matricula.lancar_frequencia(frequencia)
        return matricula
    
    def processar_calculo_situacao(self, cod_aluno, cod_turma):
        matricula = self.buscar_matricula(cod_aluno, cod_turma)
        if matricula:
            matricula.calcular_situacao()
            return matricula.estado
        return None
    