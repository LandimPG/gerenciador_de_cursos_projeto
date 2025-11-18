from oferta import Oferta

class Turma(Oferta):
    """
Representa a Turma, como abstração da sala de aula física.

Responsabilidades:
    Retém os horários (dias e horários) das aulas, local da sala de aula, código de turma, estado da turma (Aberta, Fechada) e matriulas (Representação em lista dos alunos matriculados na turma). Permite a geração de estatísticas como: taxa de aprovação e distribuição de notas (Média, moda e mediana)
"""
    def __init__(self, codigo_curso:int, vagas:int, semestre:str, horarios:str, codigo_turma:int, estado_aberta:bool = False, matriculas:list = None,local:str = None,):
        pass