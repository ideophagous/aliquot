from math import sqrt
from igraph import *

def getDivisors(n):
    #print('...Getting divisors for '+str(n),end='')
    divisors = []
    for i in range(1,int(sqrt(n))+1):
        if n%i == 0:
            divisors.append(i)
            divisors.append(n//i)
    divisors = sorted(list(set(divisors)))
    #print('....done')
    return divisors

def getPrimeDivisors(n,list_path,prime_chk=False):
    """
    Returns list of prime divisors of a
    number n, with their respective powers

    Input:
    - n: integer whose prime list will be
    computed
    - prime_chk: boolean denoting whether
    
    #6158 - sky
    Output:
    
    """
    prime_divs = []
    if prime_chk:
        if isPrime(n):
            prime_divs.append((n,1))
            return prime_divs
    #m = n//2
    #list_path = build_prime_list(m)  #dangerous for large n

    #list_path = 'Master lists//master_list_11.txt'
    prime_divs = []
    r = n
    with open(list_path,'r') as lp:
        for i,line in enumerate(lp):
            p = int(line.strip())
            if r>=p:
                if r%p==0:
                    prime_divs.append([p,1])
                    r = r//p
                    while r%p==0:
                      prime_divs[-1][1]+=1
                      r = r//p
                      
            else:
                break

    prime_divs.append([r,1])
    return prime_divs
        

def isPrime(n):
    if n==0 or n==1:
        return False
    for i in range(2,int(sqrt(n))+1):
        if n%i == 0:
            return False
    return True

def build_prime_list(n):
    with open('primes_'+str(n)+'.txt','w') as pr:
        for i in range(2,n+1):
            if isPrime(i):
                pr.write(str(i)+'\n')
    return 'primes_'+str(n)+'.txt'

def new_sum(lis):
    ss = 0
    for i in range(len(lis)-1):
        ss+=lis[i]
    return ss

def divisiorSum(prime_divs):
    ss = 0
    for pr_d in prime_divs:
        sub_sum = 0
        

def aliquot(n,end,max_value,no_print=False):
    if not no_print:
        print('...Building Aliquot sequence for '+str(n),end='')
    sequence = [n]
    stop     = False
    counter  = 0
    flag     = None
    while not stop:
        m    = new_sum(getDivisors(n))
        if m in sequence:
            stop = True
            flag = 'loop back to position '+str(sequence.index(m)+1)+' of length '+str(len(sequence)-sequence.index(m))
        elif m == 1:
            sequence.append(1)
            stop = True
            flag = 'end'
        elif counter == end or (max_value is not None and m>max_value) or m<0:
            stop = True
            flag = 'interrupted'
        else:
            sequence.append(m)
            n    = m
        counter+=1
    if not no_print:
        print('.....done, seq='+str(sequence)+', flag='+str(flag))
    return sequence,flag

def get_prev_list(n):
    prev_list = []
    if isPrime(n-1):
        prev_list.append((n-1)**2)
    x = (n-3)**2+1
    for i in range(x):
        if new_sum(getDivisors(i))==n:
            prev_list.append(i)
    return sorted(prev_list)

def isSourceNumber(n):
    """
    Returns a boolean value denoting
    whether a number is a source
    number. A "source number" is an
    integer that has no precedent on
    an Aliquot sequence; in other
    words, no integer, including the
    number itself, has strict divisors
    that add up to it. For example, 2
    and 5 are source numbers, for we
    cannot find an integer x, such as
    s(x) = 2 or s(x) = 5. 15 and 28
    on the other hand are not source
    numbers, because s(16) = 15, and
    s(28) = 28.
    We can demonstrate that for m,n
    integers, such that s(m) = n, m
    has values in [1,(n-3)²]U{(n-1)²}.
    The function therefore will look
    for potential precedents in that
    set, and will return False if any
    one is found, and True if none.

    Input:
    - n: a positive integer

    Output:
    A boolean denoting whether n is a
    source number or not
    """
    if isPrime(n-1):
        return False
    x = (n-3)**2+1
    for i in range(1,x):
        if new_sum(getDivisors(i))==n:
            return False
    return True


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
    print('Building Aliquot map...')
    aliqs = mapping(n,end,max_value)
    print('Aliquot map built.')

    g = Graph(n+1)  # add ,directed=True for a directed graph -- solve issue with subgraphs through
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
    #n   = int(input('Enter some number: '))
    #print(getPrimeDivisors(n,'primes_10000.txt',False))
    #end = int(input('Enter max length of Aliquot sequence: '))
    #max_value = int(input('Enter max value in sequence: '))
    #print(sum(getDivisors(n)))
    #print(aliquot(n,end))
    #print(aliquot(n,end,max_value,no_print=False))
    #print(new_sum(getDivisors(n)))
    #n = 4705499686630466473042812716861336570115880660669072889905496053875945320601882581045264500921665604368264934151667308502968743487543692918887982034128889292133536046049610054928273805151278311296155020067
    n = 7986861071103475746153325993713722181939909575864008193389534105062120286142322991406855519581385426912057012922595899418279984883608337001102840753700533724445688873618121428292285830078301636565283538690642182
    m = 2483660323220411301662800497358268532965109658682700089101155088985854510807969279727822490967549193389806085603996408573665775790428871396394940818505350238794952399068139714943423691925314837177937623488
    for file in os.listdir('Master lists//'):
        print(file)
        print(getPrimeDivisors(m,'Master lists//'+file,False))
    """
    aliqs = mapping(n,end,max_value)
    for aliq in aliqs:
        print(aliq)
    
    print('Starting...')
    alg = agraph(n,end,max_value)
    print('Full graph built.')
    #print(alg)
    print('Building connected components...')
    visual_style = {}
    comp = getSignificantParts(alg)
    print('Connected components built.')
    #print(type(comp))
    print('Plotting...')
    visual_style["bbox"] = (1500, 1500)
    #visual_style["layout"] = g.layout_circle
    counter = 1
    for clu in comp:
        visual_style["layout"] = clu.layout_kamada_kawai()
        print('Plot '+str(counter)+'...')
        gr = plot(clu,**visual_style)
        gr.save(str(counter)+'_n='+str(n)+'_max_sequence_size='+str(end)+'_max_value='+str(max_value)+'.png')
        counter+=1
    print('Task ended.')
    print("Source numbers smaller than "+str(n)+":")
    for m in range(2,n+1):
        #print(str(m)+' -> '+str(get_prev_list(m)))
        if isSourceNumber(m):
            print(m)
    """
