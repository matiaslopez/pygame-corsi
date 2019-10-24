

import trials_raw
import itertools
import csv


letters = sorted(trials_raw.box_positions.keys())

source = "".join(letters)

data = []
data.append(["NumberMoves","Leftness","Frontness","Length"])
for i in xrange(1, 9+1):
    c = 0
    for seq in itertools.combinations(letters,i):
        # print "for ", seq
        for trial in itertools.permutations(seq):
            c += 1
            data.append([i,                             # number
                        trials_raw.leftness(trial),     # leftness
                        trials_raw.frontness(trial),    # frontness length
                        sum(trials_raw.distances(trial)),    # length
                    ]) #number, leftness, frontness, length

    print "For ", i, " there are ", c, "different trials"


with open("theroy.csv", 'w') as fp:
    a = csv.writer(fp, delimiter=';')
    a.writerows(data)
