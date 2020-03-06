"""
LAMBDA NFA ACCEPTER - Checkes whether or not a word is processed by a given LAMBDA-NFA (Lamba is symbolised by $)
Data Format: n - number of states
            m - size of alphabet
            - Line of m alphabet chars -
            Initial state
            k - number of final states
            - Line of k final states -
            l - number of translations
            l lines of x a b ( from state x with translation a you go to state b)
"""


def ApplyLambda(States):  # States = Set din starile curente
    global A
    new_states = set()
    for state in States:
        for a in A[state]['$']:
            if a != -1:
                new_states.add(a)
    if len(new_states) > 0:
        return new_states
    else:
        return States


def LambdaTranzitie(stari_initiale):
    while (stari_initiale != stari_initiale.union(ApplyLambda(stari_initiale))):
        stari_initiale = stari_initiale.union(ApplyLambda(stari_initiale))
    return stari_initiale


def eval(cuvant):
    global A, final, Q
    s = []
    s.append(Q)
    stari_initiale = LambdaTranzitie(set(s))
    while (len(cuvant)) > 0:
        stari_noi = set()
        for stare in stari_initiale:
            for a in A[stare][cuvant[0]]:
                if a != -1:
                    stari_noi.add(a)
        stari_initiale = LambdaTranzitie(stari_noi)
        cuvant = cuvant[1:]
    stari_initiale = LambdaTranzitie(stari_initiale)
    print(stari_initiale)
    for x in stari_initiale:
        if x in final:
            return True
    return False


with open("E:\PyCharmProjects\Datalambda.in") as f:
    A = []
    n = int(f.readline())
    m = int(f.readline())
    alfabet = [x for x in f.readline().split()]
    alfabet.append('$')
    Q = int(f.readline())
    k = int(f.readline())
    final = [int(x) for x in f.readline().split()]
    i = int(f.readline())
    for i in range(n):
        temp = dict()
        for i in alfabet:
            temp[i] = [-1]
        A.append(temp)
    for linie in f:
        translatie = [x for x in linie.split()]
        A[int(translatie[0])][translatie[1]].append(int(translatie[2]))
    for x in A:
        print(x)

print(eval('aaaaaa'))
