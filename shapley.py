from __future__ import division
import json
import itertools
import math
import matplotlib.pyplot as plt

data = json.load(open('stakeholder-list.json'))

MIN_QUOTA = 11
MAX_QUOTA = 61

N = 10

def isplit(iterable, splitters):
    return [list(g) for k, g in itertools.groupby(iterable, lambda x:x in splitters) if not k]

def voting(s, t, q):
    cumulative = 0
    for index in s:
        cumulative += data[index-1]["weight"]

    for index in t:
        cumulative -= data[index-1]["weight"]

    cumulative += data[7]["weight"]
    cumulative -= data[8]["weight"]

    if (cumulative < q):
        return -1
    return 1

def plot(phi_plus, phi_minus):
    plt.figure(1)
    for i in range(1, N-2):
        # print "phi_plus[", i, "] = ", phi_plus[i-1]
        plt_label = "i = " + str(i)
        plt.plot(range(MIN_QUOTA, MAX_QUOTA+1, 5), phi_plus[i-1], label=plt_label, marker='o')
    plt.xlabel('QUOTA')
    plt.ylabel('phi +')
    plt.legend()

    plt.figure(2)
    for i in range(1, N-2):
        # print "phi_minus[", i, "] = ", phi_minus[i-1]
        plt_label = "i = " + str(i)
        plt.plot(range(MIN_QUOTA, MAX_QUOTA+1, 5), phi_minus[i-1], label=plt_label, marker='o')
    plt.xlabel('QUOTA')
    plt.ylabel('phi -')
    plt.legend()

    plt.show()

def main():
    phi = range(1, N)
    all_perm = list(itertools.permutations(range(1, N-2)))
    phi_plus = range(1, N-2)
    phi_minus = range(1, N-2)
    for i in range(1, N-2):
        phi_plus[i-1] = []
        phi_minus[i-1] = []
        for q in range(MIN_QUOTA, MAX_QUOTA+1, 5):
            QUOTA = q * (100 - data[9]["weight"]) / 100.0
            delta_plus = 0
            delta_minus = 0
            for perm in all_perm:
                sets = [1, 2]
                if (perm[0] == i):
                    sets[0] = []
                    sets[1] = isplit(perm, [i])[0]
                elif (perm[N-4] == i):
                    sets[0] = isplit(perm, [i])[0]
                    sets[1] = []
                else:
                    sets = isplit(perm, [i])

                s1 = len(sets[0])
                s2 = len(sets[1])
                delta_plus += (voting(sets[0] + [i], sets[1], QUOTA) - voting(sets[0], sets[1], QUOTA))*math.factorial(s1)*math.factorial(N - s1 - 1)
                delta_minus += (voting(sets[1], sets[0], QUOTA) - voting(sets[1], sets[0] + [i], QUOTA))*math.factorial(s2)*math.factorial(N - s2 - 1)
            print "(", i, ") quota : ", QUOTA, ", delta_plus : ", delta_plus, ", delta_minus : ", delta_minus
            phi_plus[i-1].append(delta_plus/math.factorial(N))
            phi_minus[i-1].append(delta_minus/math.factorial(N))
    plot(phi_plus, phi_minus)

if __name__== "__main__":
    main()
