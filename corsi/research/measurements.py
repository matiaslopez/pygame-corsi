import numpy as np
import csv
from shapely.geometry import LineString

# for presentations
protocol = [[1,'G'],
[2,'HG'],
[3,'FG'],
[4,'BGD'],
[5,'CGD'],
[6,'EDFG'],
[7,'AFGH'],
[8,'GEABC'],
[9,'CHBDCE'],
[10,'DAFGHEB']]

box_positions = { # ROW, COLUMN
    "A": (1,1),
    "B": (2,2),
    "C": (4,2),
    "D": (1,3),
    "E": (3,3),
    "F": (2,4),
    "G": (4,4),
    "H": (1,5),
    "I": (3,5),
}

def complete_dict(d, is_column = True):
    for i in range(1,5+1 if is_column else 4+1):
        if i not in d:
            d[i] = 0
    return d


def number_per_column(sequence):
    columns = [ box_positions[b][1] for b in sequence]
    return complete_dict({x:columns.count(x) for x in columns})

def number_per_row(sequence):
    rows = [ box_positions[b][0] for b in sequence]
    return complete_dict({x:rows.count(x) for x in rows}, is_column=False)


def leftness(sequence):
    columns = number_per_column(sequence)

    ret = 0
    multipliers = [ -2, -1, 0, 1, 2]
    for i in range(1,5+1):
        ret += columns[i] * multipliers[i-1]

    return ret

def frontness(sequence):
    rows = number_per_row(sequence)

    ret = 0
    multipliers = [ 2, 1, -1, -2]
    for i in range(1,4+1):
        ret += rows[i] * multipliers[i-1]

    return ret


def distances(sequence):
    d = []
    for i in range(len(sequence)-1):
        a = box_positions[sequence[i]]
        b = box_positions[sequence[i+1]]
        d.append(np.linalg.norm(np.array(a)-np.array(b)))

    return d


def all_distances():
    ret = []
    for i in list(box_positions.keys()):
        for j in list(box_positions.keys()):
            if i<j:
                ret.append([i,j, distances([i,j])[0]])

    return ret

def greedy_long_path():
    connected = []
    dist = all_distances()
    used = []

    i = 0

    heaviest = sorted(dist, key=lambda x: x[2], reverse=True)[0]
    connected.append((heaviest[0], heaviest[1]))


    head = heaviest[0]
    tail = heaviest[1]

    used.append(head)
    used.append(tail)

    print(heaviest, used, head, tail)

    while len(used)<len(list(box_positions.keys())):
        tail_sel = sorted([ x for x in dist if (x[0] == tail and x[1] not in used) or (x[1] == tail and x[0] not in used)]
            , key=lambda x: x[2], reverse=True)[0]

        head_sel = sorted([ x for x in dist if (x[0] == head and x[1] not in used) or (x[1] == head and x[0] not in used)]
            , key=lambda x: x[2], reverse=True)[0]

        if tail_sel[2]>head_sel[2]:
            heaviest = tail_sel
            new_tail = heaviest[0] if heaviest[1]==tail else heaviest[1]
            used.append(new_tail)
            connected.append((tail, new_tail))
            tail = new_tail
        else:
            heaviest = head_sel
            new_head = heaviest[0] if heaviest[1]==head else heaviest[1]
            # used.append(new_head)
            used = [new_head] + used
            connected = [(new_head, head)] + connected
            head = new_head

        print(heaviest, used, head, tail)

        i+=1
        if i >= 30:
            print("bardo")
            break

    print(connected)


def save_protocol_csv(protocol, file_name="test.csv"):
    data = []
    data.append(["Ensayo","Sequencia","leftness","frontness","length","distances", "intersections","overlaps"])
    for [ensayo, sequence] in protocol:
        inter = intersections(sequence)
        data.append([ensayo,
                sequence,
                leftness(sequence),
                frontness(sequence),
                "%.2f"%sum(distances(sequence)),
                # ["%.2f" %x for x in distances(sequence)],
                inter[0],
                inter[1]])

    with open(file_name, 'w') as fp:
        a = csv.writer(fp, delimiter=';')
        a.writerows(data)

def save_csv(file_name="test.csv"):
    data = []
    data.append(["Grupo", "Nivel","Ensayo","Sequencia","number_per_row","number_per_column","leftness","frontness","length","distances", "intersections","overlaps"])
    for (g,gr) in enumerate(trials_group):
        for [nivel, ensayo, sequence] in gr:
            inter = intersections(sequence)
            data.append([g+1,nivel, ensayo, " - ".join(sequence), number_per_row(sequence), number_per_column(sequence),
                leftness(sequence), frontness(sequence),
                "%.2f"%sum(distances(sequence)), ["%.2f" %x for x in distances(sequence)],
                inter[0],inter[1]])

    with open(file_name, 'w') as fp:
        a = csv.writer(fp, delimiter=';')
        a.writerows(data)


def make_segments(p):
    ret = []

    for i in range(0, len(p)-1):
        ret.append([box_positions[p[i]], box_positions[p[i+1]]])

    return ret

def intersections(path):

    segments = make_segments(path)
    count_intersection = 0
    count_overlap = 0

    for i in range(0, len(segments)-1):
        for j in range(i + 1, len(segments)):
            l1 = LineString(segments[i])
            l2 = LineString(segments[j])
            if l1.intersects(l2):
                inter = l1.intersection(l2)
                # print inter.length
                if i+1 == j and inter.length:
                    # print i,j, segments[i], segments[j], "consecutive overlap line", inter
                    count_overlap += 1
                elif i+1!=j and inter.length:
                    # print i,j, segments[i], segments[j], "non-consecutive overlap", inter
                    count_overlap += 1
                elif i+1!=j and inter.length == 0.0:
                    # print i,j, segments[i], segments[j], "real intersection", inter
                    count_intersection += 1
            # else:
                # inter = l1.intersection(l2)
                # print i,j, segments[i], segments[j], "no overlap", inter

    return (count_intersection, count_overlap)


trials_raw = [[1,1,'G','I'],
[1,2,'H','B'],
[1,3,'F','A'],
[1,4,'B','G'],
[1,5,'C','H'],
[2,1,'E - D','H -B'],
[2,2,'A - F','F -D'],
[2,3,'G - E','C -A'],
[2,4,'C - H','G -B'],
[2,5,'D - A','C -E'],
[3,1,'A - F - B','D - B - E'],
[3,2,'G - B - E','H - C - F'],
[3,3,'C - D - E','A - F - I'],
[3,4,'D - G - H','B - C - D'],
[3,5,'I - H - A','E - I - H'],
[4,1,'F - B - H - G','A - D - E - B'],
[4,2,'A - B - G - E','D - A - B - G'],
[4,3,'H - C - I - D','F - C - E - G'],
[4,4,'A - H - F - G','I - C - B - E'],
[4,5,'E - H - D - C','F - A - H - B'],
[5,1,'E - I - A - C -B','F - C - G - A - D'],
[5,2,'I - G - E - C- F','B - H - F - C - D'],
[5,3,'B - E - C - D - F','C - E - D - G - A'],
[5,4,'F - C - B - A - G','I - F - H - B - C'],
[5,5,'F - A - C - I - D','C - I - G - B - H'],
[6,1,'H - I - D - B - F - G','E - A - C - B - F - H'],
[6,2,'H - E - I - B - D - C','I - D - E - G - C - A'],
[6,3,'C - E - D - G - B - F','G - E - I - H - B - C'],
[6,4,'A - I - E - D - C - B ','B - F - G - E - I - D'],
[6,5,'I - D - E - A - F - G ','E - C - F - I - B - G'],
[7,1,'G - E - B - H - A - F - D','A - C - E - G - I - B - D'],
[7,2,'F - C - D - B - A - H - E','I - B - F - A - H - D - E'],
[7,3,'G - I - E - F - C - H - A ','B - C - F - I - E - D - H'],
[7,4,'D - I - A - G - F - C - B ','C - E - F - A - I - H - B'],
[7,5,'B - F - E - G - C - A - H','H - A - B - E - G - I - D'],
[8,1,'H - E - I - D - F - C - A - G','E - G - B - A - C - I - F - H'],
[8,2,'F - C - A - B - D - I - G - E','F - E - A - B - G - I - C - D'],
[8,3,'H - G - I - C - B - E - A - F','G - A - F - C - I - H - E - B'],
[8,4,'D - C - I - F - E - G - B - A','D - E - C - H - A - I - F - G'],
[8,5,'B - F - C - D - E - I - H - A','I - G - F - A - D - E - H - C'],
]


trials_group = ([ [x,y,z.replace(" ","").split("-")] for [x,y,z,_] in trials_raw ],
                [ [x,y,z.replace(" ","").split("-")] for [x,y,_,z] in trials_raw ],
                [ [-1,-2, ["A","B","C","D","E","F","G","H","I",]],
                  [-1,-2, ["A","D","H"]],
                  [-1,-2, ["B","F"]],
                  [-1,-2, ["E","I",]],
                  [-1,-2, ["C","G"]],
                  [-1,-2, ["A"]],
                  [-1,-2, ["A","B","C"]],
                  [-1,-2, ["A","B","C","D","E"]],
                  [-1,-2, ["A","B","C","D","E","F","G"]],
                  [-1,-2, ["A","B","C","D","E","F","G","H","I",]],
                  [-1,-2, ['F', 'B', 'H', 'C', 'D', 'G', 'A', 'I', 'E']],
                ]
                )
