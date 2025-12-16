# 🎓 Sistema de Gerenciamento de Cursos e Alunos (SGA)

> Projeto final desenvolvido para a disciplina de Programação Orientada a Objetos (POO) da Universidade Federal do Cariri (UFCA).

---

## 📝 Descrição do Projeto

Este projeto consiste em um sistema de linha de comando (CLI) robusto para a administração acadêmica. O sistema permite o gerenciamento completo do ciclo de vida acadêmico, desde a criação de cursos e turmas até a matrícula de alunos, lançamento de notas/frequência e geração de histórico escolar.

O foco principal do desenvolvimento foi a aplicação prática dos pilares da **Orientação a Objetos**, garantindo um código modular, seguro e persistente.

---

## 🚀 Funcionalidades Principais

### 1. Gestão de Cursos
* Cadastro de cursos com validação de carga horária.
* **Sistema de Pré-requisitos:** Impede que um curso seja pré-requisito dele mesmo e valida se os requisitos existem.
* Edição e exclusão lógica (impede exclusão se houver turmas vinculadas).

### 2. Gestão de Turmas
* Abertura de turmas com definição de **Local** (Validação via Regex: ex `A01`) e **Horários**.
* Controle de **Vagas**: Impede matrículas em turmas lotadas.
* Alteração de estado: Abrir ou Fechar turmas para novas matrículas.

### 3. Gestão Acadêmica (O Coração do Sistema)
* **Matrícula Inteligente:**
    *  **Bloqueio por Choque de Horário:** O sistema detecta se o aluno já tem aula naquele dia/hora.
    *  **Bloqueio por Pré-requisito:** Verifica se o aluno cumpriu as matérias necessárias no histórico.
    *  **Bloqueio de Duplicidade:** Impede matricular o aluno na mesma turma ou curso já aprovado.
* **Ciclo de Vida:**
    * Lançamento de Notas (0-10) e Frequência (0-100%).
    * Cálculo automático de situação (Aprovado, Reprovado por Nota/Frequência).
    * Migração automática de "Matrícula Atual" para "Histórico Escolar".
    * Trancamento de matrícula (respeitando datas limites configuráveis).

### 4. Relatórios e Estatísticas
* 📊 **Alunos em Risco:** Identifica alunos com notas ou frequência abaixo da média antes do fim do semestre.
* 🏆 **Top Alunos (CR):** Ranking dos melhores alunos baseado no cálculo ponderado do Coeficiente de Rendimento.
* 📈 **Estatísticas da Turma:** Média geral, desvio padrão, melhor e pior nota da turma.

### 5. Interface e Usabilidade
* Interface colorida (ANSI Colors) para melhor experiência do usuário (Erros em vermelho, Sucessos em verde, Alertas em amarelo).
* Entradas de dados tratadas para evitar quebra do programa (Tratamento de Exceções).
* **Persistência Automática:** Todos os dados são salvos em `banco_dados.json` a cada alteração crítica.

---

## 🛠️ Conceitos de POO Aplicados

O projeto foi construído para demonstrar domínio sobre:

1.  **Herança:**
    * `Aluno` herda de `Pessoa`.
    * `Turma` herda de `Oferta`.
2.  **Encapsulamento:**
    * Uso extensivo de `@property` e `@setter` para validação de dados (ex: não aceitar notas negativas, validar formato de e-mail e semestre).
    * Atributos privados (ex: `__matriculas`, `__notas`).
3.  **Polimorfismo:**
    * Sobrescrita de métodos mágicos como `__str__` (representação textual), `__eq__` (comparação de igualdade) e `__lt__` (ordenação de alunos pelo CR).
    * Métodos `to_dict` e `from_dict` em todas as classes para serialização JSON.
4.  **Associação e Composição:**
    * A classe `Matricula` atua como classe associativa ligando `Aluno` e `Turma`.
    * `GerenciadorSistema` compõe todas as listas e orquestra as regras de negócio.

---

## 📐 Estrutura do Projeto (UML Textual Resumido)

### 1. Entidades Base
* **Pessoa:** `nome`, `email`.
* **Oferta:** `codigo_curso`, `vagas`, `semestre`.

### 2. Entidades Principais
* **Aluno (Pessoa):**
    * `matricula`, `historico`, `matriculas_atuais`.
    * Métodos: `calcular_cr()`, `realizar_matricula()`, `verif_choque_horario()`.
* **Turma (Oferta):**
    * `horarios`, `local`, `estado_aberta`, `lista_matriculas`.
    * Métodos: `ver_taxa_aprovacao()`, `ver_distribuicao_notas()`.
* **Curso:**
    * `nome`, `carga_horaria`, `ementa`, `pre_requisitos`.
* **Matricula (Associação):**
    * `aluno`, `turma`, `notas`, `frequencia`, `estado`.
    * Métodos: `calcular_situacao()`, `lancar_nota()`.

### 3. Controle
* **GerenciadorSistema:** Classe "Deus" que carrega/salva JSON e contém as regras de negócio globais (ex: impedir deletar curso com aluno matriculado).
* **MenuCli:** Interface visual que captura inputs, trata erros e chama o Gerenciador.

---

## 📂 Organização de Arquivos

```text
/gerenciador_de_cursos
│
├── main.py                 # Ponto de entrada (Inicializa o sistema e o Menu)
├── banco_dados.json        # Persistência de dados (Gerado automaticamente)
├── settings.json           # Configurações (ex: data limite trancamento)
│
└── src/
    ├── academicos/
    │   ├── curso.py
    │   ├── matricula.py
    │   ├── oferta.py       # Classe Abstrata/Base
    │   └── turma.py
    │
    ├── usuarios/
    │   ├── aluno.py
    │   └── pessoa.py       # Classe Base
    │
    ├── dados/
    │   └── persistencia.py # Leitura e Escrita de JSON
    │
    ├── gerenciadores/
    │   └── gerenciador_sistema.py # Regras de Negócio e Controle
    │
    └── interface/
        └── cli.py          # Menus e Tratamento de Input (Cores)
```



## 📥 Como Clonar o Repositório

Se você deseja baixar o código fonte completo para sua máquina, siga os passos abaixo:

### Pré-requisitos
* Ter o **Git** instalado em sua máquina.
  * *Para verificar se já possui, digite `git --version` no seu terminal.*

### Passo a Passo

1. **Obtenha o Link do Repositório:**
   * Vá até o topo desta página no GitHub.
   * Clique no botão verde **Code** (ou Código).
   * Copie a URL apresentada (HTTPS).

2. **Clone via Terminal:**
   Abra o seu terminal (CMD, PowerShell ou Bash), navegue até a pasta onde deseja salvar o projeto e digite o comando:
   
   ```bash
   git clone [https://github.com/SEU-USUARIO/NOME-DO-REPOSITORIO.git](https://github.com/SEU-USUARIO/NOME-DO-REPOSITORIO.git)

   ```
## ===== Como Executar =====

### Pré-requisitos
* Ter o **Python 3.8** ou superior instalado em sua máquina.
* O sistema utiliza apenas bibliotecas padrão do Python (`json`, `os`, `sys`, `re`), portanto, **não é necessário instalar dependências externas** para a execução principal.
* 
* Via VS Code (Botão Play):

    1. Abra o arquivo main.py.

    2. Clique no botão de "Play" (Executar) no canto superior direito.

    Importante: Como o seu sistema cria arquivos automaticamente (como o banco_dados.json), certifique-se de que você tem permissão de escrita na pasta onde o         projeto está salvo.

    Se você tentar rodar clicando em outros arquivos (como cli.py ou curso.py), nada vai acontecer ou vai dar erro, pois eles são apenas partes do sistema. O          main.py é quem conecta tudo
