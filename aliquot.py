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

def mapping2(n,end):
    mapping = []
    for i in range(1,n+1):
        x = i
        sequence = [x]
        stop     = False
        counter  = 0
        while not stop:
            m     = sum(getDivisors(x))
            if m in sequence:
                stop = True
            elif m<x:
                sequence.append(m)
                stop = True
            elif m == 1:
                sequence.append(1)
                stop = True
            elif counter == end:
                stop = True
            else:
                sequence.append(m)
                x    = m
            counter+=1
        mapping.append(sequence)
    return mapping

def reverse(t):
    return (t[1],t[0])

def isContained(g,edge):
    for e in g.es:
        if e.tuple == edge or reverse(e.tuple) == edge:
            return True
    return False

def agraph(n,end):
    aliqs = mapping(n,end)

    g = Graph(n+1)
    for aliq in aliqs:
        print('gg: '+str(aliq))
        if len(aliq) == 1:
            if aliq[0]+1>g.vcount():
                g.add_vertices(aliq[0]+1-g.vcount())
            if not isContained(g,(aliq[0],aliq[0])):
                g.add_edges([(aliq[0],aliq[0])])
        else:
            for i in range(len(aliq)-1):
                if max(aliq[i],aliq[i+1])+1>g.vcount():
                    g.add_vertices(max(aliq[i],aliq[i+1])+1-g.vcount())
                if not isContained(g,(aliq[i],aliq[i+1])):
                    g.add_edges([(aliq[i],aliq[i+1])])
            '''if aliq[-1] not in [0,1]:
                if aliq[-1]+1>g.vcount():
                    g.add_vertices(aliq[-1]+1-g.vcount())
                if not isContained(g,(aliq[-1],aliq[-1])):
                    g.add_edges([(aliq[-1],aliq[-1])])'''
    labels = []
    for i in range(g.vcount()):
        labels.append(i)
    g.vs["label"] = labels

    return g

def getSignificantParts(g):
    comp = g.clusters()
    clusters = []
    for i in range(len(comp)):
        if len(comp[i])>1:
            clusters.append(g.subgraph(comp[i]))
    return clusters
        

if __name__=='__main__':
    n   = int(input('Enter some number: '))
    end = int(input('Enter max length of Aliquot sequence: '))
    #print(sum(getDivisors(n)))
    #print(aliquot(n,end))
    aliqs = mapping(n,end)
    for aliq in aliqs:
        print(aliq)
    alg = agraph(n,end)
    print(alg)
    visual_style = {}
    comp = getSignificantParts(alg)
    print(type(comp))
    visual_style["bbox"] = (1500, 1500)
    counter = 1
    for clu in comp:
        gr = plot(clu,**visual_style)
        gr.save(str(counter)+'.png')
        counter+=1
