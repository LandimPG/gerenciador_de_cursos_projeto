import re
import statistics


from .oferta import Oferta

class Turma(Oferta):
    """
Representa a Turma, como abstração da sala de aula física.

Responsabilidades:
    Retém os horários (dias e horários) das aulas, local da sala de aula, código de turma, estado da turma (Aberta, Fechada) e matriulas (Representação em lista dos alunos matriculados na turma). Permite a geração de estatísticas como: taxa de aprovação e distribuição de notas (Média, moda e mediana)
"""

    def __init__(self, codigo_curso:int, vagas_totais:int, semestre:str, horarios:dict, codigo_turma:int, estado_aberta:bool = False, matriculas:list = None,local:str = None):

        super().__init__(codigo_curso, vagas_totais, semestre)
        self.horarios = horarios
        self.codigo_turma = codigo_turma
        self.estado_aberta = estado_aberta
        self.matriculas = matriculas
        self.local = local

#Encapsulamento e property

    @property
    def horarios(self):
        return self.__horarios
    
    @horarios.setter
    def horarios(self, valor):
        if not isinstance(valor, dict):
            raise TypeError("Os horários devem ser passados em formato de dicionário.")
        
        if len(valor) == 0:
            raise ValueError("A turma precisa ter ao meno um hoário definido")
        
        horarios_padronizados = {}

        formato_dia = r"^(seg|ter|qua|qui|sex|sab|dom)$"
        
        formato_horario = r"^\d{2}:\d{2}\-\d{2}:\d{2}$"

        for dia, horario in valor.items():
            if not re.match(formato_dia, dia, re.IGNORECASE):
                raise ValueError(f"O formato do(s) dia(s) deve ser por ex: ter, qua...")

            if not isinstance(horario, str) or not re.match(formato_horario, horario):
                raise ValueError(f"O formato do(s) horário(s) deve ser por ex: 10:00-12:00 e precisa ser uma string")
            
            horarios_padronizados[dia.lower()] = horario

        self.__horarios = horarios_padronizados

    @property
    def estado_aberta(self):
        return self.__estado_aberta
    
    @estado_aberta.setter
    def estado_aberta(self,valor):
        if not isinstance(valor, bool):
            raise TypeError("O valor de estado da turma precisa ser um valor booleano (True ou False)")
        
        self.__estado_aberta = valor

    @property
    def matriculas(self):
        return self.__matriculas
    
    @matriculas.setter
    def matriculas(self, valor):

        if valor is None:
            self.__matriculas = []
            return
        
        if not isinstance(valor, list):
            raise TypeError("A lista de matrículas devem ser passadas em formato de lista.")
        for matricula in valor:
            if not hasattr(matricula, 'aluno') or not hasattr(matricula, 'turma'):
                raise TypeError("As matrículas precisam ser objetos da classe Matrícula.")

        self.__matriculas = valor

    @property
    def local(self):
        return self.__local
    
    @local.setter
    def local(self,valor):

        if valor is None:
            self.__local = "Local não informado."
            return

        if not isinstance(valor, str):
            raise TypeError("O local da turma precisa ser passado como uma string.")
        
        formato = r'^[A-Z]{1}\d{2}$'

        if not re.match(formato, valor, re.IGNORECASE):
            raise ValueError("O local deve ser passado como: A01, A02, A33...")
        self.__local = valor.upper()
 
#Métodos da Classe Turma
    def abrir_turma(self):
        if self.estado_aberta:
            print("A turma já está aberta.")
            return
        
        self.estado_aberta = True
        print("A turma foi aberta com sucesso")

    def fechar_turma(self):
        if not self.estado_aberta:
            print("A turma já está fechada.")
            return
        
        self.estado_aberta = False
        print("A turma foi fechada com sucesso")

    def listar_alunos(self):
        if len(self.matriculas) == 0:
            print("Não há alunos matriculados na turma.")
            return
        
        print(f"--- Lista de Alunos {len(self)}/{self.vagas_totais}")

        for cont, matricula in enumerate(self.matriculas, start=1):

            print(f"{cont}° aluno: {matricula.aluno.nome}")

            """Finalizar após terminar classe Aluno e Classe Matricula"""

    def adicionar_matricula(self, nova_matricula):
        """
        Recebe um objeto Matrícula e adiciona à lista da turma,
        se houver vagas disponíveis.
        """
        if not hasattr(nova_matricula, 'aluno'):
            raise TypeError("O objeto passado não é uma Matrícula válida.")

        #Validação de Capacidade 
        if len(self) >= self.vagas_totais:
            raise ValueError(f"Turma lotada! Capacidade máxima de {self.vagas_totais} alunos atingida.")

        if nova_matricula in self.matriculas:
            raise ValueError("Este aluno já está matriculado nesta turma.")

        self.matriculas.append(nova_matricula)
        return True
    
    #ALERTA
    def ver_taxa_aprovacao_turma(self):

        """Calcula a taxa de aprovação (Porcentagem de alunos com status de Aprovado
        com relação à turma específica.)"""

        total_alunos = len(self.matriculas)

        if total_alunos == 0:
            return 0.0
        
        qtd_aprovados = sum(1 for m in self.matriculas if m.estado == "APROVADO")

        taxa_aprov = (qtd_aprovados/total_alunos) * 100
        return round(taxa_aprov, 2)
    


    #Ainda em Alerta
    def ver_distribuicao_notas(self):
        
        """Calcula as estastísiticas das notas dos alunos,
        como: Média, mediana e Desvio Padrão
        """
        medias_finais = []

        for matricula in self.matriculas:
            if matricula.notas:
                media_aluno = sum(matricula.notas) / len(matricula.notas)
                medias_finais.append(media_aluno)

        if not medias_finais:
            return None


        dados =  {
            "media_geral": round(statistics.mean(medias_finais), 2),
            "mediana": round(statistics.median(medias_finais), 2),
            "maior_nota": round(max(medias_finais), 2),
            "menor_nota": round(min(medias_finais), 2),
            "desvio_padrao": 0.0
        }

        if len(medias_finais) > 1:
            dados["desvio_padrao"] = round(statistics.stdev(medias_finais), 2)

        return dados


    def __len__(self):
        return len(self.matriculas)
    

    def to_dict(self):
        """
        Transforma o objeto Curso em um dicionário para salvar no JSON.
        """
        return {
            "codigo_curso": self.codigo_curso,
            "vagas_totais": self.vagas_totais,
            "semestre": self.semestre,
            "horarios": self.horarios,
            "codigo_turma": self.codigo_turma,
            "estado_aberta": self.estado_aberta,
            "local": self.local
        }

    @classmethod
    def from_dict(cls, dados):
        local_salvo = dados.get("local")
        if local_salvo == "Local não informado.":
            local_salvo = None

        return cls(
            codigo_curso = int(dados["codigo_curso"]),  # Força Inteiro
            vagas_totais = int(dados["vagas_totais"]),  # Força Inteiro
            semestre = dados["semestre"], 
            horarios = dados.get("horarios", {}), 
            codigo_turma = int(dados["codigo_turma"]),  # Força Inteiro (Essencial!)
            estado_aberta = dados["estado_aberta"], 
            matriculas = [],
            local = local_salvo
        )