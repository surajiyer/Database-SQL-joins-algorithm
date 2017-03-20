import random
cpt = []

def sampleIndex(S, I, n):
    for t in S:
        count = lookup(t)

        p = (t, count)
        cpt.append(p)

    intSum = 0
    for p in cpt:
        #print(p[0])
        intSum += p[1]

    #print (intSum)

    Sout = []

    intMin = min(n, intSum)
    print('intMin', intMin, 'intSum' , intSum)
    sid = random.sample(range(intSum), intMin)
    print('sid', sid)
    for id in sid:
        chosen = chosenTupleId(id, n)
        tS = cpt[chosen][0]
        #print('tS', tS)
        offset = id - offsetID(chosen)
        tA = lookupTuple(tS)#[offset]
        tSA = tS+tA
        Sout.append(tSA)
    #print('Sout', Sout)
    return Sout


def chosenTupleId(id, n):
    intSum = 0
    for i in range(0,n):
        intSum += cpt[i][1]
        if intSum > id:
            return i
    print("error in chosenTupleId")
    return -1


def offsetID(chosen):
    intSum = 0
    if chosen == 0:
        return 0
    for i in range(0,chosen):
        intSum += cpt[0][1]
    return intSum


def lookup(tuple):
    return 10


def lookupTuple(tuple):
    return "Z"

Y = ["a", "b", "c", "d"]
x = 4
H = 0
sampleIndex(Y, H, x)