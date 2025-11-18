class Matricula:
    """
    Objeto que liga Aluno com uma Turma

    Responsabilidades:
        Retém os dados da ligação entre Aluno com a Turma como: notas, frequência e o estado da matrícula (Aprovado, Reprovado, Cursando).

        Ela permite o lançamento das notas do estudante, o cálculo da situação  final e trancamento.
    """
    def __init__(self, aluno:object, turma:object, notas:list = None, frequencia: float = 0.0,estado:str = "CURSANDO"):
        pass