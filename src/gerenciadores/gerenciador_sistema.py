import sys
import os
import json
from datetime import datetime

from src.academicos.curso import Curso
from src.academicos.turma import Turma
from src.usuarios.aluno import Aluno
from src.academicos.matricula import Matricula
from src.dados.persistencia import salvar_dado, carregar_dados

class GerenciadorSistema:
    """
    Controlador central do sistema (God`s view).
    """

    def __init__(self):
        # Carrega os dados assim que o sistema inicia
        self.alunos, self.cursos, self.turmas, self.matriculas = carregar_dados()
        
        self.configuracoes = self.carregar_configuracoes()

    def carregar_configuracoes(self):
        """
        Lê os arquivos do settings.json
        """

        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            root_dir = os.path.dirname(os.path.dirname(base_dir))
            settings_path = os.path.join(root_dir, "settings.json")

            with open (settings_path, "r", encoding="utf-8" ) as f:
                return json.load(f)
            
        except FileNotFoundError:
            print("Settings.json não foi encontrado. Usando formatações padrão")

            return {"data_limite_trancamento": "2099-12-31"}
        

    def salvar_tudo(self):
        salvar_dado(self.alunos, self.cursos, self.turmas, self.matriculas)

    # --- MÉTODOS DE BUSCA ---

    def buscar_curso(self, codigo_curso: int):
        for c in self.cursos:
            if c.codigo_curso == codigo_curso:
                return c
        return None
    
    def buscar_aluno(self, matricula: int):
        for a in self.alunos:
            if a.codigo_matricula == matricula:
                return a
        return None
    
    def buscar_turma(self, codigo_turma):
        str_buscado = str(codigo_turma).strip()

        for t in self.turmas:
            # Garante que converte o ID da turma para string sem espaços
            id_t = str(getattr(t, 'codigo_turma', '')).strip()
            
            if id_t == str_buscado:
                return t
        return None

    def buscar_matricula(self, cod_aluno: int, cod_turma: int):
        for m in self.matriculas:
            if m.aluno.codigo_matricula == cod_aluno and m.turma.codigo_turma == cod_turma:
                return m
        return None
    
    # --- MÉTODOS DE ESCRITA ---

    def criar_curso(self, nome, codigo_curso, horas, ementa, pre_requisitos = None):

        # Validar se já existe
        if self.buscar_curso(codigo_curso) is not None:
            raise ValueError(f"Já existe um curso com o código {codigo_curso}")
        
        for c in self.cursos:
            if c.nome.lower() == nome.strip().lower():
                raise ValueError(f"Já existe um curso com o nome: {nome}.")
            
        #Validação dos ids dos pré-requisitos.
        if pre_requisitos:
            for id_req in pre_requisitos:
                if self.buscar_curso(id_req) is None:
                    raise ValueError(f"Erro: O curso pré-requisito ID {id_req} ainda não existe no sistema.")


        novo_curso = Curso(nome, codigo_curso, horas, ementa, pre_requisitos)
        self.cursos.append(novo_curso)
        self.salvar_tudo()
        return novo_curso
    
    def criar_aluno(self, nome, email, matricula):
        if self.buscar_aluno(matricula) is not None:
            raise ValueError(f"Já existe um aluno com a matrícula: {matricula}.")
        
        novo_aluno = Aluno(nome, email, matricula)
        self.alunos.append(novo_aluno)
        self.salvar_tudo()
        return novo_aluno

    def criar_turma(self, cod_curso, cod_turma, vagas, semestre, local, horarios):
        curso = self.buscar_curso(cod_curso)
        
        # Correção Crítica: Validar se é None
        if curso is None:
            raise ValueError("Curso não encontrado.")
        
        if self.buscar_turma(cod_turma) is not None:
            raise ValueError(f"Já existe uma turma com o código: {cod_turma}")
        
        nova_turma = Turma(cod_curso, vagas, semestre, horarios, cod_turma, local=local, curso_obj=curso)
        nova_turma.abrir_turma()
        self.turmas.append(nova_turma)
        self.salvar_tudo()
        return nova_turma
    
    def realizar_matricula(self, cod_aluno, cod_turma):
        # 1. Busca Aluno
        aluno = self.buscar_aluno(cod_aluno)
        if aluno is None:
            raise ValueError(f"Aluno {cod_aluno} não encontrado.")
        
        # 2. Busca Turma
        turma = self.buscar_turma(cod_turma)
        
        # --- CORREÇÃO DO ERRO ---
        # Não usamos "if not turma", pois se len(turma) == 0 o Python acha que é False.
        # Usamos "if turma is None" para saber se a variável está vazia de verdade.
        if turma is None:
            raise ValueError(f"Turma {cod_turma} não encontrada.")
        
        curso = self.buscar_curso(turma.codigo_curso)

        for historico in aluno.historico:
            if historico.turma.codigo_curso == curso.codigo_curso and historico.estado == "APROVADO":
                 raise ValueError(f"O aluno já foi APROVADO na disciplina {curso.nome}. Não é possível cursar novamente.")
        
        if self.buscar_matricula(cod_aluno, cod_turma) is not None:
            raise ValueError(f"Aluno já matriculado nessa turma.")
        
        # É preciso ter o objeto curso para saber a lista de pré requisitos
        if curso:
            for historico in aluno.historico:
                # Se o aluno tem um registro dessa matéria no histórico E foi aprovado
                if historico.turma.codigo_curso == curso.codigo_curso and historico.estado == "APROVADO":
                    raise ValueError(f"O aluno já foi APROVADO na disciplina {curso.nome}. Não é possível cursar novamente.")
                

        if curso and curso.lista_pre_requisitos:
            for id_req in curso.lista_pre_requisitos:
                # Verifica se esse ID está no histórico do aluno COMO APROVADO
                aprovado = False
                for hist in aluno.historico:
                    if hist.turma.codigo_curso == id_req and hist.estado == "APROVADO":
                        aprovado = True
                        break
                
                # Se rodou todo o histórico e não achou o pré-requisito aprovado:
                if not aprovado:
                    # Busca o nome do curso pré-requisito só para mostrar na mensagem
                    req_obj = self.buscar_curso(id_req)
                    nome_req = req_obj.nome if req_obj else str(id_req)
                    raise ValueError(f"Pré-requisito não atendido: O aluno precisa ser aprovado em {nome_req} (ID {id_req}) antes.")
                
        # Verificar Duplicidade de vagas
        if self.buscar_matricula(cod_aluno, cod_turma) is not None:
            raise ValueError("Aluno já matriculado nessa turma.")

        nova_matricula = Matricula(aluno, turma)

        turma.adicionar_matricula(nova_matricula) #Valida vagas
        aluno.realizar_matricula(nova_matricula)  #VAlida choque de horário

        self.matriculas.append(nova_matricula)
        self.salvar_tudo()
        return nova_matricula
    
    def processar_notas(self, cod_aluno, cod_turma, nota):
        matricula = self.buscar_matricula(cod_aluno, cod_turma)
        if matricula is None:
            raise ValueError("Matrícula não encontrada.")
        
        matricula.lancar_nota(nota)
        self.salvar_tudo()
        return matricula
    
    def processar_frequencia(self, cod_aluno, cod_turma, frequencia):
        matricula = self.buscar_matricula(cod_aluno, cod_turma)
        if matricula is None:
            raise ValueError("Matrícula não encontrada")
        matricula.lancar_frequencia(frequencia)
        self.salvar_tudo()
        return matricula
    
    def processar_calculo_situacao(self, cod_aluno, cod_turma):

        matricula = self.buscar_matricula(cod_aluno, cod_turma)

        if matricula:
            nota_minima = self.configuracoes.get("nota_minima_aprovacao", 6.0)
            frequencia_minima = self.configuracoes.get("frequencia_minima_aprovacao", 75.0)
            matricula.calcular_situacao(nota_minima, frequencia_minima)
            return matricula.estado
        
        return None
    
    def processar_trancamento(self, cod_aluno, cod_turma):
        """
        Muda o estado de matrícula para TRANCADA chamando o método
        trancar_matricula
        """
        matricula = self.buscar_matricula(cod_aluno, cod_turma)
        if matricula is None:
            raise ValueError("Matrícula não encontrada.")
        
        data_limite_str = self.configuracoes.get("data_limite_trancamento")

        if data_limite_str:
            data_limite = datetime.strptime(data_limite_str, "%Y-%m-%d")
            data_hoje = datetime.now()

            if data_hoje > data_limite:
                raise ValueError("Erro! Data limite de trancamento foi excedida ")

        matricula.trancar_matricula()
        self.salvar_tudo()
        return matricula
    
    def ver_situacao_aluno(self, cod_aluno, cod_turma):
        """
        Calcula a situação do aluno por meio do método calcular_situacao
        em matricula.py
        """

        matricula = self.buscar_matricula(cod_aluno, cod_turma)
        if matricula is None:
            raise ValueError("Matrícula não foi encontrada.")
        
        #Conseguir as informações do seetings.json
        nota_minima = self.configuracoes.get("nota_minima_aprovacao", 6.0)
        frequencia_minima = self.configuracoes.get("frequencia_minima_aprovacao", 75.0)


        # verifica notas/frequência e muda o status para APROVADO ou REPROVADO
        matricula.calcular_situacao(media_minima = nota_minima, frequencia_minima = frequencia_minima)

        if matricula.estado != "CURSANDO":
            #Remove das matriculas atuais
            if matricula in matricula.aluno.matriculas_atuais:
                matricula.aluno.matriculas_atuais.remove(matricula)

            if matricula not in matricula.aluno.historico:
                matricula.aluno.historico.append(matricula)

        self.salvar_tudo()
        return matricula.estado
    
    def relatorio_alunos_em_risco(self, cod_turma):
        """
        Lista alunos de uma turma específica que estão com nota abaixo da média ou
        frequência abaixo da mínima e que ainda estão cursando.
        """

        turma = self.buscar_turma(cod_turma)
        if turma is None:
            raise ValueError("Turma não encontrada.")
        
        min_nota = self.configuracoes.get("nota_minima_aprovacao", 6.0)
        min_frequencia = self.configuracoes.get("frequencia_minima_aprovacao", 75)

        alunos_risco = []

        for m in turma.matriculas:
            if m.estado == "CURSANDO":

                media_atual = sum(m.notas) / len(m.notas) if m.notas else 0.0

                if media_atual < min_nota or m.frequencia < min_frequencia:
                    alunos_risco.append({
                        "nome": m.aluno.nome,
                        "matricula": m.aluno.codigo_matricula,
                        "media_atual": media_atual,
                        "frequencia": m.frequencia,
                        "motivo": []
                    })

                if media_atual < min_nota:
                    alunos_risco[-1]["motivo"].append(f"Nota abaixo da média. Nota: ({media_atual:.2f}) | Nota Mínima: ({min_nota})")
                if m.frequencia < min_frequencia:
                    alunos_risco[-1]["motivo"].append(f"Frequência abaixo da média. Freq: ({m.frequencia}%) | Freq Mínima: {min_frequencia}%")

        return turma, alunos_risco
    

    def relatorio_top_alunos(self, top_n = 5):
        """
        Retorna os N melhores alunos baseados no CR (Coeficiente de Rendimento.)
        Utiliza do método __lt__ da classe Aluno para ordenar.
        """

        if not self.alunos:
            return []
        
        alunos_ordenados = sorted(self.alunos, key =lambda a: a.calcular_cr(), reverse=True)

        return alunos_ordenados[:top_n]
    

    def remover_curso(self, cod_curso):
        curso = self.buscar_curso(cod_curso)

        if not curso:
            raise ValueError("Curso não encontrado.")
        
        #Não apaga o curso se tiver turmas o usando
        for t in self.turmas:
            if t.codigo_curso == cod_curso:
                raise ValueError("Não é possível excluir, pois existem turmas vinculadas a esse curso.")
            
        self.cursos.remove(curso)
        self.salvar_tudo()

    def editar_curso(self, cod_curso, novo_nome = None, nova_carga = None, novos_pre_reqs = None):
        curso = self.buscar_curso(cod_curso)
        if not curso:
            raise ValueError("Curso não encontrado")
        
        if novo_nome: curso.nome = novo_nome
        if nova_carga: curso.carga_horaria = nova_carga

        if novos_pre_reqs is not None:

            # O curso não pode ser pré-requisito para ele mesmo:
            if cod_curso in novos_pre_reqs:
                raise ValueError("O curso não pode ser pré-requisito dele mesmo.")
            
            # Os ids passados precisam existir no sistema:

            for id_req in novos_pre_reqs:
                if self.buscar_curso(id_req) is None:
                    raise ValueError(f"Erro: O curso pré-requisito ID {id_req} não existe.")
                
            curso.lista_pre_requisitos = novos_pre_reqs

        return curso
    
    def remover_aluno(self, matricula):
        aluno = self.buscar_aluno(matricula)
        if not aluno:
            raise ValueError("Aluno não encontrado")
        
        if aluno.matriculas_atuais or aluno.historico:
            raise ValueError("Não é possível excluir: Aluno possui vínculos acadêmicos.")
        
        self.alunos.remove(aluno)
        self.salvar_tudo()
        return True
    
    def editar_aluno(self, matricula_atual, novo_nome = None, novo_email = None, nova_matricula = None):

        aluno = self.buscar_aluno(matricula_atual)

        if not aluno:
            raise ValueError("Aluno não encontrado")
        
        if novo_nome:
            aluno.nome = novo_nome

        if novo_email:
            aluno.email = novo_email

        if nova_matricula is not None and nova_matricula != matricula_atual:

            if self.buscar_aluno(nova_matricula) is not None:
                raise ValueError(f"Não é possível alterar: Já existe um aluno com a matrícula {nova_matricula}.")
            

            aluno.codigo_matricula = nova_matricula
        self.salvar_tudo()
        return aluno
    
    
    #Gestão de turmas

    def editar_turma(self, cod_turma, novo_local = None, novas_vagas = None):

        turma = self.buscar_turma(cod_turma)
        if not turma:
            raise ValueError("Turma não encontrada")
        
        if novo_local:
            turma.local = novo_local

        if novas_vagas:

            if novas_vagas < len(turma.matriculas):
                raise ValueError(f"Não é possível reduzir para {novas_vagas} vagas. Já existem {len(turma.matriculas)} alunos matriculados.")
            turma.vagas_totais = novas_vagas

        return turma
    
    def excluir_turma(self, cod_turma):
        turma = self.buscar_turma(cod_turma)
        
        if turma is None: # Melhor que "if not turma"
            raise ValueError("Turma não encontrada")
        
        # Validação de alunos (Isso pode ser o que está impedindo, mas daria outra msg de erro)
        if len(turma.matriculas) > 0:
            raise ValueError("Não é possível excluir: Existem alunos matriculados nessa turma. Remova matrículas primeiro")
        
        self.turmas.remove(turma)
        self.salvar_tudo() # Auto-save para segurança
        return True
    
    def alterar_estado_turma(self, cod_turma, acao):
        """
        acao: 'abrir' ou 'fechar'
        """

        turma = self.buscar_turma(cod_turma)
        if not turma:
            raise ValueError("Turma não encontrada.")
        

        if acao == "abrir":
            turma.abrir_turma()

        elif acao == "fechar":
            turma.fechar_turma()

        


