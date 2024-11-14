from abc import ABC, abstractmethod
from typing import List, Tuple
from .errores import (
    ContieneNumero, ContieneNoAscii,
    DobleEspacio, SinLetras, NoTrim
)


class ReglaCifrado(ABC):
    def __init__(self, token: int):
        self.token = token

    @abstractmethod
    def encriptar(self, mensaje: str) -> str:
        pass

    @abstractmethod
    def desencriptar(self, mensaje: str) -> str:
        pass

    @abstractmethod
    def mensaje_valido(self, mensaje: str):
        pass

    def encontrar_numeros_mensaje(self, mensaje: str) -> List[Tuple[int, str]]:
        return [(i, char) for i, char in enumerate(mensaje) if char.isdigit()]

    def encontrar_no_ascii_mensaje(self, mensaje: str) -> List[Tuple[int, str]]:
        return [(i, char) for i, char in enumerate(mensaje) if ord(char) > 127]


class ReglaCifradoTraslacion(ReglaCifrado):
    def mensaje_valido(self, mensaje: str):
        errores = []

        # Verificar si hay letras
        if not any(char.isalpha() for char in mensaje):
            errores.append(SinLetras())

        # Verificar números
        if any(char.isdigit() for char in mensaje):
            errores.append(ContieneNumero())

        # Verificar caracteres no ASCII
        if any(ord(char) > 127 for char in mensaje):
            errores.append(ContieneNoAscii())

        if errores:
            if len(errores) == 1:
                raise errores[0]
            else:
                mensaje_error = "; ".join(str(e) for e in errores)
                raise Exception(mensaje_error)

    def encriptar(self, mensaje: str) -> str:
        self.mensaje_valido(mensaje)
        mensaje = mensaje.lower()
        resultado = ""
        for char in mensaje:
            if char.isalpha():
                nuevo_char = chr(((ord(char) - ord('a') + self.token) % 26) + ord('a'))
                resultado += nuevo_char
            else:
                resultado += char
        return resultado

    def desencriptar(self, mensaje: str) -> str:
        self.mensaje_valido(mensaje)
        mensaje = mensaje.lower()
        resultado = ""
        for char in mensaje:
            if char.isalpha():
                nuevo_char = chr(((ord(char) - ord('a') - self.token) % 26) + ord('a'))
                resultado += nuevo_char
            else:
                resultado += char
        return resultado


class ReglaCifradoNumerico(ReglaCifrado):
    def mensaje_valido(self, mensaje: str):
        errores = []

        # Verificar si hay letras
        if not any(char.isalpha() for char in mensaje):
            errores.append(SinLetras())

        # Verificar números
        if any(char.isdigit() for char in mensaje):
            errores.append(ContieneNumero())

        # Verificar caracteres no ASCII
        if any(ord(char) > 127 for char in mensaje):
            errores.append(ContieneNoAscii())

        # Verificar doble espacio
        if "  " in mensaje:
            errores.append(DobleEspacio())

        # Verificar espacios al inicio o final
        if mensaje.strip() != mensaje:
            errores.append(NoTrim())

        if errores:
            if len(errores) == 1:
                raise errores[0]
            else:
                mensaje_error = "; ".join(str(e) for e in errores)
                raise Exception(mensaje_error)

    def encriptar(self, mensaje: str) -> str:
        self.mensaje_valido(mensaje)
        mensaje = mensaje.lower()
        resultado = " ".join(str(ord(char) * self.token) for char in mensaje)
        return resultado

    def desencriptar(self, mensaje: str) -> str:
        numeros = mensaje.split()
        resultado = "".join(chr(int(num) // self.token) for num in numeros)
        return resultado


class Cifrador:
    def __init__(self, agente: ReglaCifrado):
        self.agente = agente

    def encriptar(self, mensaje: str) -> str:
        return self.agente.encriptar(mensaje)

    def desencriptar(self, mensaje: str) -> str:
        return self.agente.desencriptar(mensaje)