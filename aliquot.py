from math import sqrt
from igraph import *

def getDivisors(n):
    divisors = []
    for i in range(1,int(sqrt(n))+1):
        if n%i == 0:
            divisors.append(i)
            divisors.append(n//i)
    divisors = sorted(list(set(divisors)))
    return divisors

def sum(lis):
    ss = 0
    for i in range(len(lis)-1):
        ss+=lis[i]
    return ss

def aliquot(n,end):
    sequence = [n]
    stop     = False
    counter  = 0
    while not stop:
        m     = sum(getDivisors(n))
        if m in sequence:
            stop = True
        elif m == 1:
            sequence.append(1)
            stop = True
        elif counter == end:
            stop = True
        else:
            sequence.append(m)
            n    = m
        counter+=1
    return sequence

def mapping(n,end):
    mapping = []
    for i in range(1,n+1):
        mapping.append(aliquot(i,end))
    return mapping

def agraph(n,end):
    aliq = mapping(n,end)

    g = Graph()

    return g
        

if __name__=='__main__':
    n   = int(input('Enter some number: '))
    end = int(input('Enter max length of Aliquot sequence: '))
    #print(sum(getDivisors(n)))
    #print(aliquot(n,end))
    mapping = mapping(n,end)
    for aliq in mapping:
        print(aliq)
    print(agraph(n,end))
    
