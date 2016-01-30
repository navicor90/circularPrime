#!/usr/bin/python

import threading


def evaluar_primos():
    for i in range(1,2000):
        # mostramos si es circular
        if es_circular(i):
            print "%i Es primo circular!!" %(i)

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
        if not es_primo(int(rotado)):
            return False

        rotado = rotar(rotado)

    return True;




evaluar_primos()
