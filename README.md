# gerenciador_de_cursos_projeto
Projeto para a disciplina de poo da UFCA

## ===== Descrição do Projeto =====  

Este projeto, intitulado **"Gerenciador de Cursos e Alunos"**   
consiste no desenvolvimento de um sistema de linha de comando (CLI) para administração acadêmica.

O sistema será responsável por gerenciar quatro entidades principais:  
cursos, turmas, alunos e matrículas. Suas funcionalidades centrais incluem o controle de pré-requisitos para inscrição, detecção de choque de horário,   gerenciamento de limite de vagas por turma, e o acompanhamento de frequência e notas dos alunos.  
Além disso, o sistema deverá gerar relatórios acadêmicos e persistir os dados em formato JSON ou SQLite.

## ===== Objetivo =====  

O objetivo principal deste projeto é aplicar de forma prática os conceitos fundamentais da Programação Orientada a Objetos (POO).

O foco não está na interface, mas sim na correta implementação de:

 - Encapsulamento
 - Herança
 - Métodos Especiais
 - O gerenciamento das relações entre múltiplas classes 

## ====== UML TEXTUAL =======


**1. Classe Curso**  
   - Atributos:  
             - `nome`  
             - `codigo_curso`  
             - `carga_horaria`  
             - `lista_pre_requisitos`  
             - `ementa`  
     
**2. Classe Oferta (Classe Base)**  
   
   - Atributos:  
             - `codigo_curso`  
             - `vagas`  
             - `semestre`  

**3. Classe Turma (Herda da Classe Oferta)**  
   
   - Atributos:  
         - `horarios`  
         - `local`  
         - `codigo_turma`  
         - `estado_aberta`  
         - `matriculas` (lista de objetos da Classe Matricula)
     
   - Métodos:  
             - `abrir_turma` (muda "estado_aberta" para True)  
             - `fechar_turma` (muda "estado_aberta" para False)  
             - `listar_alunos` (mostra a lista de alunos)  
             - `ver_taxa_aprovacao_turma` (Calcula a taxa de aprovação com base na lista matrículas)  
             - `ver_distribuicao_notas` (Calcula com base na lista matrículas)  
             
**4. Classe Pessoa (Classe Base)**
     
   - Atributos:  
             - `nome`  
             - `email`  
   
**5. Classe Aluno (Herda da Classe Pessoa)**
     
   - Atributos:  
             - `matricula_id`  
             - `historico`  
             - `matriculas_atuais` (lista de matriculas ativas)
     
   - Métodos:  
             - `calcular_cr`  
     
**6. Classe Matricula**
     
   - Atributos:  
             - `aluno` (Objeto da Classe Aluno)  
             - `turma` (Objeto da Classe Turma)  
             - `notas`  
             - `frequencia`  
             - `estado`
     
   - Métodos:  
             - `trancar_matricula`  
             - `lancar_frequencia`  
             - `lancar_nota`  
             - `calcular_situacao`
     
  ## ====== RELACIONAMENTOS =======  
  
**1. Herança:**  
   - `Aluno` --|> `Pessoa`  (Aluno é uma Pessoa)
   - `Turma` --|> `Oferta`  (Turma é uma Oferta)  

**2. Associação:**  
   - `Aluno` "1" --- "N" `Matricula`  
     (Um Aluno pode ter várias Matrículas no histórico ou atuais)
  
   - `Turma` "1" --- "N" `Matricula`  
     (Uma Turma contém várias Matrículas de alunos diferentes)  
     
   - `Matricula` --- `Aluno` e `Turma`  
     (A Matrícula conecta EXATAMENTE 1 Aluno a 1 Turma)  
  
   - `Turma` "N" --> "1" `Curso`  
     (Várias Turmas podem ser ofertadas para o mesmo Curso)
  
**3. Auto-Relacionamento**  
   - `Curso` "1" --> "N" `Curso`  
     (Um Curso pode ter vários outros Cursos como pré-requisito)  
