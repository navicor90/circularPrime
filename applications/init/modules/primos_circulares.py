#!/usr/bin/python
# -*- coding: utf-8 -*-

from threading import Thread
import time
import sys
from math import sqrt

class PrimosCirculares(object):

    class EvaluarCirculares(Thread):
        def __init__ (self,outer, circulares , top):
            threading.Thread.__init__(self)
            self.outer = outer
            self.base = 3
            self.top = top
            self.circulares = circulares

        def __rotar(self, cadena):
            """ Rota una cadena ingresada , desplazando los elementos del arreglo hacia
            la izquierda y colocando el primero al final. Devuelve la cadena rotada"""
            cadena_rotada = ''
            for i in range(0,len(cadena)):
                cadena_rotada += cadena[(i+1) % len(cadena)]
            return cadena_rotada

        def __esCircular(self, i):
            """ Evalua si es primo circular """
            # Si uno de los caracteres que componen el numero es diferente de 1,3,7,9
            # entonces ya no es circular
            for j in str(i):
                if int(j) not in [1,3,7,9]:
                    return False

            # Si alguna de las rotaciones esta en la lista de circulares, es porque ya
            # se evaluo esa combinacion
            rotado = i
            for j in range(0, len(str(i))):
                # Si alguna rotacion no es prima , no es circular
                if not self.outer.esPrimo(rotado):
                    return False
                rotado = int(self.__rotar( str(rotado) ))

            return True;

        def run(self):
            # Estos valores se añaden explicitamente para poder iterar con paso 2
            # cuando estemos buscando los circulares y así hacerlo con mayor
            # eficiencia
            if self.top >= 2:
                self.circulares.append(2)
            else:
                return

            for i in range(self.base, self.top+1, 2):
                # Si no tenemos suficientes primos para factorizar un numero, se pone a
                # dormir el hilo
                while((self.outer.PRIMOS[len(self.outer.PRIMOS)-1] < sqrt(i))):
                    time.sleep(2)

                if self.__esCircular(i):
                    self.circulares.append(i)

    def buscar(self, top):
        """ Busca todos los numeros primos circulares mayores a 0 y menores que el
        parametro "top" """
        circulares = []

        p = Primos(1000)
        print p.esPrimo(top)

        # Validamos que el valor ingresado, sea entero y positivo
        if int(top) > 0:

            """
            threads = []

            # Creamos hilo para calcular todos los numeros primos a utilizar para
            # descomponer otros numeros a evaluar
            thread1 = self.CalcularPrimos(self, top)
            thread1.start()
            threads.append(thread1)

            # Creamos hilo para calcular los circulares
            thread2 = self.EvaluarCirculares(self, circulares, top)
            thread2.start()
            threads.append(thread2)

            for thread in threads:
                thread.join()
            """
            pass

        return circulares
    
class Primos(object):
    def __init__ (self, top=2, primos=[2]):
        self.top = top
        self.primos = primos
        self.calculador = Thread(target=self.preCalcular, args=(self.top,))
        self.calculador.start()

    def esPrimo(self,n):
        """ Utilizando la lista "primos" evalua si un numero dado "i" es primo """
        if(self.primos[len(self.primos) -1] < sqrt(n)):
            if self.calculador.is_alive():
                print 'Esperar a que termine'
                self.calculador.join()
            else:
                print 'Es hora de despertar'
                self.top = n
                self.calculador = Thread(target=self.preCalcular, args=(self.top,))
                self.calculador.start()
                self.calculador.join()
                return self.esPrimo(n)
                #wakeup

        for divisor in self.primos:
            # Si hay un modulo 0 quiere decir que es compuesto porque es divisible
            # por ese divisor
            if( n % divisor == 0):
                return False;
            # Los multiplos de un numero compuesto deben ser menor a la raiz
            # cuadrada del numero a evaluar( No hay casos donde sean mayor)
            if(divisor >= sqrt(n)):
                return True

        raise Exception()


    def preCalcular(self, top):
        for i in range(self.primos[len(self.primos)-1], int(top)):
            if self.esPrimo(i):
                self.primos.append(i)
                # Si se alcnazó la raiz cuadrada del numero maximo a evaluar,
                # no se siguen calculando primos


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
