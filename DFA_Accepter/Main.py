"""
DFA ACCEPTER - Checkes whether or not a word is processed by a given DFA

Data Format: n - number of states
            m - size of alphabet
            - Line of m alphabet chars -
            Initial state
            k - number of final states
            - Line of k final states -
            l - number of translations
            l lines of x a b ( from state x with translation a you go to state b)

"""

def eval(cuvant):
    global A, final, Q
    stare_curenta = Q
    print(cuvant)
    while (len(cuvant)) > 0:
        stare_curenta = A[stare_curenta][cuvant[0]]
        if stare_curenta == -1:
            return False
        cuvant = cuvant[1:]
    if stare_curenta in final:
        return True
    else:
        return False


with open("data.in") as f:
    A = []
    n = int(f.readline())
    m = int(f.readline())
    alfabet = [x for x in f.readline().split()]
    Q = int(f.readline())
    k = int(f.readline())
    final = [int(x) for x in f.readline().split()]
    i = int(f.readline())
    for i in range(n):
        temp = dict()
        for i in alfabet:
            temp[i] = -1
        A.append(temp)
    for linie in f:
        translatie = [x for x in linie.split()]
        A[int(translatie[0])][translatie[1]] = int(translatie[2])
    print(A)

with open("cuvinte.in") as f:
    for linie in f:
        print(eval(linie.rstrip()))
