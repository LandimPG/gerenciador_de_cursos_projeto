class Curso:
    """
    Representa a definição estrutural de uma disciplina no catálogo da instituição.
    
    Responsabilidade:
        Armazenar os dados imutáveis da disciplina, como nome, carga horária e ementa.
        Define as regras acadêmicas de dependência através da lista de pré-requisitos
        (códigos de outros cursos necessários).
    """

    def __init__(self, nome:str, codigo_curso:int, carga_horaria:int, ementa:str, lista_pre_requisitos:list = None):

        self.nome = nome
        self.codigo_curso = codigo_curso
        self.carga_horaria = carga_horaria
        self.ementa = ementa

        if lista_pre_requisitos is None: #Parâmetro passado pelo usuário
            self.lista_pre_requisitos = []
        else:
            self.lista_pre_requisitos = lista_pre_requisitos

    @property
    def nome(self):
        return self.__nome
        
    @nome.setter
    def nome(self, valor):
        if not isinstance(valor, str):
            raise TypeError("O nome passado deve ser um texto.")
            
        if not len(valor.strip()) > 0:
            raise ValueError("O nome passado não pode ser vazio")
            
        self.__nome = valor.strip().title()

    @property
    def codigo_curso(self):
        return self.__codigo_curso
    
    @codigo_curso.setter
    def codigo_curso(self, valor):

        if not isinstance(valor, int):
            raise TypeError("O codigo de curso passado precisa ser um valor inteiro.")
        
        if valor <= 0:
            raise ValueError("O código de curso passado não pode ser nulo ou negativo.")
        
        self.__codigo_curso = valor

    @property
    def carga_horaria(self):
        return self.__carga_horaria

    @carga_horaria.setter
    def carga_horaria(self, valor):
        if not isinstance(valor, int):
            raise TypeError("A carga horária inserida precisa ter apenas números inteiros.")
        if valor == 0 or valor < 0:
            raise ValueError("A carga horária não pode ser nula")
        self.__carga_horaria = valor

    @property
    def ementa(self):
        return self.__ementa
    
    @ementa.setter
    def ementa(self,valor):
        if not isinstance(valor, str):
            raise TypeError("A ementa precisa ser passa em formato de texto.")
        
        self.__ementa = valor.strip()

    @property
    def lista_pre_requisitos(self):
        return self.__lista_pre_requisitos
    
    @lista_pre_requisitos.setter

    def lista_pre_requisitos(self,valor):

        if not isinstance(valor, list):
            raise TypeError("A lista de pré requisitos deve ser passada em formato de lista.")

        for item in valor:
            if not isinstance(item, int) or isinstance(item, bool):
                raise TypeError("Os valores passados nos itens da lista precisam ser inteiros.")
        
        for item in range(len(valor)): #Poderia apenas ter feito len(valor) != len(set(valor)) 
            for item2 in range(item + 1, len(valor)):
                if valor[item2] == valor[item]:
                    raise ValueError(f"Os Requisitos passados não podem ser iguais: o requisito {valor[item]} foi duplicado.")
                
        if hasattr(self, 'codigo_curso') and self.codigo_curso in valor:
            raise ValueError("O requisito do curso não pode ser o próprio curso.")

        self.__lista_pre_requisitos = valor

    def __str__(self):
        return f"""Nome do Curso: {self.nome}
Código do Curso: {self.codigo_curso}
Carga Horária: {self.carga_horaria} Horas
Ementa do Curso: {self.ementa}\n  
Lista de Pré-Requisitos: {self.lista_pre_requisitos}\n"""
