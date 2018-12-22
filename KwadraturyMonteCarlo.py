#! /usr/bin/python3.6

#Michał Sobieraj , WMS IV
#Analiza Numeryczna grupa 1/czwartkowa

import math
import numpy as np
from scipy.stats import multivariate_normal

#############################################################################################
## Funkcje jednej zmiennej nieciągłe


def montecarlo1D(delta, funkcja, n):
    """Używamy rozkładu jednostajnego na przedziale (-delta, delta)"""
    suma = 0
    for i in range(1, n+1):
        x = np.random.uniform(-delta, delta)
        suma = suma+funkcja(x)
    return 2*delta*suma/n


def restrict(a, b, f,x):
    """Zwraca wartosc funkcji zawężonej do [a,b], wpp 0"""
    if a <= x <= b:
        return f(x)
    else:
        return 0


N = 100000

# nieciągłe funkcje do całkowania:
a1 = lambda x: np.floor(x)
a2 = lambda x: 2 if x <= 0 else x*x


# Przedział całkowania dla tych funkcji:
a = -1
b = 2

# Dobieramy delte dla rozkładu U(-delta, delta) tak żeby (a,b) zawierał się w (-delta, delta)

delta = 5

f1 = lambda x: restrict(a, b, a1, x)
f2 = lambda x: restrict(a, b, a2, x)


#############################################################################################
## Funkcja wielu zmiennych

def included(przedzial, punkt):
    """Sprawdza czy punkt (tablica 1xn) należy do obszaru (tablica 2xn)"""

    for i in range(len(punkt)):
        if punkt[i] > przedzial[1][i] or punkt[i] < przedzial[0][i]:
            return 0

    return 1


def monteCarlo(przedzial, funkcja, m, n):
    """Używamy wielowymiarowego rozkładu normalnego z parametrami wektor zerowy i macierz jednostkowa
        n-liczba kroków , m- liczba zmiennych"""

    mean = [0 for y in range(m)]
    cov = [[1 if x == y else 0 for x in range(m)] for y in range(m)]

    suma = 0
    for i in range(1, n+1):
        point = np.random.multivariate_normal(mean, cov)
        if included(przedzial, point):
            suma = suma+funkcja(point)/multivariate_normal(mean, cov).pdf(point)

    return suma/n;


N1 = 100000

# całkujemy na kostkach
obszar1 = [[0, 0], [2, 2]]
obszar2 = [[-2 for i in range(4)], [2 for i in range(4)]]
obszar3 = [[0 for i in range(10)], [1 for i in range(10)]]
obszar4 = [[0 for i in range(4)], [1 for i in range(4)]]

# Przykładowe funkcje wielu zmiennych do całkowania


def g1(x):
    return x[0]*x[1]


def g2(x):
    return x[0]+x[1]-x[2]+x[3]


def g3(x):
    return x[1]+x[2]


def g4(x):
    return x[0]+x[1]*x[2]


##PONIŻEJ PRZYKŁADY

#
# ##############################################################
# print("\nPrzykład I (funkcja 1-zmiennej nieciagła) ")
# print("Liczba prób:", N)
#
# print("\nOczekiwany wynik: 0")
# print("Otrzymano: ", montecarlo1D(delta, f1, N))
# print("Oczekiwany wynik: 4+2/3")
# print("Otrzymano:", montecarlo1D(delta, f2, N))
#
# ###############################################################
# print("\n Przykład II (funkcja wielu zmiennych)")
#
# print("Liczba prób:", N1)
# print("\ng1(x,y)=x*y", "\nOczekiwany wynik: 4")
# print("Otrzymano: ", monteCarlo(obszar1, g1, 2, N1))
#
# print("\ng2(x,y,z,w)=x+y-z+w", "\nOczekiwany wynik: 0")
# print("Otrzymano: ", monteCarlo(obszar2, g2, 4, N1))
#
# print("\ng3(x1,...,x10)=x2+x3", "\nOczekiwany wynik: 1")
# print("Otrzymano: ", monteCarlo(obszar3, g3, 10, N1))
#
# print("\ng4(x,y,z)=x+y*z", "\nOczekiwany wynik: 3/4")
# print("Otrzymano: ", monteCarlo(obszar4, g4, 4, N1))
