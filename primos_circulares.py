#!/usr/bin/python

import threading

class evaluar_primos(threading.Thread):
    def __init__ (self, base, top):
        threading.Thread.__init__(self)
        self.base = base
        self.top = top

    def run(self):
        for i in range(self.base,self.top):
            if es_circular(i):
                print "%i Es primo circular!!" %(i)

import time
def buscar_primos(top):
    threads = []

    startTime = time.time()
    thread1 = evaluar_primos(1,top/2)
    thread1.start()
    threads.append(thread1)

    thread2 = evaluar_primos(top/2,top*0.75)
    thread2.start()
    threads.append(thread2)

    thread3 = evaluar_primos(top*0.75,top)
    thread3.start()
    threads.append(thread3)

    for thread in threads:
            thread.join()
    endTime = time.time()
    print('el calculo se tardo:'+str(endTime-startTime))
    
    

def es_primo(i):
    # Si se divide por 2 o un numero menor a si mismo, es primo
    for divisor in range(2,i-1):
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


    rotado = str(i)
    for j in range(0, len(str(i))):
        # Si alguna rotacion no es prima , no es circular
        alguno_no_es_primo = False
        if not es_primo(int(rotado)):
            return False

        rotado = rotar(rotado)
        threading.currentThread()

    return True;


buscar_primos(1000000)
