class Usuario:
    def __init__(self, identificador, nome, matricula):
        self._identificador = identificador
        self._nome = nome
        self._matricula = matricula

    @property
    def identificador(self):
        return self._identificador

    @property
    def nome(self):
        return self._nome

    @property
    def matricula(self):
        return self._matricula

    def __repr__(self):
        return f"Usuario(identificador={self._identificador}, nome='{self._nome}', matricula='{self._matricula}')"

    def __eq__(self, outro):
        if not isinstance(outro, Usuario):
            return False
        return self._identificador == outro.identificador
