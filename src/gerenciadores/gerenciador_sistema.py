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
    """

    def __init__(self):
        # Carrega os dados assim que o sistema inicia
        self.alunos, self.cursos, self.turmas, self.matriculas = carregar_dados()

    def salvar_tudo(self):
        salvar_dado(self.alunos, self.cursos, self.turmas, self.matriculas)

    # --- MÉTODOS DE BUSCA ---

    def buscar_curso(self, codigo_curso: int):
        for c in self.cursos:
            if c.codigo_curso == codigo_curso:
                return c
        return None
    
    def buscar_aluno(self, matricula: int):
        for a in self.alunos:
            if a.codigo_matricula == matricula:
                return a
        return None
    
    def buscar_turma(self, codigo_turma: int):
        for t in self.turmas:
            # Usa getattr para segurança, caso o objeto venha incompleto do JSON
            id_real = getattr(t, 'codigo_turma', None)
            if id_real == codigo_turma:
                return t
        return None

    def buscar_matricula(self, cod_aluno: int, cod_turma: int):
        for m in self.matriculas:
            if m.aluno.codigo_matricula == cod_aluno and m.turma.codigo_turma == cod_turma:
                return m
        return None
    
    # --- MÉTODOS DE ESCRITA ---

    def criar_curso(self, nome, codigo_curso, horas, ementa):
        # Correção: usar 'is not None' para evitar erros com objetos vazios
        if self.buscar_curso(codigo_curso) is not None:
            raise ValueError(f"Já existe um curso com o código {codigo_curso}")
        
        for c in self.cursos:
            if c.nome.lower() == nome.strip().lower():
                raise ValueError(f"Já existe um curso com o nome: {nome}.")
            
        novo_curso = Curso(nome, codigo_curso, horas, ementa)
        self.cursos.append(novo_curso)
        return novo_curso
    
    def criar_aluno(self, nome, email, matricula):
        if self.buscar_aluno(matricula) is not None:
            raise ValueError(f"Já existe um aluno com a matrícula: {matricula}.")
        
        novo_aluno = Aluno(nome, email, matricula)
        self.alunos.append(novo_aluno)
        return novo_aluno

    def criar_turma(self, cod_curso, cod_turma, vagas, semestre, local, horarios):
        curso = self.buscar_curso(cod_curso)
        
        # Correção Crítica: Validar se é None
        if curso is None:
            raise ValueError("Curso não encontrado.")
        
        if self.buscar_turma(cod_turma) is not None:
            raise ValueError(f"Já existe uma turma com o código: {cod_turma}")
        
        nova_turma = Turma(cod_curso, vagas, semestre, horarios, cod_turma, local=local)
        nova_turma.abrir_turma()
        self.turmas.append(nova_turma)
        return nova_turma
    
    def realizar_matricula(self, cod_aluno, cod_turma):
        # 1. Busca Aluno
        aluno = self.buscar_aluno(cod_aluno)
        if aluno is None:
            raise ValueError(f"Aluno {cod_aluno} não encontrado.")
        
        # 2. Busca Turma
        turma = self.buscar_turma(cod_turma)
        
        # --- CORREÇÃO DO ERRO ---
        # Não usamos "if not turma", pois se len(turma) == 0 o Python acha que é False.
        # Usamos "if turma is None" para saber se a variável está vazia de verdade.
        if turma is None:
            raise ValueError(f"Turma {cod_turma} não encontrada.")

        # 3. Verifica Duplicidade
        if self.buscar_matricula(cod_aluno, cod_turma) is not None:
            raise ValueError(f"Aluno já matriculado nessa turma.")
        
        # 4. Cria Matrícula
        nova_matricula = Matricula(aluno, turma)

        turma.adicionar_matricula(nova_matricula)
        aluno.realizar_matricula(nova_matricula)

        self.matriculas.append(nova_matricula)
        return nova_matricula
    
    def processar_notas(self, cod_aluno, cod_turma, nota):
        matricula = self.buscar_matricula(cod_aluno, cod_turma)
        if matricula is None:
            raise ValueError("Matrícula não encontrada.")
        
        matricula.lancar_nota(nota)
        return matricula
    
    def processar_frequencia(self, cod_aluno, cod_turma, frequencia):
        matricula = self.buscar_matricula(cod_aluno, cod_turma)
        if matricula is None:
            raise ValueError("Matrícula não encontrada")
        matricula.lancar_frequencia(frequencia)
        return matricula
    
    def processar_calculo_situacao(self, cod_aluno, cod_turma):
        matricula = self.buscar_matricula(cod_aluno, cod_turma)
        if matricula:
            matricula.calcular_situacao()
            return matricula.estado
        return None