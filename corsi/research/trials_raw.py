import numpy as np
import csv
from shapely.geometry import LineString

# for presentations
trials_raw = [[6,1,'H - D - B - C - G - I','A - F - B - G - D - C'],]

box_positions = {
        "A": (1.0,0.85),
        "B": (3.6,1.2),
        "C": (5.1,1.7),
        "D": (1.4,1.75), 
        "E": (3.9,2.3),
        "F": (5.2,3.0),
        "G": (0.8,3.2),
        "H": (2.0,4.0),
        "I": (3.25,3.45)
}

protocolo_1 = [[1, "A"]]

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
    for i in box_positions.keys():
        for j in box_positions.keys():
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

    print (heaviest, used, head, tail)

    while len(used)<len(box_positions.keys()):
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

        print (heaviest, used, head, tail)

        i+=1
        if i >= 30:
            print ("bardo")
            break

    print (connected)

# def save_csv(file_name="test.csv"):
#     data = []
#     data.append(["Grupo", "Nivel","Ensayo","Sequencia","number_per_row","number_per_column","leftness","frontness","length","distances", "intersections","overlaps"])
#     for (g,gr) in enumerate(trials_group):
#         for [nivel, ensayo, sequence] in gr:
#             inter = intersections(sequence)
#             data.append([g+1,nivel, ensayo, " - ".join(sequence), number_per_row(sequence), number_per_column(sequence),
#                 leftness(sequence), frontness(sequence),
#                 "%.2f"%sum(distances(sequence)), ["%.2f" %x for x in distances(sequence)],
#                 inter[0],inter[1]])

#     with open(file_name, 'w') as fp:
#         a = csv.writer(fp, delimiter=';')
#         a.writerows(data)


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
