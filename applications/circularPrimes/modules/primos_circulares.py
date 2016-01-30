#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
circulares = []
primos = []
class evaluar_circulares(threading.Thread):

    def __init__ (self, top):
        threading.Thread.__init__(self)
        self.base = 3
        self.top = top

    def run(self):
        # Estos valores se añaden explicitamente para poder iterar con paso 2
        # cuando estemos buscando los circulares y así hacerlo con mayor
        # eficiencia
        if self.top > 1:
            circulares.append(1)
            circulares.append(2)
        else:
            circulares.append(1)
            return

        for i in range(self.base,self.top,2):
            # Si no tenemos suficientes primos para factorizar un numero, se pone a
            # dormir el hilo
            while( (len(primos) < 2) or (primos[len(primos)-1] < sqrt(i))):
                time.sleep(2)
                #sleep

            if es_circular(i):
                circulares.append(i)

class calcular_primos(threading.Thread):
    def __init__ (self, top):
        threading.Thread.__init__(self)
        self.base = 2
        self.top = top
        self.limite = sqrt(top)

    def run(self):
        for i in range(self.base,self.top):
            if es_primo(i):
                primos.append(i)
                # Si se alcnazó la raiz cuadrada del numero maximo a evaluar,
                # no se siguen calculando primos
                if i > self.limite:
                    return


import time
from math import sqrt
def buscar_primos(top):

    startTime = time.time()
    threads = []

    thread1 = calcular_primos(top)
    thread1.start()
    threads.append(thread1)

    thread2 = evaluar_circulares(top)
    thread2.start()
    threads.append(thread2)

    for thread in threads:
            thread.join()

    endTime = time.time()
    print('el calculo se tardo:'+str(endTime-startTime))
    print('total encontrados:'+ str(len(circulares)))
    print circulares
    
    
def es_primo(i):
    for divisor in primos:
        # Si hay un modulo 0 quiere decir que es compuesto porque es divisible
        # por ese divisor
        if( i % divisor == 0):
            return False;
        else:
            # Los multiplos de un numero compuesto deben ser menor a la raiz
            # cuadrada del numero a evaluar( No hay casos donde sean mayor)
            if(divisor >= sqrt(i)):
                return True
    return True

def rotar(cadena):
    """ Rota una cadena ingresada , desplazando los elementos del arreglo hacia
    la izquierda y colocando el primero al final. Devuelve la cadena rotada"""
    cadena_rotada = ''
    for i in range(0,len(cadena)):
        cadena_rotada += cadena[(i+1) % len(cadena)]
    return cadena_rotada

def es_circular(i):
    """ Evalua si es primo circular """
    # Si uno de los caracteres que componen el numero es diferente de 1,3,7,9
    # entonces ya no es circular
    for j in str(i):
        if int(j) not in [1,3,7,9]:
            return False

    # Si alguna de las rotaciones esta en la lista de circulares, es porque ya
    # se evaluo esa combinacion
    rotado = str(i)
    for j in range(0, len(str(i))):
        # Si alguna rotacion no es prima , no es circular
        if not es_primo(int(rotado)):
            return False
        rotado = rotar(rotado)

    return True;


buscar_primos(100000000)
