from datetime import date
from src.livro import Livro
from src.usuario import Usuario
from src.biblioteca import Biblioteca
from src.comparacao_paradigmas import (
    calcular_total_multas_imperativo,
    calcular_total_multas_funcional
)

def executar_demonstracao():
    biblioteca = Biblioteca()

    livro1 = Livro(1, "Estruturas de Dados e Algoritmos", "Thomas Cormen", "Computacao")
    livro2 = Livro(2, "Engenharia de Software Moderna", "Marco Tulio Valente", "Computacao")
    livro3 = Livro(3, "Calculo Diferencial e Integral", "James Stewart", "Matematica")
    livro4 = Livro(4, "Fisica Universitaria", "Young e Freedman", "Fisica")

    biblioteca.cadastrar_livro(livro1)
    biblioteca.cadastrar_livro(livro2)
    biblioteca.cadastrar_livro(livro3)
    biblioteca.cadastrar_livro(livro4)

    usuario1 = Usuario(1, "Ana Silva", "20240101")
    usuario2 = Usuario(2, "Bruno Souza", "20240102")
    usuario3 = Usuario(3, "Carla Dias", "20240103")

    biblioteca.cadastrar_usuario(usuario1)
    biblioteca.cadastrar_usuario(usuario2)
    biblioteca.cadastrar_usuario(usuario3)

    emp1 = biblioteca.registrar_emprestimo(1, 1, date(2026, 11, 1), date(2026, 11, 10))
    emp2 = biblioteca.registrar_emprestimo(2, 2, date(2026, 11, 5), date(2026, 11, 15))
    emp3 = biblioteca.registrar_emprestimo(3, 1, date(2026, 11, 12), date(2026, 11, 25))
    emp4 = biblioteca.registrar_emprestimo(4, 3, date(2026, 11, 2), date(2026, 11, 8))

    biblioteca.registrar_devolucao(emp4.identificador, date(2026, 11, 7))

    data_referencia = date(2026, 11, 20)

    livros_computacao = biblioteca.buscar_livros_por_categoria("Computacao")
    relatorio_multas = biblioteca.gerar_relatorio_multas(data_referencia)
    estatisticas = biblioteca.gerar_estatisticas(data_referencia)

    total_imperativo = calcular_total_multas_imperativo(biblioteca.listar_emprestimos(), data_referencia)
    total_funcional = calcular_total_multas_funcional(biblioteca.listar_emprestimos(), data_referencia)

    print("=== SISTEMA DE GERENCIAMENTO DE BIBLIOTECA ===")
    print(f"Total de livros cadastrados: {len(biblioteca.listar_livros())}")
    print(f"Total de usuarios cadastrados: {len(biblioteca.listar_usuarios())}")
    print(f"Livros na categoria 'Computacao': {[l.titulo for l in livros_computacao]}")
    print("\n--- Relatorio de Multas (Data de Referencia: 20/11/2026) ---")
    for item in relatorio_multas["itens"]:
        print(f"Emprestimo {item['identificador_emprestimo']} | Livro: {item['titulo_livro']} | Usuario: {item['nome_usuario']} | Dias de Atraso: {item['dias_atraso']} | Multa: R$ {item['valor_multa']:.2f}")
    print(f"Valor Total de Multas (via reduce): R$ {relatorio_multas['total_multas']:.2f}")
    print("\n--- Estatisticas Gerais ---")
    for chave, valor in estatisticas.items():
        print(f"{chave}: {valor}")
    print("\n--- Comparacao entre Paradigmas ---")
    print(f"Total calculado via paradigma imperativo: R$ {total_imperativo:.2f}")
    print(f"Total calculado via paradigma funcional:  R$ {total_funcional:.2f}")
    print(f"Resultados identicos: {total_imperativo == total_funcional}")

if __name__ == "__main__":
    executar_demonstracao()
