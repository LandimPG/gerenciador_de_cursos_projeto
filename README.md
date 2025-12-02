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

## ===== UML TEXTUAL =====


**1. Classe Curso**  
   - Atributos:  
             - `nome`  
             - `codigo_curso`  
             - `carga_horaria`  
             - `lista_pre_requisitos`  
             - `ementa`  
             - **Método Especial**: - `__str__` (Retorna resumo textual do curso)
     
**2. Classe Oferta (Classe Base)**  
   
   - Atributos:  
             - `codigo_curso`  
             - `vagas_totais`  
             - `semestre`  

**3. Classe Turma (Herda da Classe Oferta)**  
   
   - Atributos:  
         - `horarios`       (Contém em forma de dicionário os dias e os horários das aulas.)  
         - `local`  
         - `codigo_turma`  
         - `estado_aberta`  (Identifica se a turma se encontra aberta (True) ou fechada (False))  
         - `matriculas`     (lista de objetos da Classe Matricula)  
     
   - Métodos:  
             - `abrir_turma` (muda "estado_aberta" para True)  
             - `fechar_turma` (muda "estado_aberta" para False)  
             - `listar_alunos` (mostra a lista de alunos)  
             - `adicionar_matricula` (Recebe um objeto Matrícula e adiciona à lista da turma, se houver vagas disponíveis.)  
             - `ver_taxa_aprovacao_turma` (Calcula a taxa de aprovação com base na lista matrículas)  
             - `ver_distribuicao_notas` (Calcula com base na lista matrículas)  
             - **Método Especial**: - `__len__` (Retorna a quantidade de alunos matriculados)  
     
**4. Classe Pessoa (Classe Base)**
     
   - Atributos:  
             - `nome`  
             - `email`  
   
**5. Classe Aluno (Herda da Classe Pessoa)**
     
   - Atributos:  
             - `codigo_matricula`  
             - `historico`         (lista de objetos de matricula não ativas)
             - `matriculas_atuais` (lista de objetos de matricula ativas)
     
   - Métodos:
             - `realizar_matricula`   (Adiciona uma nova matrícula à lista de atuais.) 
             - `atualizar_historico`  (Verifica as matrículas atuais. Se alguma estiver finalizada, [não está mais CURSANDO], move para o histórico.)  
             - `calcular_cr`  (Calculo do coeficiente de rendimento do aluno)  
             - **Método Especial**: - `__lt__` (Permite ordenar alunos pelo CR para relatórios Top N)  
     
**6. Classe Matricula**
     
   - Atributos:  
             - `aluno` (Objeto da Classe Aluno)  
             - `turma` (Objeto da Classe Turma)  
             - `notas`  
             - `frequencia`  
             - `estado`  (Define o estado da matrícula entre ([APROVADO'|'REPROVADO_POR_NOTA'|'REPROVADO_POR_FREQUENCIA'|'CURSANDO'|TRANCADA]) caso o aluno seja                             reprovado por nota e por frequência o sistema define que reprovou por frequência.)
     
   - Métodos:  
             - `trancar_matricula`  
             - `lancar_frequencia`  
             - `lancar_nota`  
             - `calcular_situacao`  (Calcula o estado da matricula atual e muda o atributo `estado`)
             - **Método Especial**: - `__eq__` (Verifica igualdade para impedir duplicação de matrícula)
     
**7. Sistema / Interface CLI (Arquivo main.py)**
   *(Responsável pela orquestração e gerenciamento das listas globais)*  
   
   - Métodos de Gerenciamento (CRUD):  
             - `cadastrar_aluno`  
             - `cadastrar_curso`  
             - `novar_turma` (cria objeto Turma)
             - `realizar_matricula` (cria objeto Turma)  
             - `buscar_matricula`  (Método auxiliar)
             - `lancar_notas`  
             - `lancar_frequencia`  
             - `listas_gerais`  
           

   - Métodos de Relatórios Globais:  
             - `gerar_relatorio_top_n_alunos` (Ordena todos os alunos por CR)  
             - `gerar_relatorio_alunos_em_risco` (Verifica todas as matrículas ativas)
     
  ## ===== RELACIONAMENTOS ======  
  
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


## ===== Estrutura de Arquivos =====

   Organização dos arquivos do projeto

   ```text
   /gerenciador_de_cursos_projeto
   │
   ├── src/                    <-- Suas pastas de código
   │   ├── academicos/
   │   │   ├──oferta.py           # Classe base: Oferta
   │   │   ├── curso.py           # Classe: Curso
   │   │   ├── turma.py           # Classe: Turma (Herda de Oferta)
   │   │   └── matricula.py       # Classe: Matricula (Associa Aluno e Turma)
   │   └── dados/
   │       └── persistencia.py     # Módulo responsável por Salvar/Carregar JSON
   │
   │   └── usuarios/
   │       ├── aluno.py        # Classe: Aluno (Herda de Pessoa)
   │       └── pessoa.py       # Classe base: Pessoa
   │
   ├── main.py                 # Arquivo principal
   ├── test_classes.py         # arquivo de testes (pytest)
   ├──.gitignore               # Arquivos e pastas ignorados pelo Git (ex: __pycache__)
   └── README.md               # Documentação do projeto e UML Textual

```
## ===== Como Executar =====

### Pré-requisitos
* Python 3.x
* Pytest (para rodar os testes unitários)

### Instalação das dependências
Caso não tenha o pytest instalado:
```bash
pip install pytest

