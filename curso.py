class Curso:
    """
    Representa a definição estrutural de uma disciplina no catálogo da instituição.
    
    Responsabilidade:
        Armazenar os dados imutáveis da disciplina, como nome, carga horária e ementa.
        Define as regras acadêmicas de dependência através da lista de pré-requisitos
        (códigos de outros cursos necessários).
    """
    def __init__(self, nome:str, codigo_curso:int, carga_horaria:int, ementa:str, lista_pre_requisitos:list = None):
        pass