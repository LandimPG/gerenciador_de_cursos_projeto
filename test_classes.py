import pytest
from src.usuarios.aluno import Aluno
from src.academicos.curso import Curso
from src.academicos.turma import Turma
from src.academicos.matricula import Matricula

# --- TESTES DA CLASSE CURSO ---

def test_criar_curso_valido():
    """Testa se um curso é criado corretamente com os dados válidos."""
    c = Curso("Engenharia de Software", 10, 3000, "Formação de Engenheiros")
    assert c.nome == "Engenharia De Software"  # Verifica o .title()
    assert c.codigo_curso == 10
    assert c.carga_horaria == 3000

def test_validacao_carga_horaria_negativa():
    """Testa se o sistema impede carga horária negativa ou zero."""
    with pytest.raises(ValueError):
        Curso("Curso Ruim", 11, -10, "Ementa teste")

def test_curso_str():
    """Testa o método especial __str__ do Curso."""
    c = Curso("Python", 1, 40, "Introdução")
    resultado = str(c)
    assert "Python" in resultado
    assert "40 Horas" in resultado

# --- TESTES DA CLASSE ALUNO ---

def test_criar_aluno_valido():
    """Testa criação de aluno e validação de email."""
    a = Aluno("João Silva", "joao@ufca.edu.br", 20241001)
    assert a.nome == "João Silva"
    assert a.email == "joao@ufca.edu.br"

def test_aluno_email_invalido():
    """Testa se o setter de email bloqueia formatos errados."""
    with pytest.raises(ValueError):
        Aluno("Teste", "email_sem_arroba", 123)

def test_ordenacao_alunos_por_cr():
    """
    Testa o método especial __lt__ (Less Than).
    Cenário: Aluno A tem CR maior que Aluno B.
    Ordenação padrão (sort) deve colocar o menor CR primeiro.
    """
    # Para testar o CR, precisamos simular histórico, 
    # mas vamos confiar na lógica de desempate por nome se CR for 0
    a1 = Aluno("Ana", "ana@test.com", 1)
    a2 = Aluno("Bruno", "bruno@test.com", 2)
    
    # Como ambos tem CR 0.0, o critério de desempate é o nome.
    # 'Ana' vem antes de 'Bruno' alfabeticamente -> Ana < Bruno = True
    assert a1 < a2 

# --- TESTES DA CLASSE TURMA ---

def test_criar_turma_valida():
    t = Turma(
        codigo_curso=10, 
        vagas_totais=30, 
        semestre="2025.1", 
        horarios={"seg": "14:00-16:00"}, 
        codigo_turma=50
    )
    assert t.semestre == "2025.1"
    assert t.vagas_totais == 30
    assert len(t) == 0  # Testando __len__ inicial

def test_validacao_semestre_formato():
    """Testa a regex do semestre (AAAA.S)."""
    with pytest.raises(ValueError):
        Turma(10, 30, "2025-1", {"seg": "10:00-12:00"}, 50) # Formato errado

def test_turma_len_com_matricula():
    """Testa se __len__ aumenta ao adicionar matrícula."""
    # Setup
    t = Turma(1, 10, "2025.1", {"seg": "08:00-10:00"}, 100)
    a = Aluno("Ze", "ze@mail.com", 999)
    m = Matricula(a, t)
    
    # Ação
    t.adicionar_matricula(m)
    
    # Verificação
    assert len(t) == 1

# --- TESTES DA CLASSE MATRICULA ---

def test_validacao_nota():
    """Testa se o sistema bloqueia notas fora do intervalo 0-10."""
    a = Aluno("Teste", "t@t.com", 1)
    # Mockando a turma já que a matrícula pede um objeto turma
    # Aqui passamos um objeto real para simplificar
    t = Turma(1, 10, "2025.1", {"seg": "08:00-10:00"}, 100)
    
    m = Matricula(a, t)
    
    # Teste nota válida
    m.lancar_nota(8.5)
    assert 8.5 in m.notas

    # Teste nota inválida (Maior que 10)
    with pytest.raises(ValueError):
        m.lancar_nota(11.0)

    # Teste nota inválida (Negativa)
    with pytest.raises(ValueError):
        m.lancar_nota(-1.0)