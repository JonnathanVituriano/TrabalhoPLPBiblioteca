class Emprestimo:
    def __init__(self, identificador, livro, usuario, data_emprestimo, data_prevista_devolucao, data_devolucao=None):
        self._identificador = identificador
        self._livro = livro
        self._usuario = usuario
        self._data_emprestimo = data_emprestimo
        self._data_prevista_devolucao = data_prevista_devolucao
        self._data_devolucao = data_devolucao

    @property
    def identificador(self):
        return self._identificador

    @property
    def livro(self):
        return self._livro

    @property
    def usuario(self):
        return self._usuario

    @property
    def data_emprestimo(self):
        return self._data_emprestimo

    @property
    def data_prevista_devolucao(self):
        return self._data_prevista_devolucao

    @property
    def data_devolucao(self):
        return self._data_devolucao

    def esta_ativo(self):
        return self._data_devolucao is None

    def esta_atrasado(self, data_referencia):
        if not self.esta_ativo():
            return False
        return data_referencia > self._data_prevista_devolucao

    def dias_de_atraso(self, data_referencia):
        if not self.esta_atrasado(data_referencia):
            return 0
        return (data_referencia - self._data_prevista_devolucao).days

    def registrar_devolucao(self, data_devolucao):
        if not self.esta_ativo():
            raise ValueError("Emprestimo ja devolvido.")
        if data_devolucao < self._data_emprestimo:
            raise ValueError("Data de devolucao anterior a data de emprestimo.")
        self._data_devolucao = data_devolucao

    def __repr__(self):
        return (
            f"Emprestimo(identificador={self._identificador}, livro='{self._livro.titulo}', "
            f"usuario='{self._usuario.nome}', data_prevista={self._data_prevista_devolucao}, "
            f"data_devolucao={self._data_devolucao})"
        )

    def __eq__(self, outro):
        if not isinstance(outro, Emprestimo):
            return False
        return self._identificador == outro.identificador
