couts = [[5, 3, 4],
         [6, 7, 2]]
offre = [8, 9]
demande = [4, 5, 8]


def cout_total(x):
    total = 0
    for i in range(2):
        for j in range(3):
            total += couts[i][j] * x[i][j]
    return total


def solution_initiale():
    x = [[0, 0, 0], [0, 0, 0]]
    stock = offre[:]
    besoin = demande[:]
    i = 0
    j = 0
    while i < 2 and j < 3:
        q = min(stock[i], besoin[j])
        x[i][j] = q
        stock[i] -= q
        besoin[j] -= q
        if stock[i] == 0:
            i += 1
        else:
            j += 1
    return x


def copier(x):
    return [x[0][:], x[1][:]]


def generer_voisins_transport(x):
    voisins = []
    for j in range(3):
        for k in range(3):
            if j != k and x[0][j] > 0 and x[1][k] > 0:
                voisin = copier(x)
                voisin[0][j] -= 1
                voisin[0][k] += 1
                voisin[1][j] += 1
                voisin[1][k] -= 1
                voisins.append(((j, k), voisin))
    return voisins


def tabou_transport(taille_tabou, max_iter):
    solution = solution_initiale()
    best_solution = copier(solution)
    best_cout = cout_total(solution)
    tabou_list = []
    print("depart :", solution, "cout =", best_cout)

    for it in range(1, max_iter + 1):
        candidats = []
        for mouvement, voisin in generer_voisins_transport(solution):
            if mouvement not in tabou_list or cout_total(voisin) < best_cout:
                candidats.append((mouvement, voisin))
        if not candidats:
            break
        mouvement, solution = min(candidats, key=lambda c: cout_total(c[1]))
        tabou_list.append((mouvement[1], mouvement[0]))
        if len(tabou_list) > taille_tabou:
            tabou_list.pop(0)
        if cout_total(solution) < best_cout:
            best_solution = copier(solution)
            best_cout = cout_total(solution)
        print("it", it, ": M%d -> M%d" % (mouvement[0] + 1, mouvement[1] + 1),
              solution, "cout =", cout_total(solution))
    return best_solution, best_cout


print("Exercice 2")
sol, cout = tabou_transport(taille_tabou=3, max_iter=6)
print("D1 :", sol[0])
print("D2 :", sol[1])
print("cout minimal :", cout)