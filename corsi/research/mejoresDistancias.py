import numpy as np
import itertools

def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in xrange(size_x):
        matrix [x, 0] = x
    for y in xrange(size_y):
        matrix [0, y] = y

    for x in xrange(1, size_x):
        for y in xrange(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )
    #print (matrix)
    return (matrix[size_x - 1, size_y - 1])

#Le asigna un punto a cada letra solo la primera vez que aparece
def cantLetras(seq1,seq2):
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    cantLetras = 0
    for letter in letters:
        apariciones = (str(seq1+seq2)).count(letter)
        #Si la letra aparece alguna vez, incremento
        if apariciones > 0:
            cantLetras+=1

    return cantLetras

#Ejemplos
#print(levenshtein("ABC", "ACB"), cantLetras("ABC", "ACB"))
#print(levenshtein("ABC", "ADB"), cantLetras("ABC", "ADB"))
#print(levenshtein("ABC", "ABD"), cantLetras("ABC", "ABD"))
#print(levenshtein("ABC", "GHI"), cantLetras("ABC", "GHI"))

#Genero una funcion que para un conjunto de secuencias me devuelva las dos que tienen mayor distancia
def dameDosMejoresSecuencias(secs):
    mayorDistancia = 0
    secsElegidas = []
    for seq in itertools.combinations(secs,2):
        distanciaEntreEstasDosSecs = levenshtein(seq[0],seq[1]) + cantLetras(seq[0],seq[1])
        print (seq,distanciaEntreEstasDosSecs)
        if distanciaEntreEstasDosSecs > mayorDistancia:
            secsElegidas = seq
            mayorDistancia = distanciaEntreEstasDosSecs

    print secsElegidas

#secs26PC = ["AD","AD","FC","AD"]
#dameDosMejoresSecuencias(secs26PC)
#(('AD', 'FC'), 6.0)

#secs37PC = ["DHE","ABI","CBA","IEC"]
#dameDosMejoresSecuencias(secs37PC)
#(('DHE', 'ABI'), 9.0)
#(('DHE', 'CBA'), 9.0)
#(('DHE', 'IEC'), 8.0)
#(('ABI', 'IEC'), 8.0)
#(('CBA', 'IEC'), 8.0)

# secs48PC = ["BFEC","IGFC","ADBE","FCBE"]
# dameDosMejoresSecuencias(secs48PC)
# (('IGFC', 'ADBE'), 12.0)
# (('BFEC', 'ADBE'), 10.0)
# (('IGFC', 'FCBE'), 10.0)
# (('BFEC', 'IGFC'), 9.0)

# secs59PC = ["EFCID","GHIEB","BFIEC","GHIFC"]
# dameDosMejoresSecuencias(secs59PC)
# (('EFCID', 'GHIEB'), 13.0)
# (('EFCID', 'GHIFC'), 12.0)
# (('EFCID', 'BFIEC'), 10.0)
# (('GHIEB', 'BFIEC'), 10.0)
# (('BFIEC', 'GHIFC'), 10.0)

# secs610PC = ["DGHCEB","HEFIBC","ECFIDG","DHIBCE"]
# dameDosMejoresSecuencias(secs610PC)
# (('DGHCEB', 'HEFIBC'), 14.0)
# (('DGHCEB', 'ECFIDG'), 14.0)
# (('ECFIDG', 'DHIBCE'), 14.0)
# (('HEFIBC', 'ECFIDG'), 12.0)

# secs711PC = ["BDAHGIC","CBDAIHG","CEABDHI","DGABCEF"]
# dameDosMejoresSecuencias(secs711PC)
# (('CBDAIHG', 'DGABCEF'), 16.0)
# (('BDAHGIC', 'DGABCEF'), 15.0)
# (('BDAHGIC', 'CEABDHI'), 14.0)
# (('CEABDHI', 'DGABCEF'), 14.0)

secs812PC = ["HADEIBCF","AGDECFBH","GAHIFEBD","AEICFDGB"]
dameDosMejoresSecuencias(secs812PC)



#secs26PL = ["AF","DF","CG","GF"]
#dameDosMejoresSecuencias(secs26PL)
#(('AF', 'CG'), 6.0)
#(('DF', 'CG'), 6.0)

#secs37PL = ["FDH","FGB","HFA","EGF"]
#dameDosMejoresSecuencias(secs37PL)
#(('FDH', 'EGF'), 8.0)
#(('FGB', 'HFA'), 8.0)
#(('HFA', 'EGF'), 8.0)

#secs48PL = ["HBDE","BGAC","DFGC","ICAF"]
#dameDosMejoresSecuencias(secs48PL)
#(('HBDE', 'ICAF'), 12.0)
#(('HBDE', 'BGAC'), 11.0)
#(('HBDE', 'DFGC'), 11.0)

#secs59PL = ["FHAGB","HEGFB","BDGCA","HFDCG"]
#dameDosMejoresSecuencias(secs59PL)
#(('FHAGB', 'BDGCA'), 12.0)
#(('HEGFB', 'BDGCA'), 12.0)
#(('FHAGB', 'HFDCG'), 11.0)
#(('HEGFB', 'HFDCG'), 11.0)
#(('BDGCA', 'HFDCG'), 11.0)


#secs610PL = ["BACGDF","GCAEHD","HBACDI","IDFABH"]
#dameDosMejoresSecuencias(secs610PL)
#(('BACGDF', 'IDFABH'), 14.0)
#(('GCAEHD', 'IDFABH'), 14.0)
#(('BACGDF', 'GCAEHD'), 13.0)
#(('GCAEHD', 'HBACDI'), 13.0)
#(('HBACDI', 'IDFABH'), 13.0)

#secs711PL = ["GCHDIAE","EDCFAHB","AGFDCHB","GACDFHE"]
#dameDosMejoresSecuencias(secs711PL)
#(('GCHDIAE', 'EDCFAHB'), 16.0)
#(('GCHDIAE', 'AGFDCHB'), 15.0)
#(('EDCFAHB', 'AGFDCHB'), 13.0)
#(('EDCFAHB', 'GACDFHE'), 13.0)
#(('AGFDCHB', 'GACDFHE'), 13.0)

#secs812PL = ["EDCIGFAH","AFIBHCGD","GIBHEFDC","IACDHBFG"]
#dameDosMejoresSecuencias(secs812PL)
#(('EDCIGFAH', 'AFIBHCGD'), 17.0)
#(('EDCIGFAH', 'GIBHEFDC'), 16.0)
#(('EDCIGFAH', 'IACDHBFG'), 16.0)
#(('GIBHEFDC', 'IACDHBFG'), 16.0)
