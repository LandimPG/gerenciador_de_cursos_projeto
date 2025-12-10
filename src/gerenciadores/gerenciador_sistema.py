import sys
import os
import json
from datetime import datetime

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
        
        self.configuracoes = self.carregar_configuracoes()

    def carregar_configuracoes(self):
        """
        Lê os arquivos do settings.json
        """

        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            root_dir = os.path.dirname(os.path.dirname(base_dir))
            settings_path = os.path.join(root_dir, "settings.json")

            with open (settings_path, "r", encoding="utf-8" ) as f:
                return json.load(f)
            
        except FileNotFoundError:
            print("Settings.json não foi encontrado. Usando formatações padrão")

            return {"data_limite_trancamento": "2099-12-31"}
        

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

    def criar_curso(self, nome, codigo_curso, horas, ementa, pre_requisitos = None):

        # Validar se já existe
        if self.buscar_curso(codigo_curso) is not None:
            raise ValueError(f"Já existe um curso com o código {codigo_curso}")
        
        for c in self.cursos:
            if c.nome.lower() == nome.strip().lower():
                raise ValueError(f"Já existe um curso com o nome: {nome}.")
            
        #Validação dos ids dos pré-requisitos.
        if pre_requisitos:
            for id_req in pre_requisitos:
                if self.buscar_curso(id_req) is None:
                    raise ValueError(f"Erro: O curso pré-requisito ID {id_req} ainda não existe no sistema.")


        novo_curso = Curso(nome, codigo_curso, horas, ementa, pre_requisitos)
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

        
        if self.buscar_matricula(cod_aluno, cod_turma) is not None:
            raise ValueError(f"Aluno já matriculado nessa turma.")
        
        # É preciso ter o objeto curso para saber a lista de pré requisitos
        curso = self.buscar_curso(turma.codigo_curso)
        if curso and curso.lista_pre_requisitos:
            for id_req in curso.lista_pre_requisitos:
                aprovado = False

                for historico in aluno.historico:

                    if historico.turma.codigo_curso == id_req and historico.estado == "APROVADO":
                        aprovado = True
                        break

                if not aprovado:
                    raise ValueError(f"Pré-requisito não atendido: O aluno precisa ser APROVADO no curso ID {id_req} antes.")
                
        # Verificar Duplicidade de vagas
        if self.buscar_matricula(cod_aluno, cod_turma) is not None:
            raise ValueError("Aluno já matriculado nessa turma.")

        nova_matricula = Matricula(aluno, turma)

        turma.adicionar_matricula(nova_matricula) #Valida vagas
        aluno.realizar_matricula(nova_matricula)  #VAlida choque de horário

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
            nota_minima = self.configuracoes.get("nota_minima_aprovacao", 6.0)
            frequencia_minima = self.configuracoes.get("frequencia_minima_aprovacao", 75.0)
            matricula.calcular_situacao(nota_minima, frequencia_minima)
            return matricula.estado
        
        return None
    
    def processar_trancamento(self, cod_aluno, cod_turma):
        """
        Muda o estado de matrícula para TRANCADA chamando o método
        trancar_matricula
        """
        matricula = self.buscar_matricula(cod_aluno, cod_turma)
        if matricula is None:
            raise ValueError("Matrícula não encontrada.")
        
        data_limite_str = self.configuracoes.get("data_limite_trancamento")

        if data_limite_str:
            data_limite = datetime.strptime(data_limite_str, "%Y-%m-%d")
            data_hoje = datetime.now()

            if data_hoje > data_limite:
                raise ValueError("Erro! Data limite de trancamento foi excedida ")

        matricula.trancar_matricula()
        return matricula
    
    def ver_situacao_aluno(self, cod_aluno, cod_turma):
        """
        Calcula a situação do aluno por meio do método calcular_situacao
        em matricula.py
        """

        matricula = self.buscar_matricula(cod_aluno, cod_turma)
        if matricula is None:
            raise ValueError("Matrícula não foi encontrada.")
        
        #Conseguir as informações do seetings.json
        nota_minima = self.configuracoes.get("nota_minima_aprovacao", 6.0)
        frequencia_minima = self.configuracoes.get("frequencia_minima_aprovacao", 75.0)


        # verifica notas/frequência e muda o status para APROVADO ou REPROVADO
        matricula.calcular_situacao(media_minima = nota_minima, frequencia_minima = frequencia_minima)

        if matricula.estado != "CURSANDO":
            #Remove das matriculas atuais
            if matricula in matricula.aluno.matriculas_atuais:
                matricula.aluno.matriculas_atuais.remove(matricula)

            if matricula not in matricula.aluno.historico:
                matricula.aluno.historico.append(matricula)

        return matricula.estado
    