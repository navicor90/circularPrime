#!/usr/bin/python

import threading
circulares = []
class evaluar_primos(threading.Thread):
    def __init__ (self, base, top):
        threading.Thread.__init__(self)
        self.base = base
        self.top = top

    def run(self):
        for i in range(self.base,self.top):
            if es_circular(i):
                circulares.append(i)
                print i

import time
BLOCK_SIZE = 100000
def buscar_primos(top):

    startTime = time.time()
    for i in range(1,top/BLOCK_SIZE,2):
        threads = []
        base = (i-1) * BLOCK_SIZE
        top1 = i * (BLOCK_SIZE)
        top2 = (i+1) * BLOCK_SIZE
        print "base: "+ str(base) + " top1:"+ str(top1)
        print "top1: "+ str(top1) + " top2:"+ str(top2)
        thread1 = evaluar_primos(base, top1)
        thread1.start()
        threads.append(thread1)

        thread2 = evaluar_primos(top1, top2)
        thread2.start()
        threads.append(thread2)

        for thread in threads:
                thread.join()

    endTime = time.time()
    print('el calculo se tardo:'+str(endTime-startTime))
    print('total encontrados:'+ str(len(circulares)))
    
    

def es_primo(i):
    # Si se divide por 2 o un numero menor a si mismo, es primo
    for divisor in range(3,i/2):
        if( i % divisor == 0):
            return False;
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
        else:
            if rotado in circulares:
                return True
        rotado = rotar(rotado)

    return True;


buscar_primos(1000000)
