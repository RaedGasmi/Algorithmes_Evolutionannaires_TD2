import random, math, itertools

INF = 10**6
E = {(1,2):14,(1,3):15,(1,8):17,(2,3):13,(2,4):14,(2,5):20,(2,8):21,
     (3,4):11,(3,5):21,(3,6):17,(3,7):9,(3,8):9,(4,5):11,(4,6):10,(4,7):8,(4,8):20,
     (5,6):15,(5,7):18,(6,7):9,(7,8):13}

def d(a, b): return E.get((a,b), E.get((b,a), INF))
def cost(t): return sum(d(t[i], t[(i+1) % len(t)]) for i in range(len(t)))
def fmt(t):  return "-".join(map(str, t + [t[0]]))
def inv(t, i, j): return t[:i] + t[i:j+1][::-1] + t[j+1:]

# ----------recherche tabou----------
def tabou(init, nb_iter=6, taille=3):
    cur = init[:]; best = cur[:]; tabu = []
    print(f"init {fmt(cur)} cout={cost(cur)}")
    for k in range(1, nb_iter+1):
        cand = []
        for i, j in itertools.combinations(range(1, len(cur)), 2):
            if (i, j) == (1, len(cur)-1): continue
            v = inv(cur, i, j); m = (cur[i], cur[j])
            if m in tabu and cost(v) >= cost(best): continue
            cand.append((cost(v), m, v))
        c, m, v = min(cand, key=lambda x: x[0])
        cur = v; tabu.append(m); tabu = tabu[-taille:]
        if c < cost(best): best = cur[:]
        print(f"it{k}: inversion{m} -> {fmt(cur)} cout={c} | tabou={tabu} | best={cost(best)}")
    return best

# ----------recuit simule----------
def recuit(init, T0=20, alpha=0.7, nb_iter=5, seed=31):
    random.seed(seed)
    cur = init[:]; best = cur[:]; T = T0
    print(f"init {fmt(cur)} cout={cost(cur)}, T0={T0}")
    for k in range(1, nb_iter+1):
        i, j = sorted(random.sample(range(1, len(cur)), 2))
        if (i, j) == (1, len(cur)-1): j -= 1
        v = inv(cur, i, j); delta = cost(v) - cost(cur)
        p = 1 if delta <= 0 else math.exp(-delta / T)
        ok = delta <= 0 or random.random() < p
        print(f"it{k}: T={T:.2f} inversion({cur[i]},{cur[j]}) voisin={fmt(v)} "
              f"cout={cost(v)} delta={delta} p={p:.2f} -> {'accepte' if ok else 'rejete'}")
        if ok:
            cur = v
            if cost(cur) < cost(best): best = cur[:]
        T *= alpha
    return best

print("Exercice3")
init = [1, 2, 3, 4, 5, 6, 7, 8]
b = tabou(init);  print("tabou :",  fmt(b), cost(b)); print()
b = recuit(init); print("recuit simule :", fmt(b), cost(b))