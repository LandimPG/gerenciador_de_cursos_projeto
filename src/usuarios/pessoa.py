class Pessoa:
    """
    Classe base que representa uma entidade humana genérica no sistema acadêmico.
    
    Responsabilidade:
        Centralizar os atributos comuns (nome e contato) para utilizar os conceitos de
        herança em classes como Aluno.
    """

    def __init__(self, nome:str, email:str):
        self.nome = nome
        self.email = email

    @property
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self, valor):
        if not isinstance(valor, str):
            raise TypeError("O nome passado deve ser uma string.")
        
        if not len(valor.strip()) > 0:
            raise ValueError("Nome inserido para 'pessoa' precisa mais que 0 caracteres.")
        
        self.__nome = valor.strip().title()
    
    @property
    def email(self):
        return self.__email
    
    @email.setter
    def email(self, valor):
        if not isinstance(valor, str): 
            raise TypeError("O tipo passado para email precisa ser uma -string- ")
        
        partes = valor.split('@')

                    #poderia colocar apenas or not partes[0], pois quando for vazio, ele entende "" como falso e colocando not "" ele dá como verdadeiro e entra no if
        if len(partes) != 2 or len(partes[1]) == 0  or len(partes[0]) == 0:
            raise ValueError("Email inserido foi inválido.")

        self.__email = valor.strip()
    
    