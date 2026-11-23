# Atividade Prática — Sistema de Gerenciamento de Biblioteca

**Disciplina:** Linguagens de Programação  
**Tema:** Integração entre Programação Orientada a Objetos (POO) e Programação Funcional (PF)  
**Linguagem Utilizada:** Python 3 (versão 3.10+)  

---

## 1. Integrantes do Grupo

- **Jonnathan Vituriano** - Matrícula / Função: Desenvolvimento, Modelagem e Testes

---

## 2. Visão Geral do Projeto

O sistema foi desenvolvido para atender às necessidades de uma biblioteca universitária, permitindo o gerenciamento de acervo de livros, cadastro de usuários, controle rigoroso de empréstimos e devoluções, além do cálculo automatizado de multas por atraso e geração de relatórios estatísticos consolidados.

A arquitetura do software adota um modelo híbrido e modular:
1. **Programação Orientada a Objetos (POO):** Modela o domínio do problema, estrutura as entidades (`Livro`, `Usuario`, `Emprestimo`, `Biblioteca`), define o ciclo de vida dos objetos e assegura o encapsulamento do estado interno.
2. **Programação Funcional (PF):** Processa dados, realiza filtragens, transformações matemáticas e agregações analíticas (`map`, `filter`, `reduce`), operando exclusivamente com funções puras e imutabilidade de dados.

Seguindo estritamente o regulamento técnico da disciplina, o código-fonte não possui comentários internos. Toda a documentação técnica, decisões de design e regras de uso estão concentradas neste documento.

---

## 3. Estrutura dos Arquivos

```text
TrabalhoPLPBiblioteca/
├── .gitignore
├── README.md
├── main.py
├── src/
│   ├── __init__.py
│   ├── livro.py
│   ├── usuario.py
│   ├── emprestimo.py
│   ├── biblioteca.py
│   ├── operacoes_funcionais.py
│   └── comparacao_paradigmas.py
└── tests/
    ├── __init__.py
    └── test_biblioteca.py
```

---

## 4. Modelagem Orientada a Objetos (POO)

### 4.1. Classe `Livro` (`src/livro.py`)
Representa um exemplar do acervo da biblioteca.
- **Atributos privados:**
  - `_identificador`: Identificador numérico único do livro.
  - `_titulo`: Título da obra.
  - `_autor`: Nome do autor.
  - `_categoria`: Gênero ou área do conhecimento (ex.: Computacao, Matematica, Fisica).
- **Encapsulamento:** Propriedades de leitura (`@property`) para acesso seguro aos atributos.

### 4.2. Classe `Usuario` (`src/usuario.py`)
Representa uma pessoa vinculada à instituição universitária.
- **Atributos privados:**
  - `_identificador`: Identificador numérico único do usuário.
  - `_nome`: Nome completo do usuário.
  - `_matricula`: Registro acadêmico institucional.
- **Encapsulamento:** Propriedades de leitura (`@property`).

### 4.3. Classe `Emprestimo` (`src/emprestimo.py`)
Representa a transação de cessão temporária de um livro a um usuário.
- **Atributos privados:**
  - `_identificador`: Identificador único do empréstimo.
  - `_livro`: Instância da classe `Livro`.
  - `_usuario`: Instância da classe `Usuario`.
  - `_data_emprestimo`: Objeto `date` contendo a data em que o empréstimo foi efetuado.
  - `_data_prevista_devolucao`: Objeto `date` indicando o prazo limite para devolução.
  - `_data_devolucao`: Objeto `date` com a data real em que o livro foi entregue (ou `None` se o empréstimo estiver ativo).
- **Métodos de Negócio:**
  - `esta_ativo()`: Retorna `True` se `_data_devolucao` for `None`.
  - `esta_atrasado(data_referencia)`: Retorna `True` se o empréstimo estiver ativo e a data de referência for estritamente maior que a data prevista de devolução.
  - `dias_de_atraso(data_referencia)`: Retorna a quantidade inteira de dias decorridos após o prazo previsto (retorna 0 caso não haja atraso ou o empréstimo já tenha sido devolvido).
  - `registrar_devolucao(data_devolucao)`: Valida a data e atualiza o estado de devolução.

### 4.4. Classe `Biblioteca` (`src/biblioteca.py`)
Atua como o agregador central e ponto de orquestração do sistema.
- **Responsabilidades:**
  - Manter o registro em memória de livros, usuários e empréstimos utilizando dicionários indexados por chave identificadora.
  - Assegurar a unicidade de cadastros impedindo identificadores duplicados.
  - Aplicar a regra de exemplar único: não permite novo empréstimo de um livro que já esteja emprestado e ativo.
  - Registrar devoluções, tornando o livro imediatamente disponível para empréstimos subsequentes.
  - Expor consultas retornando estruturas de dados imutáveis (tuplas).
  - Integrar os dados com os processamentos do módulo funcional.

---

## 5. Regras de Negócio Atendidas

1. **Unicidade de Empréstimo:** Um usuário pode realizar vários empréstimos, mas cada empréstimo está vinculado a um único usuário e um único livro.
2. **Exemplar Único:** Cada livro cadastrado é tratado como exemplar único. Um livro não pode estar emprestado para mais de um usuário simultaneamente. Tentativas de novo empréstimo para livros ativos disparam exceção `ValueError`.
3. **Disponibilidade Imediata na Devolução:** A devolução de um empréstimo preenche a data efetiva de devolução, liberando o livro para novas operações.
4. **Critério de Atraso:** Um empréstimo é considerado em atraso se e somente se estiver ativo (não devolvido) e a data de referência informada for posterior à sua data prevista de devolução.
5. **Valor da Multa Diária:** R$ 2,00 por dia de atraso. Empréstimos devolvidos no prazo ou não atrasados possuem multa igual a R$ 0,00.

---

## 6. Programação Funcional (PF)

As operações analíticas e de transformação residem no módulo `src/operacoes_funcionais.py` e seguem os princípios fundamentais do paradigma funcional:

### 6.1. Funções Puras e Transparência Referencial
Uma função é pura quando depende exclusivamente dos seus argumentos de entrada, não produz efeitos colaterais observáveis (não altera variáveis globais, não modifica coleções externas, não faz I/O) e para os mesmos parâmetros sempre produz exatamente o mesmo resultado.
- `calcular_multa(dias_atraso, valor_diaria=2.0)`: Calcula o valor da penalidade financeira de forma determinística e matemática.

### 6.2. Imutabilidade
Nenhuma função do módulo altera o estado das coleções ou objetos recebidos. Quando há necessidade de criar agregações, novas tuplas ou novos dicionários são instanciados (por exemplo, via desempacotamento de dicionários `{**acumulador, ...}`).

### 6.3. Operações Funcionais Obrigatórias

- **Filtragem de Livros (`filtrar_livros_por_categoria`):**  
  Utiliza a função de alta ordem `filter` para extrair da coleção de livros apenas os elementos cuja categoria coincide com a solicitada, retornando uma tupla imutável.
- **Filtragem de Empréstimos Atrasados (`filtrar_emprestimos_atrasados`):**  
  Utiliza `filter` com um predicado baseado na data de referência.
- **Relatório de Multas (`gerar_relatorio_multas`):**  
  Emprega a tríade funcional de alta ordem:
  1. `filter`: Seleciona os empréstimos ativos em atraso.
  2. `map`: Transforma cada empréstimo em atraso em um dicionário contendo resumo do item e a multa individual calculada.
  3. `reduce`: Agrega e soma os valores das multas individuais para produzir o montante consolidado do relatório.
- **Estatísticas com `reduce`:**  
  - `contar_livros_por_categoria`: Utiliza `reduce` para acumular e totalizar os livros por categoria em um novo dicionário.
  - `contar_emprestimos_por_usuario`: Utiliza `reduce` para acumular a contagem de empréstimos atribuídos a cada usuário.

---

## 7. Comparação entre Paradigmas (`src/comparacao_paradigmas.py`)

O sistema implementa o cálculo do somatório de multas sob os dois paradigmas:

### Versão Imperativa:
```python
def calcular_total_multas_imperativo(emprestimos, data_referencia, valor_diaria=2.0):
    total = 0.0
    for emp in emprestimos:
        if emp.esta_atrasado(data_referencia):
            dias = emp.dias_de_atraso(data_referencia)
            total += dias * valor_diaria
    return total
```

### Versão Funcional:
```python
def calcular_total_multas_funcional(emprestimos, data_referencia, valor_diaria=2.0):
    atrasados = filter(lambda emp: emp.esta_atrasado(data_referencia), emprestimos)
    multas = map(lambda emp: calcular_multa(emp.dias_de_atraso(data_referencia), valor_diaria), atrasados)
    return reduce(lambda acumulador, multa: acumulador + multa, multas, 0.0)
```

### Síntese Comparativa:
| Critério | Paradigma Imperativo | Paradigma Funcional |
| :--- | :--- | :--- |
| **Foco** | Como executar o algoritmo passo a passo (fluxo de controle). | O que deve ser transformado (declaração de transformações). |
| **Mutabilidade** | Variável acumuladora mutável (`total = 0.0` com reassociações). | Estruturas imutáveis processadas em pipeline. |
| **Efeitos Colaterais** | Propício a alterações acidentais de estado compartilhado. | Ausência de efeitos colaterais e facilidade de paralelização. |
| **Legibilidade e Testes** | Laços e condicionais misturam lógica de filtro e soma. | Separação nítida de responsabilidades (`filter`, `map`, `reduce`). |

---

## 8. Como Executar o Projeto

### Pré-requisitos:
- Python 3.10 ou superior instalado no sistema operacional.

### 8.1. Execução da Demonstração Completa
Para executar o fluxo completo do sistema, com cadastro de dados de exemplo, simulação de devoluções, exibição de relatórios funcionais e validação de equivalência de paradigmas:

```bash
python main.py
```

### 8.2. Execução da Suíte de Testes Unitários
Para rodar todos os testes automatizados da aplicação:

```bash
python -m unittest discover tests
```

---

## 9. Suíte de Testes

Os testes cobrem:
1. Validação de regras de unicidade de chave primária para livros e usuários.
2. Bloqueio de empréstimo duplo de um mesmo livro (regra de exemplar único).
3. Liberação imediata do livro após registro de devolução.
4. Pureza e precisão do cálculo de multas.
5. Filtragem imutável de livros por categoria e empréstimos atrasados.
6. Pipeline funcional completo de relatório de multas com `filter`, `map` e `reduce`.
7. Agregações estatísticas com `reduce`.
8. Equivalência exata entre as abordagens imperativa e funcional.
