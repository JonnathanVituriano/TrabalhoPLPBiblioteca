import unittest
from datetime import date
from src.livro import Livro
from src.usuario import Usuario
from src.emprestimo import Emprestimo
from src.biblioteca import Biblioteca
from src.operacoes_funcionais import (
    filtrar_livros_por_categoria,
    calcular_multa,
    filtrar_emprestimos_atrasados,
    gerar_relatorio_multas,
    contar_livros_por_categoria,
    contar_emprestimos_por_usuario,
    contar_emprestimos_ativos,
    contar_emprestimos_ativos_em_atraso,
    calcular_total_multas,
    gerar_estatisticas_completas
)
from src.comparacao_paradigmas import (
    calcular_total_multas_imperativo,
    calcular_total_multas_funcional
)

class TestSistemaBiblioteca(unittest.TestCase):
    def setUp(self):
        self.livro1 = Livro(1, "Estruturas de Dados", "Cormen", "Computacao")
        self.livro2 = Livro(2, "Engenharia de Software", "Valente", "Computacao")
        self.livro3 = Livro(3, "Calculo 1", "Stewart", "Matematica")
        self.livro4 = Livro(4, "Fisica 1", "Halliday", "Fisica")

        self.usuario1 = Usuario(1, "Alice", "1001")
        self.usuario2 = Usuario(2, "Bob", "1002")
        self.usuario3 = Usuario(3, "Carol", "1003")

        self.biblioteca = Biblioteca()
        self.biblioteca.cadastrar_livro(self.livro1)
        self.biblioteca.cadastrar_livro(self.livro2)
        self.biblioteca.cadastrar_livro(self.livro3)
        self.biblioteca.cadastrar_livro(self.livro4)

        self.biblioteca.cadastrar_usuario(self.usuario1)
        self.biblioteca.cadastrar_usuario(self.usuario2)
        self.biblioteca.cadastrar_usuario(self.usuario3)

    def test_cadastrar_livro_duplicado_lanca_excecao(self):
        with self.assertRaises(ValueError):
            self.biblioteca.cadastrar_livro(Livro(1, "Outro Livro", "Autor", "Categoria"))

    def test_cadastrar_usuario_duplicado_lanca_excecao(self):
        with self.assertRaises(ValueError):
            self.biblioteca.cadastrar_usuario(Usuario(1, "Outro Nome", "9999"))

    def test_emprestimo_livro_ja_emprestado_lanca_excecao(self):
        self.biblioteca.registrar_emprestimo(1, 1, date(2026, 11, 1), date(2026, 11, 10))
        with self.assertRaises(ValueError):
            self.biblioteca.registrar_emprestimo(1, 2, date(2026, 11, 2), date(2026, 11, 12))

    def test_devolucao_libera_livro_para_novo_emprestimo(self):
        emp = self.biblioteca.registrar_emprestimo(1, 1, date(2026, 11, 1), date(2026, 11, 10))
        self.assertTrue(self.biblioteca.livro_esta_emprestado(1))

        self.biblioteca.registrar_devolucao(emp.identificador, date(2026, 11, 5))
        self.assertFalse(self.biblioteca.livro_esta_emprestado(1))

        novo_emp = self.biblioteca.registrar_emprestimo(1, 2, date(2026, 11, 6), date(2026, 11, 15))
        self.assertIsNotNone(novo_emp)
        self.assertTrue(self.biblioteca.livro_esta_emprestado(1))

    def test_funcao_pura_calcular_multa(self):
        self.assertEqual(calcular_multa(0, 2.0), 0.0)
        self.assertEqual(calcular_multa(-5, 2.0), 0.0)
        self.assertEqual(calcular_multa(1, 2.0), 2.0)
        self.assertEqual(calcular_multa(5, 2.0), 10.0)
        self.assertEqual(calcular_multa(10, 2.5), 25.0)

    def test_funcao_pura_filtrar_livros_por_categoria(self):
        livros = (self.livro1, self.livro2, self.livro3, self.livro4)
        resultado = filtrar_livros_por_categoria(livros, "Computacao")
        self.assertEqual(len(resultado), 2)
        self.assertIn(self.livro1, resultado)
        self.assertIn(self.livro2, resultado)
        self.assertEqual(len(livros), 4)

    def test_funcao_pura_filtrar_emprestimos_atrasados(self):
        emp1 = Emprestimo(1, self.livro1, self.usuario1, date(2026, 11, 1), date(2026, 11, 10))
        emp2 = Emprestimo(2, self.livro2, self.usuario2, date(2026, 11, 1), date(2026, 11, 25))
        emp3 = Emprestimo(3, self.livro3, self.usuario3, date(2026, 11, 1), date(2026, 11, 10), date(2026, 11, 9))

        lista = (emp1, emp2, emp3)
        data_ref = date(2026, 11, 20)

        atrasados = filtrar_emprestimos_atrasados(lista, data_ref)
        self.assertEqual(len(atrasados), 1)
        self.assertEqual(atrasados[0].identificador, 1)

    def test_relatorio_multas_com_map_filter_reduce(self):
        emp1 = Emprestimo(1, self.livro1, self.usuario1, date(2026, 11, 1), date(2026, 11, 10))
        emp2 = Emprestimo(2, self.livro2, self.usuario2, date(2026, 11, 5), date(2026, 11, 15))
        emp3 = Emprestimo(3, self.livro3, self.usuario1, date(2026, 11, 10), date(2026, 11, 25))

        data_ref = date(2026, 11, 20)
        relatorio = gerar_relatorio_multas((emp1, emp2, emp3), data_ref, 2.0)

        self.assertEqual(len(relatorio["itens"]), 2)
        self.assertEqual(relatorio["itens"][0]["dias_atraso"], 10)
        self.assertEqual(relatorio["itens"][0]["valor_multa"], 20.0)
        self.assertEqual(relatorio["itens"][1]["dias_atraso"], 5)
        self.assertEqual(relatorio["itens"][1]["valor_multa"], 10.0)
        self.assertEqual(relatorio["total_multas"], 30.0)

    def test_estatisticas_com_reduce(self):
        livros = (self.livro1, self.livro2, self.livro3, self.livro4)
        por_cat = contar_livros_por_categoria(livros)
        self.assertEqual(por_cat["Computacao"], 2)
        self.assertEqual(por_cat["Matematica"], 1)
        self.assertEqual(por_cat["Fisica"], 1)

        emp1 = Emprestimo(1, self.livro1, self.usuario1, date(2026, 11, 1), date(2026, 11, 10))
        emp2 = Emprestimo(2, self.livro2, self.usuario1, date(2026, 11, 2), date(2026, 11, 12))
        emp3 = Emprestimo(3, self.livro3, self.usuario2, date(2026, 11, 3), date(2026, 11, 13))

        por_usr = contar_emprestimos_por_usuario((emp1, emp2, emp3))
        self.assertEqual(por_usr["Alice"], 2)
        self.assertEqual(por_usr["Bob"], 1)

    def test_comparacao_paradigmas_equivalencia(self):
        emp1 = Emprestimo(1, self.livro1, self.usuario1, date(2026, 11, 1), date(2026, 11, 10))
        emp2 = Emprestimo(2, self.livro2, self.usuario2, date(2026, 11, 5), date(2026, 11, 15))
        emp3 = Emprestimo(3, self.livro3, self.usuario3, date(2026, 11, 12), date(2026, 11, 25))
        emp4 = Emprestimo(4, self.livro4, self.usuario1, date(2026, 11, 1), date(2026, 11, 5), date(2026, 11, 4))

        emprestimos = (emp1, emp2, emp3, emp4)
        data_ref = date(2026, 11, 20)

        total_imperativo = calcular_total_multas_imperativo(emprestimos, data_ref, 2.0)
        total_funcional = calcular_total_multas_funcional(emprestimos, data_ref, 2.0)

        self.assertEqual(total_imperativo, 30.0)
        self.assertEqual(total_funcional, 30.0)
        self.assertEqual(total_imperativo, total_funcional)

if __name__ == "__main__":
    unittest.main()
