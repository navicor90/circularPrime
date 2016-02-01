#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import time
import sys
from math import sqrt

class PrimosCirculares(object):
    PRIMOS =  [2]

    def esPrimo(self, i):
        """ Evalua si es primo a través de un test de primalidad """
        for divisor in self.PRIMOS:
            # Si hay un modulo 0 quiere decir que es compuesto porque es divisible
            # por ese divisor
            if( i % divisor == 0):
                return False;
            else:
                # Los multiplos de un numero compuesto deben ser menor a la raiz
                # cuadrada del numero a evaluar( No hay casos donde sean mayor)
                if(divisor >= sqrt(i)):
                    return True

        self.PRIMOS.append(i)
        return True

    class EvaluarCirculares(threading.Thread):
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


    class CalcularPrimos(threading.Thread):
        def __init__ (self,outer, top):
            threading.Thread.__init__(self)
            self.outer = outer
            self.base = 2
            self.top = top
            self.limite = sqrt(top)

        def run(self):
            for i in range(self.base,self.top):
                if self.outer.esPrimo(i):
                    self.outer.PRIMOS.append(i)
                    # Si se alcnazó la raiz cuadrada del numero maximo a evaluar,
                    # no se siguen calculando primos
                    if i > self.limite:
                        return


    def buscar(self, top):
        """ Busca todos los numeros primos circulares mayores a 0 y menores que el
        parametro "top" """
        circulares = []

        # Validamos que el valor ingresado, sea entero y positivo
        if int(top) > 0:

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

        return circulares
    

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
