#!/usr/bin/python
# -*- coding: utf-8 -*-

from threading import Thread
import time
import sys
from math import sqrt

class PrimosCirculares(object):
    __circulares = []

    @classmethod
    def rotar(self, cadena):
        """ Rota una cadena ingresada , desplazando los elementos del arreglo hacia
        la izquierda y colocando el primero al final. Devuelve la cadena rotada"""
        cadena_rotada = ''
        for i in range(0,len(cadena)):
            cadena_rotada += cadena[(i+1) % len(cadena)]
        return cadena_rotada

    @classmethod
    def esCircular(self, i):
        """ Evalua si es primo circular """
        # Si uno de los caracteres que componen el numero es diferente de 1,3,7,9
        # entonces ya no es circular
        if i > 10:
            for j in str(i):
                if int(j) not in [1,3,7,9]:
                    return False

        # Si alguna de las rotaciones esta en la lista de circulares, es porque ya
        # se evaluo esa combinacion
        rotado = i
        for j in range(0, len(str(i))):
            # Si alguna rotacion no es prima , no es circular
            if not Primos.esPrimo(rotado):
                return False
            rotado = int(self.rotar( str(rotado) ))

        return True;

    def __obtenerCirculares(self,base=1 ,top=10):
        """ Función privada que permite evaluar los numeros circulares en un 
        intervalo dado, utilizado para multihilamiento"""
        # Estos valores se añaden explicitamente para poder iterar con paso 2
        # cuando estemos buscando los circulares y así hacerlo con mayor
        # eficiencia
        if base <= 0 or top <= 1:
            raise Exception('Parametros erroneos, debe ser base > 0 y tope > 1')

        if base < 3:
            self.__circulares.append(2)
            base = 3

        if base % 2 == 0:
            base += 1

        # Le sumamos 1 a top, para evaluar también el numero ingresado por parametros
        for i in range(base, top+1, 2):
            # Si no tenemos suficientes primos para factorizar un numero, se pone a
            # dormir el hilo
            while((Primos.getPrimosCalculados()[len(Primos.getPrimosCalculados())-1] < sqrt(i))):
                time.sleep(2)

            if self.esCircular(i):
                self.__circulares.append(i)

    def buscar(self, top):
        """ Busca todos los numeros primos circulares mayores a 0 y menores que el
        parametro "top" """

        self.__circulares = []
        threads = []
        # Validamos que el valor ingresado, sea entero y positivo
        if int(top) > 0:
            p = Primos(top)

            top1 = int(0.6*top)
            # Creamos hilo para calcular los circulares
            thread1 = Thread(target=self.__obtenerCirculares, args=(1,top1,))
            thread1.start()
            threads.append(thread1)

            # Creamos hilo para calcular los circulares
            thread2 = Thread(target=self.__obtenerCirculares, args=(top1,top,))
            thread2.start()
            threads.append(thread2)

            for t in threads:
                t.join()

            pass

        return self.__circulares
    
class Primos(object):
    PRIMOS = [2,3]
    instancia = None
    calculador = Thread()

    def __init__ (self, top=2):
        self.top = top
        self.calculador = Thread(target=self.preCalcular, args=(self.top,))
        self.calculador.start()

    @classmethod
    def esPrimo(self,n):
        """ Utilizando la lista "primos" evalua si un numero dado "i" es primo """
        if(self.PRIMOS[len(self.PRIMOS) -1] < sqrt(n)):
            if self.calculador.is_alive():
                self.calculador.join()
            else:
                self.calculador = Thread(target=self.preCalcular, args=(n,))
                self.calculador.start()
                self.calculador.join()
                return self.esPrimo(n)
                #wakeup

        for divisor in self.PRIMOS:
            # Si hay un modulo 0 quiere decir que es compuesto porque es divisible
            # por ese divisor
            if( n % divisor == 0):
                return False;
            # Los multiplos de un numero compuesto deben ser menor a la raiz
            # cuadrada del numero a evaluar( No hay casos donde sean mayor)
            if(divisor >= sqrt(n)):
                return True

        raise Exception()


    @classmethod
    def preCalcular(self, top):
        """ Recorre en paso 2 (para evaluar numeros impares) desde el ultimo primo 
        calculado hasta el valor de "top" calculando primos y guardandolos"""
        for i in range(self.PRIMOS[len(self.PRIMOS)-1], int(top), 2):
            if self.esPrimo(i):
                self.PRIMOS.append(i)

    @classmethod
    def getPrimosCalculados(self):
        """ Devuelve la lista de los primos calculada hasta el momento """
        return self.PRIMOS


# Acceso por linea de comandos
if __name__ == '__main__':

    # Si hay mas de 1 parametros, salimos
    if len(sys.argv) > 2:
        print "Error: Se debe pasar un solo parametro. Ej: primos_circulares.py 100"
        exit()

    # Comprobamos si el valor ingresado es correcto
    try:
        numero_max = int(sys.argv[1])
        if numero_max < 0 :
            raise Exception()
    except:
        print "Error: Se debe ingresar un entero positivo. Ej: primos_circulares.py 100"
        exit()

    # Buscamos los primos circulares y calculamos el tiempo
    print 'Calculando... \n'
    startTime = time.time()
    pc = PrimosCirculares()
    pcList = pc.buscar(numero_max)
    endTime = time.time()
    print pcList
    print ('\n Se encontraron %s primos circulares en %s segundos.' % (len(pcList),str(endTime-startTime)))
