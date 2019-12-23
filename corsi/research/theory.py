

import trials_raw
import itertools
import csv


letters = sorted(trials_raw.box_positions.keys())

source = "".join(letters)

data = []
data.append(["Trial","NumberMoves","Leftness","Frontness","Length"])
for i in range(1, 9+1):
    c = 0
    for seq in itertools.combinations(letters,i):
        # print ("for ", "".join(seq))
        for trial in itertools.permutations(seq):
            c += 1
            data.append(["".join(seq),                  #trial
                        i,                             # number
                        trials_raw.leftness(trial),     # leftness
                        trials_raw.frontness(trial),    # frontness length
                        sum(trials_raw.distances(trial)),    # length
                    ]) #ntrial,  umber, leftness, frontness, length

    print ("For ", i, " there are ", c, "different trials")


with open("theory.csv", 'w') as fp:
    a = csv.writer(fp, delimiter=';')
    a.writerows(data)
