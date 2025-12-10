class Matricula:
    """
    Objeto que liga Aluno com uma Turma

    Responsabilidades:
        Retém os dados da ligação entre Aluno com a Turma como: notas, frequência e o estado da matrícula (Aprovado, Reprovado, Cursando).

        Ela permite o lançamento das notas do estudante, o cálculo da situação  final e trancamento.
    """
    def __init__(self, aluno:object, turma:object, notas:list = None, frequencia: float = 0.0,estado:str = "CURSANDO"):

        self.aluno = aluno
        self.turma = turma
        self.notas = notas
        self.frequencia = frequencia
        self.estado = estado

    @property
    def aluno(self):
        return self.__aluno
    
    @aluno.setter
    def aluno(self, valor):

        if not hasattr(valor, 'codigo_matricula'):
            raise TypeError("Aluno precisa ser passado como um objeto da classe Aluno.")
    
        self.__aluno = valor
    
    @property
    def turma(self):
        return self.__turma
    
    @turma.setter
    def turma(self, valor):

        if not hasattr(valor, 'vagas_totais'):
            raise TypeError("Turma precisa ser passado como um objeto da classe Turma")
        
        self.__turma = valor
    
    @property
    def notas(self):
        return self.__notas
    
    @notas.setter
    def notas(self, valor):

        if valor is None:
            self.__notas = []
            return

        if not isinstance(valor, list):
            raise TypeError("As notas devem ser passadas em formato de lista.")
        
        for nota in valor:
            if not isinstance(nota, (int, float)) or isinstance(nota, bool):
                raise TypeError("As notas passadas precisam ser números.")
            
            if nota < 0 or nota > 10:
                raise ValueError("As notas precisam estar entre 0 a 10.")
            
        self.__notas = valor
    
    @property
    def frequencia(self):
        return self.__frequencia
    
    @frequencia.setter
    def frequencia(self, valor):

        if not isinstance(valor, (int, float)):
            raise TypeError("A frequência passada precisa ser em números.")
        
        if valor < 0 or valor > 100:
            raise ValueError("A frequência passada precisa estar entre 0 a 100.")
        
        self.__frequencia = valor
    
    @property
    def estado(self):
        return self.__estado
    
    @estado.setter
    def estado(self, valor):

        if not isinstance(valor, str):
            raise TypeError("O valor do estado precisa ser em texto.")
        
        lista_estados = ["APROVADO","REPROVADO_POR_NOTA", "REPROVADO_POR_FREQUENCIA", "CURSANDO", "TRANCADA"]

        if valor.upper().strip() not in lista_estados:
            raise ValueError("Os valores de estado só podem ser: 'APROVADO'|'REPROVADO_POR_NOTA'|'REPROVADO_POR_FREQUENCIA'|'CURSANDO'|TRANCADA")
        
        self.__estado = valor.upper().strip()

    def trancar_matricula(self):
        if self.estado == "TRANCADA":
            raise TypeError("Matrícula já foi trancada.")
        
        self.estado = "TRANCADA"
        print("Matrícula trancada com sucesso.")

    def lancar_frequencia(self, nova_frequencia):

        if self.estado != "CURSANDO":
            raise ValueError("Matrícula não está em estado para lançamento de frequência.")
        
        self.frequencia = nova_frequencia

        print(f"Frequência atualizada para {self.frequencia:.1f}% com sucesso.")

    def lancar_nota(self, nota_adicionada):

        if self.estado != "CURSANDO":
            raise ValueError("Matrícula não está em estado para lançamento de notas.")
        
        if not isinstance(nota_adicionada, (int, float)) or isinstance(nota_adicionada, bool):
            raise TypeError("A nota deve ser um número.")
        
        if nota_adicionada < 0 or nota_adicionada > 10:
            raise ValueError(f"Nota inválida: {nota_adicionada}. Deve ser entre 0 e 10.")

        self.notas.append(nota_adicionada)

        print(f"Nota {nota_adicionada:.2f} adicionada com sucesso.") 

    def calcular_situacao(self, media_minima = 6.0, frequencia_minima = 75.0):
        """
        Calcula a situação final da matrícula do aluno.
        """

        if self.estado != "CURSANDO":
            raise ValueError("A situação do aluno já foi definida.")
        
        if not self.notas:
            raise ValueError("Não há notas lançadas para calcular a situação")
        
        media_arit = sum(self.notas) / len(self.notas)

        print(f"--- Calculando: Média Aluno: {media_arit:.2f} (Mínima: {media_minima}) | Freq Aluno: {self.frequencia}% (Mínima: {frequencia_minima}%) ---")

        if media_arit >= media_minima and self.frequencia >= frequencia_minima:
            self.estado = "APROVADO"
            print ("Aluno APROVADO!! :)")
            print(f"MÉDIA DE NOTA: {media_arit}\nFREQUÊNCIA: {self.frequencia}%")
            return
        
        if media_arit < media_minima and self.frequencia >= frequencia_minima:
            self.estado = "REPROVADO_POR_NOTA"
            print("Aluno reprovado por nota. Vai dar certo! )")
            print(f"MÉDIA DE NOTA: {media_arit}\nFREQUÊNCIA: {self.frequencia}%")
            return
        
        if media_arit >= media_minima and self.frequencia < frequencia_minima:
            self.estado = "REPROVADO_POR_FREQUENCIA"
            print("Aluno reprovado por frequência. Vai dar certo! Não desista.")
            print(f"MÉDIA DE NOTA: {media_arit}\nFREQUÊNCIA: {self.frequencia}%")
            return
        
        if media_arit < media_minima and self.frequencia < frequencia_minima:
            self.estado = "REPROVADO_POR_FREQUENCIA"
            print("Aluno reprovado por nota e frequência")
            print(f"MÉDIA DE NOTA: {media_arit}\nFREQUÊNCIA: {self.frequencia}%")
            return

    def __eq__(self, objeto):
        """
        Verifica se duas matrículas são iguais.
        Critério: Mesmo Aluno E Mesma Turma.
        """

        if not isinstance(objeto, Matricula):
            return False
        # Use getattr para evitar erro caso o objeto esteja incompleto
        cod_aluno_self = getattr(self.aluno, 'codigo_matricula', None)
        cod_turma_self = getattr(self.turma, 'codigo_turma', None)
        
        cod_aluno_other = getattr(objeto.aluno, 'codigo_matricula', None)
        cod_turma_other = getattr(objeto.turma, 'codigo_turma', None)

        return cod_aluno_self == cod_aluno_other and cod_turma_self == cod_turma_other

    def to_dict(self):
        return {
            "codigo_aluno": self.aluno.codigo_matricula,
            "codigo_turma": self.turma.codigo_turma,
            "notas": self.notas,
            "frequencia": self.frequencia,
            "estado": self.estado

        }