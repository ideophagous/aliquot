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

def new_sum(lis):
    ss = 0
    for i in range(len(lis)-1):
        ss+=lis[i]
    return ss

def aliquot(n,end,max_value):
    sequence = [n]
    stop     = False
    counter  = 0
    flag     = None
    while not stop:
        m    = new_sum(getDivisors(n))
        if m in sequence:
            stop = True
            flag = 'loop '+str(sequence.index(m))
        elif m == 1:
            sequence.append(1)
            stop = True
            flag = 'end'
        elif counter == end or (max_value is not None and m>max_value):
            stop = True
            flag = 'interrupted'
        else:
            sequence.append(m)
            n    = m
        counter+=1
    return sequence,flag

def mapping(n,end,max_value):
    mapping = []
    for i in range(1,n+1):
        mapping.append(aliquot(i,end,max_value))
    return mapping

def mapping2(n,end):
    mapping = []
    for i in range(1,n+1):
        x = i
        sequence = [x]
        stop     = False
        counter  = 0
        while not stop:
            m     = new_sum(getDivisors(x))
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

def agraph(n,end,max_value):
    aliqs = mapping(n,end,max_value)

    g = Graph(n+1)
    for aliq in aliqs:
        #print('gg: '+str(aliq))
        if len(aliq[0]) == 1:
            if aliq[0][0]+1>g.vcount():
                g.add_vertices(aliq[0][0]+1-g.vcount())
            if not isContained(g,(aliq[0][0],aliq[0][0])):
                g.add_edges([(aliq[0][0],aliq[0][0])])
        else:
            for i in range(len(aliq[0])-1):
                if max(aliq[0][i],aliq[0][i+1])+1>g.vcount():
                    g.add_vertices(max(aliq[0][i],aliq[0][i+1])+1-g.vcount())
                if not isContained(g,(aliq[0][i],aliq[0][i+1])):
                    g.add_edges([(aliq[0][i],aliq[0][i+1])])
            if aliq[0][-1] not in [0,1]:
                #print('aliq[0][-1] '+str(aliq[0][-1]))
                '''if aliq[0][-1]+1>g.vcount():
                    g.add_vertices(aliq[0][-1]+1-g.vcount())'''
                if aliq[1] is not None:
                    flag = aliq[1].split()
                    if flag[0] == 'loop':
                        print(aliq[0][-1])
                        index = int(flag[1])
                        if not isContained(g,(aliq[0][index],aliq[0][-1])):
                            g.add_edges([(aliq[0][index],aliq[0][-1])])
    labels = []
    for i in range(g.vcount()):
        labels.append(i)
    g.vs["label"] = labels

    return g

def getSignificantParts(g):
    comp = g.clusters()
    clusters = []
    for i in range(len(comp)):
        cluster = g.subgraph(comp[i])
        if sum(1 for _ in enumerate(cluster.es))>0:
            clusters.append(cluster)
    return clusters
        

if __name__=='__main__':
    n   = int(input('Enter some number: '))
    end = int(input('Enter max length of Aliquot sequence: '))
    max_value = int(input('Enter max value in sequence: '))
    #print(sum(getDivisors(n)))
    #print(aliquot(n,end))
    '''aliqs = mapping(n,end,max_value)
    for aliq in aliqs:
        print(aliq)'''
    alg = agraph(n,end,max_value)
    #print(alg)
    visual_style = {}
    comp = getSignificantParts(alg)
    #print(type(comp))
    visual_style["bbox"] = (1500, 1500)
    counter = 1
    for clu in comp:
        gr = plot(clu,**visual_style)
        gr.save(str(counter)+'_n='+str(n)+'_max_sequence_size='+str(end)+'_max_value='+str(max_value)+'.png')
        counter+=1
    
