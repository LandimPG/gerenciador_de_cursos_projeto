from .pessoa import Pessoa

class Aluno(Pessoa):
    """
    Representa um estudante matriculado na instituição.
    
    Responsabilidade:
        Mantém a identidade única do aluno (matrícula) e todo o seu registro acadêmico.
        É responsável por armazenar tanto o histórico de disciplinas concluídas quanto
        as matrículas do semestre atual, além de fornecer métodos para cálculo de
        desempenho individual (como o CR).
    """

    def __init__(self, nome:str, email:str, codigo_matricula:int, historico:list = None, matriculas_atuais:list = None):
        
        super().__init__(nome, email)
        self.codigo_matricula = codigo_matricula
        self.historico = historico
        self.matriculas_atuais = matriculas_atuais


    @property
    def codigo_matricula(self):
        return self.__codigo_matricula
    
    @codigo_matricula.setter
    def codigo_matricula(self,valor):

        if not isinstance(valor, int):
            raise TypeError("O código de matrícula precisa ser um número inteiro.")
        
        if valor <= 0:
            raise ValueError("O código de matrícula não pode ser nulo ou negativo.")
        
        self.__codigo_matricula = valor
    
    @property
    def historico(self):
        return self.__historico
    
    @historico.setter
    def historico(self, valor):

        if valor is None:
            self.__historico = []
            return

        if not isinstance(valor, list):
            raise TypeError("O histórico deve ser passado como uma lista.")
        
        for item in valor:
            if not hasattr(item, 'notas') or not hasattr(item, 'estado'): #dúvida
                raise TypeError("O item passado na lista do histórico precisa ser um objeto de matrícula.")
        self.__historico = valor

    @property
    def matriculas_atuais(self):
        return self.__matriculas_atuais
    
    @matriculas_atuais.setter
    def matriculas_atuais(self,valor):

        if valor is None:
            self.__matriculas_atuais = []
            return

        if not isinstance(valor, list):
            raise TypeError("A lista de matriculas atuais precisa ser passado em formato de lista")
        
        for item in valor:
            if not hasattr(item, 'notas') or not hasattr(item, 'estado'):
                raise TypeError("As matrículas atuais passadas precisam ser um objeto da classe Matricula")
            
        self.__matriculas_atuais =valor

    def calcular_cr(self):
        
        print("CR sendo calculado com média aritmética.")
        soma_notas_finais = 0.0
        total_materias = 0
        #Fazendo o CR com média aritmética, depois atualizar para ponderada
        for matricula in self.historico:
            if matricula.notas:
                media_notas= sum(matricula.notas) / len(matricula.notas)
                soma_notas_finais += media_notas
                total_materias += 1

        if total_materias == 0:
            return 0.0
        
        return soma_notas_finais / total_materias

    def realizar_matricula(self, nova_matricula):
        """
        Adiciona uma nova matrícula à lista de atuais.
        """
        if not hasattr(nova_matricula, 'notas'):
            raise TypeError("O objeto precisa ser uma Matrícula válida.")

        if nova_matricula in self.matriculas_atuais:
            raise ValueError("O aluno já está matriculado nesta turma.")
        # Semana 3 e 4 precisa implementar veriifcações
        #   -Choque de horários, Vagas na turma, Pré-requisitos
        self.matriculas_atuais.append(nova_matricula)
        print("Aluno matriculado com sucesso.")

    def atualizar_historico(self):
        """
        Verifica as matrículas atuais. Se alguma estiver finalizada 
        (não está mais CURSANDO), move para o histórico.
        """
        if self.matriculas_atuais == []:
            print("Não há matrículas atuais para realizar a atualização do histórico.")
            return

        ainda_cursando = []

        for matricula in self.matriculas_atuais:
            if matricula.estado == "CURSANDO":
                ainda_cursando.append(matricula)

            else:
                self.historico.append(matricula)
                print(f"Disciplina concluída: {matricula.turma.codigo_curso} - Status: {matricula.estado}")
            
        self.matriculas_atuais = ainda_cursando

    
    def __lt__(self, outro):
        """
        Define a regra de ordenação (Menor Que / Less Than).
        Critério 1: CR (Menor CR vem primeiro).
        Critério 2: Nome (Ordem alfabética para desempate).
        """
       
        if not isinstance(outro, Aluno):
            # Retorna NotImplemented para o Python tentar outra forma ou dar erro
            return NotImplemented

        # Calcula os CRs para comparar
        meu_cr = self.calcular_cr()
        outro_cr = outro.calcular_cr()

        # A Comparação Principal (Pelo CR)
        if meu_cr != outro_cr:
            return meu_cr < outro_cr
        
        # Pelo Nome
        # Se os CRs são iguais, o Python desce para esta linha.
        # Retorna True se meu nome vem antes alfabeticamente.
        return self.nome < outro.nome
