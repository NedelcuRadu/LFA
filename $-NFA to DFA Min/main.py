def ApplyLambda(A, States):  # States = Set din starile curente
    """

    :param States: set din starile curente
    :return: set format din starile in care se poate ajunge cu o miscare $
    """
    new_states = set()
    for state in States:
        for a in A[state]['$']:
            new_states.add(a)
    if len(new_states) > 0:
        return new_states
    else:
        return States


def LambdaTranzitie(A, stari_initiale):
    """

    :param stari_initiale: set format din stari
    :return: set format din toate starile curente + cele in care se poate ajunge cu lambda
    """
    while (stari_initiale != stari_initiale.union(ApplyLambda(A, stari_initiale))):
        stari_initiale = stari_initiale.union(ApplyLambda(A, stari_initiale))
    return stari_initiale  # Lambda closure


def pasechiv(A, n, alfabet, echivalenta):
    for litera in alfabet:
        for i in range(n):
            for j in range(i):
                if not echivalenta[A[i][litera]][
                    A[j][litera]]:  # Daca starile in care putem ajunge nu sunt echivalente
                    echivalenta[i][j] = False
                    echivalenta[j][i] = False
    return echivalenta


def totalechiv(A, n, alfabet, echivalenta):
    while echivalenta != pasechiv(A, n, alfabet, echivalenta):
        echivalenta = pasechiv(A, n, alfabet, echivalenta)
    return echivalenta


def DFS(A, alfabet, viz,
        noduri):  # Matricea de tranzitii, alfabetul,vectorul de bool si setul cu noduri curente/nodul curent
    if isinstance(noduri, set):  # Daca e set de noduri
        for nod in noduri:  # Facem DFS din fiecare nod din set
            if not viz[nod]:
                viz[nod] = True
                for litera in alfabet:
                    DFS(A, alfabet, viz, A[nod][litera])
    else:  # Daca nu e set atunci e int
        if not viz[noduri]:
            viz[noduri] = True
            for litera in alfabet:
                DFS(A, alfabet, viz, A[noduri][litera])


def search(L, val):  # Dictionar si valoare, returneaza pozitia sau -1
    for i in range(len(L)):
        if L[i] == val:
            return i
    return len(L)


def comparator(x):  # Compara dupa lungimea lui X si apoi dupa cel mai mic element din el
    if isinstance(x, set):
        return len(x), sorted(list(x))[0]  # conversia la liste e mereu sortata? Better be sure
    else:
        return 1, x


def Renotare(C, alfabet):  # Matrice, alfabet
    stari_noi = {0}  # Aflam ce stari au ramas
    for i in range(len(C)):
        for j in alfabet:
            stari_noi.add(C[i][j])
    stari_noi = sorted(list(stari_noi))
    for i in range(len(stari_noi)):  # Renotam starile
        Inlocuire(C, alfabet, stari_noi[i], i)


def elimin_duplicate(B, alfabet):  # Eliminam duplicatele din matricea B, returneaza matrice fara stari duplicate
    C = []
    for i in range(len(B)):  # Eliminam duplicatele
        found = False
        for j in range(len(C)):
            if C[j] == B[i]:
                found = True
                Inlocuire(C, alfabet, i, j)
                Inlocuire(B, alfabet, i, j)
        if not found:
            C.append(B[i])
    return C


def Inlocuire(B, alfabet, i, j):  # In matricea D inlocuim starea i cu starea j
    for iter in range(len(B)):
        for a in alfabet:
            try:
                if i in B[iter][a]:
                    B[iter][a].remove(i)
                    B[iter][a].add(j)
            except TypeError:
                if B[iter][a] == i:
                    B[iter][a] = j


def GenAutomat(A, Q, numefisier):  # Pt NFA-uri
    with open(numefisier, "w") as g:
        nr_tranzitii = 0
        g.write(f"{len(A)}\n")
        g.write(f"{len(A[0]) - 1}\n")
        for key in A[0].keys():
            if key != "final":
                g.write(f"{key} ")
        g.write('\n')
        g.write(f"{Q}\n")
        nr_finale = 0
        for i in range(len(A)):
            if A[i]["final"] == True:
                nr_finale += 1
        g.write(f"{nr_finale}\n")
        for i in range(len(A)):
            if A[i]["final"] == True:
                g.write(f"{i} ")
        g.write('\n')
        for iter in range(len(A)):
            for litera in A[iter].items():
                try:
                    nr_tranzitii += len(litera)
                except TypeError:
                    pass  # Exceptie pt "final" care e int
        g.write(str(nr_tranzitii))
        g.write('\n')
        for iter in range(len(A)):
            for litera in A[iter].items():
                try:
                    for nod in litera[1]:
                        g.write(f"{iter} {litera[0]} {nod}\n")
                except TypeError:
                    pass  # Exceptie pt "final" care e int pt


def GenAutomat2(A, Q, numefisier):  # Pt DFA-uri
    with open(numefisier, "w") as g:
        nr_tranzitii = 0
        g.write(f"{len(A) + 1}\n")  # +1 pt sink state
        g.write(f"{len(A[0]) - 1}\n")
        for key in A[0].keys():
            if key != "final":
                g.write(f"{key} ")
        g.write('\n')
        g.write(f"{Q}\n")
        nr_finale = 0
        for i in range(len(A)):
            if A[i]["final"] == True:
                nr_finale += 1
        g.write(f"{nr_finale}\n")
        for i in range(len(A)):
            if A[i]["final"] == True:
                g.write(f"{i} ")
        g.write('\n')
        for dict in A:
            for i in dict.items():
                if i[0] != "final":
                    nr_tranzitii += 1
        g.write(str(nr_tranzitii))
        g.write('\n')
        for iter in range(len(A)):
            for litera in A[iter].items():
                if litera[0] != "final":
                    g.write(f"{iter} {litera[0]} {litera[1]}\n")
        for litera in A[iter].items():
            if litera[0] != "final":
                g.write(f"{len(A)} {litera[0]} {len(A)}\n")


def GenAutomat3(A, Q, numefisier):  # Pt DFA-uri
    with open(numefisier, "w") as g:
        nr_tranzitii = 0
        g.write(f"{len(A)}\n")
        g.write(f"{len(A[0]) - 1}\n")
        for key in A[0].keys():
            if key != "final":
                g.write(f"{key} ")
        g.write('\n')
        g.write(f"{Q}\n")
        nr_finale = 0
        for i in range(len(A)):
            if A[i]["final"] == True:
                nr_finale += 1
        g.write(f"{nr_finale}\n")
        for i in range(len(A)):
            if A[i]["final"] == True:
                g.write(f"{i} ")
        g.write('\n')
        for dict in A:
            for i in dict.items():
                if i[0] != "final":
                    nr_tranzitii += 1
        g.write(str(nr_tranzitii))
        g.write('\n')
        for iter in range(len(A)):
            for litera in A[iter].items():
                if litera[0] != "final":
                    g.write(f"{iter} {litera[0]} {litera[1]}\n")


def LNFAtoNFA(fisier_in, fisier_out):
    with open(fisier_in) as f:
        # Citim datele si construim un dictionar din liste A[stare][litera] = multimea starilor in care se poate ajunge din stare folosind litera
        A = []
        B = []
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
                temp[i] = set()
            A.append(temp)
        for i in range(n):
            temp_2 = dict()
            for i in alfabet[:-1]:
                temp_2[i] = set()
            temp_2["final"] = 0
            B.append(temp_2)
        for linie in f:
            translatie = [x for x in linie.split()]
            try:
                A[int(translatie[0])][translatie[1]].add(int(translatie[2]))
            except:
                pass
    lambda_closure = []
    for x in range(n):
        lambda_closure.append(
            LambdaTranzitie(A, {x}))  # Initial punem in closure toate starile in care putem ajunge cu lambda
        for stare in lambda_closure[x]:
            for litera in alfabet[:-1]:
                B[x][litera] = B[x][litera].union(A[stare][litera])  # Concatenam litera din alfabet
                B[x][litera] = B[x][litera].union(LambdaTranzitie(A, B[x][litera]))  # Toate starile cu lambda
    # Determinam noile stari finale
    stari_finale = set()
    for stari in lambda_closure:
        for i in final:
            if i in stari:
                stari_finale = stari_finale.union(stari)
    # Le trecem in matrice
    for stare in stari_finale:
        B[stare]["final"] = 1
    # Scapam de duplicate
    C = []
    for i in range(len(B)):
        found = False
        for j in range(len(C)):
            if C[j] == B[i]:  # Daca am gasit deja o stare egala, renotam noile stari (necesar pt egal)
                found = True
                Inlocuire(C, alfabet[:-1], i, j)  # Nu ne mai intrereseaza ce se intampla cu $
                Inlocuire(B, alfabet[:-1], i, j)
        if not found:
            C.append(B[i])
    stari_noi = {0}  # Renotam starile
    # Nu merge folosita functia de renotare pt ca lucram cu union aici
    for i in range(len(C)):
        for j in alfabet[:-1]:
            stari_noi = stari_noi.union(C[i][j])
    stari_noi = sorted(list(stari_noi))
    for i in range(len(stari_noi)):
        Inlocuire(C, alfabet[:-1], stari_noi[i], i)
    print("LNFA->NFA:")
    for x in C:
        print(x)
    GenAutomat(C, Q, fisier_out)


def NFAtoDFA(fisier_in, fisier_out):
    with open(fisier_in) as f:
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
            temp['final'] = False
            for i in alfabet:
                temp[i] = set()
            A.append(temp)
        for linie in f:
            translatie = [x for x in linie.split()]
            try:
                A[int(translatie[0])][translatie[1]].add(int(translatie[2]))
            except:
                pass
    for i in final:
        A[i]['final'] = True
    initial = [{Q}]  # Lista cu nodurile, fiecare set reprezinta un nod
    # Initializam coada cu Q si starile in care putem ajunge din aceasta
    for litera in alfabet:
        if len(A[Q][litera]) > 0:  # Sa putem ajunge cu litera intr-o stare
            initial.append(A[Q][litera])
    for stare_comasata in initial[1:]:
        for stare in stare_comasata:
            for litera in alfabet:
                if len(A[stare][litera]) > 0 and A[stare][litera] not in initial:  # Sa nu fie deja in coada
                    initial.append(A[stare][litera])
    initial.sort(key=comparator)  # Compara dupa lungimea lui X si apoi dupa cel mai mic element din el
    # Facem un dictionar ce sa suporte si starile comasate
    B = dict()
    for i in range(len(initial)):
        temp = dict()
        for j in alfabet:
            temp[j] = set()
        temp['final'] = False
        if len(initial[i]) == 1:
            B[list(initial[i])[0]] = temp
        else:
            B[frozenset(initial[i])] = temp

    for i in range(len(initial)):
        if len(initial[i]) == 1:  # Daca e stare normala
            for litera in alfabet:
                B[list(initial[i])[0]][litera] = B[list(initial[i])[0]][litera].union(
                    A[list(initial[i])[0]][litera])  # Adaugam la tranzitii fiecare stare unde se putea ajunge
        else:  # Daca e stare comasata
            for j in initial[i]:  # Luam fiecare stare componenta
                if A[j]['final']:  # Daca starea componenta e finala -> compusa e finala
                    B[frozenset(initial[i])]['final'] = True
                for litera in alfabet:
                    B[frozenset(initial[i])][litera] = B[frozenset(initial[i])][litera].union(
                        A[j][litera])  # Adaugam fiecare stare tranzitie de la fiecare stare componenta
    C = []
    for i in range(len(B)):
        temp = dict()
        temp['final'] = False
        C.append(temp)
    # Aducem inapoi la forma de lista de dictionare
    for i in range(len(initial)):
        if len(initial[i]) == 1:
            C[i] = B[list(initial[i])[0]]
        else:
            C[i] = B[frozenset(initial[i])]
    # Renotam starile
    for i in range(len(C)):
        for litera in alfabet:
            C[i][litera] = search(initial, C[i][litera])
    print("DFA:")
    print(C)
    GenAutomat2(C, Q, fisier_out)


def DFAmin(fisier_in, fisier_out):
    with open(fisier_in) as f:
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
            temp["final"] = False
            A.append(temp)
        for linie in f:
            translatie = [x for x in linie.split()]
            try:
                A[int(translatie[0])][translatie[1]] = (int(translatie[2]))
            except:
                pass
    for stare in final:
        A[stare]["final"] = True
    # Facem tabelul cu echivalenta
    echivalenta = [[] for x in range(n)]
    for i in range(n):
        for j in range(n):
            echivalenta[i].append(True)  # Setam tot tabelul cu True
    for i in range(n):  # Daca o stare e initiala si cealalta nu e, punem False
        for j in range(n):
            if (i in final and j not in final) or (j in final and i not in final):
                echivalenta[i][j] = False
                echivalenta[j][i] = False

    echivalenta = totalechiv(A, n, alfabet, echivalenta)
    clase_echiv = [set() for iter in range(n)]  # Determinam clasele de echivalenta
    for i in range(n):
        for j in range(n):
            if echivalenta[i][j]:
                clase_echiv[i].add(j)
    clase_echiv_clean = []  # Scapam de duplicate
    for i in range(n):
        if clase_echiv[i] not in clase_echiv_clean:
            clase_echiv_clean.append(clase_echiv[i])
    for i in clase_echiv_clean:
        for j in i:
            if A[j]['final']:
                A[list(i)[0]]['final'] = True  # Daca j e stare finala, starea compusa e tot finala
            if j == Q:
                Q = list(i)[0]
            Inlocuire(A, alfabet, j,
                      list(i)[0])  # Inlocuim starile echivalente cu o singura stare(cea mai mica ca ordin)

    A = elimin_duplicate(A, alfabet)  # Eliminam duplicatele
    Renotare(A, alfabet)  # Renotam starile
    viz = [False for iter in range(n)]
    B = []  # Scapam de starile inaccesibile facand DFS din starea initiala
    DFS(A, alfabet, viz, Q)
    for i in range(n):
        if viz[i]:
            B.append(A[i])
    Renotare(B, alfabet)
    C = elimin_duplicate(B, alfabet)
    Renotare(C, alfabet)
    D = []
    '''Cream automatul "invers": daca 1 a 0 => 0 a 1 in noul automat si pastram la fel starile finale.
    Facem acest lucru pentru a putea face DFS din starile finale si a vedea unde ajungem. Toate starile vizitate vor fi stari dead end.'''
    for i in range(len(C)):
        temp = dict()
        temp["final"] = False
        for litera in alfabet:
            temp[litera] = set()
        D.append(temp)
    for iter in range(len(C)):
        for litera in C[iter].items():
            if litera[0] != "final":
                D[litera[1]][litera[0]].add(iter)
    # Am terminat constructia noului automat
    # Acum facem DFS din fiecare stare finala
    viz = [False for iter in range(len(C))]
    for i in range(len(C)):
        if C[i]['final']:
            DFS(D, alfabet, viz, i)

    B = []  # Pastram starile care au fost vizitate
    for i in range(len(C)):
        if viz[i]:
            B.append(C[i])
    Renotare(B, alfabet)
    for iter in range(len(B)):
        for litera in alfabet:
            if B[iter][litera] >= len(B):  # Daca starea nu mai exista marcam translatia ca -1
                B[iter][litera] = -1
    print("DFA Minimal:")
    print(B)
    GenAutomat3(B, Q, fisier_out)


LNFAtoNFA("Datalambda.in", "GeneratedNFA.in")
NFAtoDFA("GeneratedNFA.in", "GeneratedDFA")
DFAmin("GeneratedDFA", "DFAmin.in")
