#!/usr/bin/python

import threading
circulares = []
primos = []
class evaluar_circulares(threading.Thread):
    def __init__ (self, base, top):
        threading.Thread.__init__(self)
        self.base = base
        self.top = top

    def run(self):
        print 'inicio circ'
        for i in range(self.base,self.top):
            if es_circular(i):
                circulares.append(i)
                print i

class calcular_primos(threading.Thread):
    def __init__ (self, base, top):
        threading.Thread.__init__(self)
        self.base = base
        self.top = top

    def run(self):
        print 'inicio primos'
        for i in range(self.base,self.top):
            if es_primo(i):
                primos.append(i)


import time
from math import sqrt
def buscar_primos(top):

    startTime = time.time()
    threads = []
    thread1 = calcular_primos(2, top)
    thread1.start()
    threads.append(thread1)

    thread2 = evaluar_circulares(1, top)
    thread2.start()
    threads.append(thread2)

    for thread in threads:
            thread.join()

    endTime = time.time()
    print('el calculo se tardo:'+str(endTime-startTime))
    print('total encontrados:'+ str(len(circulares)))
    
    
def es_primo(i):
    if (len(primos) > 2) and (primos[len(primos)-1] < sqrt(i)):
            time.sleep(1)
            #sleep

    # Si se divide por 2 o un numero menor a si mismo, es primo
    for divisor in primos:
        if( i % divisor == 0):
            return False;
        else:
            if(divisor > sqrt(i)):
                return True
    return True

def rotar(cadena):
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


buscar_primos(1000000)
