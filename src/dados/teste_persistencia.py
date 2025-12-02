import sys
import os

# --- CORREÇÃO DO PATH ---
# Pega o caminho absoluto da pasta onde este arquivo está (src/dados)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Sobe dois níveis para chegar na raiz do projeto
# 1. De 'dados' para 'src'
# 2. De 'src' para a raiz 'gerenciador_de_cursos_projeto'
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))

# Adiciona a raiz ao sys.path para que o Python reconheça "src" como um módulo
sys.path.append(project_root)
# ------------------------

from src.academicos.curso import Curso
from src.academicos.turma import Turma
from src.usuarios.aluno import Aluno
from src.academicos.matricula import Matricula
from src.dados.persistencia import salvar_dado, carregar_dados

# Ajuste o import acima conforme o nome da sua pasta de persistencia. 
# Se o arquivo persistencia.py estiver na raiz, use: from persistencia import ...

def teste_fluxo_persistencia():
    print("=== INICIANDO TESTE DE PERSISTÊNCIA ===\n")

    # ---------------------------------------------------------
    # ETAPA 1: CRIAR DADOS NA MEMÓRIA
    # ---------------------------------------------------------
    print("1. Criando objetos na memória...")
    
    # Criar Curso
    curso_py = Curso("Python Avançado", 101, 60, "Curso de POO e Dados")
    
    # Criar Turma
    turma_2025 = Turma(101, 30, "2025.1", {"seg": "10:00-12:00"}, 500)
    
    # Criar Aluno
    aluno_joao = Aluno("João Teste", "joao@email.com", 2024001)
    
    # Criar Matrícula (O Grande Teste do Relacionamento)
    matricula = Matricula(aluno_joao, turma_2025)
    
    # Adicionar na lógica do sistema (vincular listas)
    # Importante: O sistema real faria isso no controller, aqui fazemos manual
    turma_2025.matriculas.append(matricula)
    aluno_joao.matriculas_atuais.append(matricula)
    
    # Lançar nota e frequência para testar se salva
    matricula.lancar_nota(9.5)
    matricula.frequencia = 80.0 # setando direto para teste

    print("   -> Objetos criados. Aluno matriculado na turma 500 com nota 9.5.")

    # ---------------------------------------------------------
    # ETAPA 2: SALVAR NO JSON
    # ---------------------------------------------------------
    print("\n2. Salvando dados no JSON...")
    
    # Prepara as listas como se fosse o 'banco de dados' do sistema
    lista_alunos = [aluno_joao]
    lista_cursos = [curso_py]
    lista_turmas = [turma_2025]
    lista_matriculas = [matricula]

    salvar_dado(lista_alunos, lista_cursos, lista_turmas, lista_matriculas)
    print("   -> Salvo com sucesso.")

    # ---------------------------------------------------------
    # ETAPA 3: SIMULAR REINÍCIO (LIMPAR MEMÓRIA)
    # ---------------------------------------------------------
    print("\n3. Limpando memória (Simulando fechar o programa)...")
    del aluno_joao
    del turma_2025
    del matricula
    del curso_py
    lista_alunos = []
    lista_turmas = []
    
    # ---------------------------------------------------------
    # ETAPA 4: CARREGAR DO JSON
    # ---------------------------------------------------------
    print("\n4. Carregando dados do disco...")
    
    # Aqui a mágica acontece: o script lê o JSON e reconstrói os objetos
    l_alunos, l_cursos, l_turmas, l_matriculas = carregar_dados()

    print(f"   -> Carregado: {len(l_alunos)} alunos, {len(l_matriculas)} matrículas.")

    # ---------------------------------------------------------
    # ETAPA 5: VALIDAÇÃO PROFUNDA
    # ---------------------------------------------------------
    print("\n5. Verificando integridade dos dados...")

    aluno_recuperado = l_alunos[0]
    turma_recuperada = l_turmas[0]
    matricula_recuperada = l_matriculas[0]

    # Teste A: Dados básicos
    if aluno_recuperado.nome == "João Teste":
        print("   [OK] Nome do aluno preservado.")
    else:
        print("   [ERRO] Nome do aluno incorreto.")

    # Teste B: Dados da Matrícula (Nota e Frequência)
    if 9.5 in matricula_recuperada.notas and matricula_recuperada.frequencia == 80.0:
        print("   [OK] Notas e Frequência preservadas.")
    else:
        print(f"   [ERRO] Nota/Freq perdidas. Notas: {matricula_recuperada.notas}")

    # Teste C: Relacionamento ALUNO -> MATRICULA
    # O aluno recuperado deve ter a matrícula na sua lista 'matriculas_atuais'
    if len(aluno_recuperado.matriculas_atuais) == 1:
        print("   [OK] A matrícula aparece na lista do Aluno.")
    else:
        print("   [ERRO] A lista de matrículas do aluno está vazia!")

    # Teste D: Relacionamento TURMA -> MATRICULA
    # A turma recuperada deve ter a matrícula na sua lista
    if len(turma_recuperada.matriculas) == 1:
        print("   [OK] A matrícula aparece na lista da Turma.")
    else:
        print("   [ERRO] A lista de matrículas da turma está vazia!")

    # Teste E: Identidade de Objeto (O teste de ouro)
    # A matrícula dentro do aluno deve ser o MESMO OBJETO da matrícula solta
    mat_do_aluno = aluno_recuperado.matriculas_atuais[0]
    
    if mat_do_aluno is matricula_recuperada:
        print("   [OK] IDENTIDADE CONFIRMADA: O objeto está conectado corretamente na memória.")
    else:
        print("   [ERRO] Clones detectados! A matrícula do aluno não é a mesma da lista geral.")

    print("\n=== TESTE FINALIZADO ===")

if __name__ == "__main__":
    teste_fluxo_persistencia()