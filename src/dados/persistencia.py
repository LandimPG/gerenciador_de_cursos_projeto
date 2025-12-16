import json
import os 
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Pasta dados
ROOT_DIR = os.path.dirname(os.path.dirname(BASE_DIR)) # Raiz do projeto (onde está o main.py provavelmente)
arquivo_db = os.path.join(ROOT_DIR, "banco_dados.json")

current_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))

sys.path.append(project_root)

from src.academicos.turma import Turma
from src.academicos.matricula import Matricula
from src.usuarios.aluno import Aluno
from src.academicos.curso import Curso

def salvar_dado(lista_alunos, lista_cursos, lista_turmas, lista_matriculas):
    """
    Recebe as listas de objetos, converte cada um para dicionário
    e salva tudo em um arquivo JSON.
    """
    dados_salvar = {
        "cursos": [c.to_dict() for c in lista_cursos],
        "alunos": [a.to_dict() for a in lista_alunos],
        "turmas": [t.to_dict() for t in lista_turmas],
        "matriculas": [m.to_dict() for m in lista_matriculas]
    }
    try: 
        with open(arquivo_db, "w", encoding="utf-8") as arquivo:
            json.dump(dados_salvar, arquivo, indent= 4, ensure_ascii= False)
        print(f"Dados salvos com sucesso em {arquivo_db}")
    except Exception as e:
        print(f"Erro aos salvar dados: {e}")

    
def carregar_dados():
    if not os.path.exists(arquivo_db):
        print("Arquivo de dados não encontrado. Iniciando banco vazio.")
        return [], [], [], []
    
    try:
        with open(arquivo_db, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        lista_cursos = [Curso.from_dict(c) for c in dados.get("cursos", [])]
        
        mapa_cursos = {c.codigo_curso: c for c in lista_cursos}

        lista_turmas = []
        mapa_turmas = {}

        for t_dict in dados.get("turmas", []):
            t = Turma.from_dict(t_dict)

            if t.codigo_curso in mapa_cursos:
                t.curso = mapa_cursos[t.codigo_curso]
            
            lista_turmas.append(t)
            mapa_turmas[int(t.codigo_turma)] = t

        lista_alunos = []
        mapa_alunos = {}
        for a_dict in dados.get("alunos", []):
            a = Aluno.from_dict(a_dict)
            lista_alunos.append(a)
            mapa_alunos[int(a.codigo_matricula)] = a
        
        lista_matriculas = []

        for m_dict in dados.get("matriculas", []):

            try:
                cod_aluno = int(m_dict["codigo_aluno"])
                cod_turma = int(m_dict["codigo_turma"])
            except ValueError:
                cod_aluno = m_dict["codigo_aluno"]
                cod_turma = m_dict["codigo_turma"]

            aluno_obj = mapa_alunos.get(cod_aluno)
            turma_obj = mapa_turmas.get(cod_turma)

            if aluno_obj is not None and turma_obj is not None:
                nova_matricula = Matricula(aluno_obj, turma_obj)
                nova_matricula.notas= m_dict["notas"]
                nova_matricula.estado = m_dict["estado"]
                nova_matricula.frequencia = m_dict.get("frequencia", 0.0)

                lista_matriculas.append(nova_matricula)

                if nova_matricula.estado == "CURSANDO":
                    aluno_obj.matriculas_atuais.append(nova_matricula)
                else:
                    aluno_obj.historico.append(nova_matricula)

                turma_obj.matriculas.append(nova_matricula)

        print("Dados carregados com sucesso.")

        return lista_alunos, lista_cursos, lista_turmas, lista_matriculas


    except Exception as e:
        print(f" Erro crítico ao ler dados: {e}")
        return [], [], [], []
    