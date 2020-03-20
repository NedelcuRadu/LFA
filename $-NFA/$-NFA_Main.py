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
    """
    
    :param States: set din starile curente  
    :return: set format din starile in care se poate ajunge cu o miscare $
    """
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
    """
    
    :param stari_initiale: set format din stari 
    :return: set format din toate starile curente + cele in care se poate ajunge cu lambda
    """
    while (stari_initiale != stari_initiale.union(ApplyLambda(stari_initiale))):
        stari_initiale = stari_initiale.union(ApplyLambda(stari_initiale))
    return stari_initiale


def eval(cuvant):
    global A, final, Q
    s = []
    s.append(Q)
    stari_initiale = LambdaTranzitie(set(s))  # Aflam in ce stari putem ajunge cu $ din starea initiala
    while (len(cuvant)) > 0:  # Procesam cate o litera din cuvant
        stari_noi = set()
        for stare in stari_initiale:  # Pt fiecare stare curenta
            for a in A[stare][cuvant[0]]:  # Pt fiecare stare in care se poate ajunge cu litera curenta
                if a != -1:
                    stari_noi.add(a)  # Adaugam la starile noi
        stari_initiale = LambdaTranzitie(stari_noi)  # Aflam starile in care se poate ajunge cu lambda
        cuvant = cuvant[1:]  # Trecem la urmatoarea litera
    stari_initiale = LambdaTranzitie(stari_initiale)  # Aflam starile in care se poate ajunge cu lambda
    for x in stari_initiale:  # Pt fiecare stare in care am ajuns
        if x in final:  # Daca e stare finala
            return True  # Cuvantul e acceptat
    return False  # Cuvantul nu e acceptat


with open("data.in") as f:
    # Citim datele si construim un dictionar din liste A[stare][litera] = multimea starilor in care se poate ajunge din stare folosind litera
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
        try:
            A[int(translatie[0])][translatie[1]].append(int(translatie[2]))
        except: pass

cuvant = input("Dati cuvantul: ")
try:
    print(eval(cuvant))
except KeyError:
    print("Cuvantul contine litere care nu sunt in alfabet")
