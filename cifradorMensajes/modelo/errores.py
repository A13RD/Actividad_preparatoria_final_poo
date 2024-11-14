class ErrorContenido(Exception):
    def __init__(self, mensaje: str):
        super().__init__(mensaje)


class ContieneNumero(ErrorContenido):
    def __init__(self, detalles: str = None):
        super().__init__("ContieneNumero")


class ContieneNoAscii(ErrorContenido):
    def __init__(self, detalles: str = None):
        super().__init__("ContieneNoAscii")


class ErrorFormato(Exception):
    def __init__(self, mensaje: str):
        super().__init__(mensaje)


class DobleEspacio(ErrorFormato):
    def __init__(self):
        super().__init__("DobleEspacio")


class SinLetras(ErrorFormato):
    def __init__(self):
        super().__init__("SinLetras")


class NoTrim(ErrorFormato):
    def __init__(self):
        super().__init__("NoTrim")
