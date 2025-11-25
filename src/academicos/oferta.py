import re

class Oferta:
    """
     Classe base que representa a oferta de turmas
     dentro do sistema acadêmico.

     Responsabilidade:
        centralizar os atributos comuns como,
        codigo de curso, vagas e semestre ofertado para utilizar os conceitos de herança como a classe turma        
    
    """
    def __init__(self, codigo_curso:int, vagas_totais:int, semestre:str):
        
        self.codigo_curso = codigo_curso
        self.vagas_totais = vagas_totais
        self.semestre = semestre

    @property
    def codigo_curso(self):
        return self.__codigo_curso
    
    @codigo_curso.setter
    def codigo_curso(self,valor):
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise TypeError("O código de curso precisa ser um número inteiro.")
        if valor <= 0:
            raise ValueError("O código do curso não pode ser nulo ou negativo.")
        
        self.__codigo_curso = valor

    @property
    def vagas_totais(self):
        return self.__vagas_totais
        
    @vagas_totais.setter
    def vagas_totais(self, valor):

        if not isinstance(valor, int) or isinstance(valor, bool):
            raise TypeError("A quantidade de vagas precisa ser um número inteiro.")

        if valor < 0:
            raise ValueError("A quantidade de vagas totais não podem ser negativas.")
            
        self.__vagas_totais = valor

    @property
    def semestre(self):
        return self.__semestre
    
    @semestre.setter
    def semestre(self, valor):
        if not isinstance(valor, str):
            raise TypeError("O semestre inserido precisa ser uma string.")
        
        formato = r"^\d{4}\.\d{1}$"

        if not re.match(formato, valor.strip()):
            raise ValueError("O semestre deve ser passado no seguinte formato: AAAA.S (EX: 2025.1)")

        self.__semestre = valor.strip()
        