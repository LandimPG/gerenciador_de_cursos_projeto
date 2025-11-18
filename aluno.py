from pessoa import Pessoa

class Aluno(Pessoa):
    """
    Representa um estudante matriculado na instituição.
    
    Responsabilidade:
        Mantém a identidade única do aluno (matrícula) e todo o seu registro acadêmico.
        É responsável por armazenar tanto o histórico de disciplinas concluídas quanto
        as matrículas do semestre atual, além de fornecer métodos para cálculo de
        desempenho individual (como o CR).
    """

    def __init__(self, nome:str, email:str, matricula_id:int, historico:list = None, matriculas_atuais:list = None):
        pass