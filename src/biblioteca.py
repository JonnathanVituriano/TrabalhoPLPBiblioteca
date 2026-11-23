from src.livro import Livro
from src.usuario import Usuario
from src.emprestimo import Emprestimo
from src.operacoes_funcionais import (
    filtrar_livros_por_categoria,
    gerar_relatorio_multas,
    gerar_estatisticas_completas
)

class Biblioteca:
    def __init__(self):
        self._livros = {}
        self._usuarios = {}
        self._emprestimos = {}
        self._contador_emprestimos = 0

    def cadastrar_livro(self, livro):
        if not isinstance(livro, Livro):
            raise TypeError("Objeto deve ser uma instancia de Livro.")
        if livro.identificador in self._livros:
            raise ValueError(f"Livro com identificador {livro.identificador} ja cadastrado.")
        self._livros[livro.identificador] = livro

    def consultar_livro(self, identificador):
        return self._livros.get(identificador)

    def listar_livros(self):
        return tuple(self._livros.values())

    def cadastrar_usuario(self, usuario):
        if not isinstance(usuario, Usuario):
            raise TypeError("Objeto deve ser uma instancia de Usuario.")
        if usuario.identificador in self._usuarios:
            raise ValueError(f"Usuario com identificador {usuario.identificador} ja cadastrado.")
        self._usuarios[usuario.identificador] = usuario

    def consultar_usuario(self, identificador):
        return self._usuarios.get(identificador)

    def listar_usuarios(self):
        return tuple(self._usuarios.values())

    def livro_esta_emprestado(self, identificador_livro):
        for emp in self._emprestimos.values():
            if emp.livro.identificador == identificador_livro and emp.esta_ativo():
                return True
        return False

    def registrar_emprestimo(self, identificador_livro, identificador_usuario, data_emprestimo, data_prevista_devolucao):
        livro = self.consultar_livro(identificador_livro)
        if livro is None:
            raise ValueError(f"Livro com identificador {identificador_livro} nao encontrado.")

        usuario = self.consultar_usuario(identificador_usuario)
        if usuario is None:
            raise ValueError(f"Usuario com identificador {identificador_usuario} nao encontrado.")

        if self.livro_esta_emprestado(identificador_livro):
            raise ValueError(f"Livro '{livro.titulo}' ja esta emprestado.")

        if data_prevista_devolucao < data_emprestimo:
            raise ValueError("Data prevista de devolucao nao pode ser anterior a data de emprestimo.")

        self._contador_emprestimos += 1
        emprestimo = Emprestimo(
            identificador=self._contador_emprestimos,
            livro=livro,
            usuario=usuario,
            data_emprestimo=data_emprestimo,
            data_prevista_devolucao=data_prevista_devolucao
        )
        self._emprestimos[emprestimo.identificador] = emprestimo
        return emprestimo

    def registrar_devolucao(self, identificador_emprestimo, data_devolucao):
        emprestimo = self.consultar_emprestimo(identificador_emprestimo)
        if emprestimo is None:
            raise ValueError(f"Emprestimo com identificador {identificador_emprestimo} nao encontrado.")

        emprestimo.registrar_devolucao(data_devolucao)
        return emprestimo

    def consultar_emprestimo(self, identificador_emprestimo):
        return self._emprestimos.get(identificador_emprestimo)

    def listar_emprestimos(self):
        return tuple(self._emprestimos.values())

    def listar_emprestimos_ativos(self):
        return tuple(filter(lambda emp: emp.esta_ativo(), self._emprestimos.values()))

    def buscar_livros_por_categoria(self, categoria):
        return filtrar_livros_por_categoria(self.listar_livros(), categoria)

    def gerar_relatorio_multas(self, data_referencia, valor_diaria=2.0):
        return gerar_relatorio_multas(self.listar_emprestimos(), data_referencia, valor_diaria)

    def gerar_estatisticas(self, data_referencia, valor_diaria=2.0):
        return gerar_estatisticas_completas(self.listar_livros(), self.listar_emprestimos(), data_referencia, valor_diaria)
