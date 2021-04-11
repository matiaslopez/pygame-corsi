import numpy as np
import itertools
import trials_raw

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
        print (seq,distanciaEntreEstasDosSecs, trials_raw.intersections(seq[0])[0],trials_raw.intersections(seq[1])[0])
        if distanciaEntreEstasDosSecs > mayorDistancia:
            secsElegidas = seq
            mayorDistancia = distanciaEntreEstasDosSecs

    return secsElegidas

#seq = "CDGAF"
#print (seq, trials_raw.intersections(seq))

#LargoCandidato
#trials = [["CI", "False"],["AF", "False"],["EIG", "False"],["FBC", "False"],["BACD", "False"],["DCGB", "False"],
#["CEAID", "False"],["CHAFE", "False"],["IFGEBA", "False"],["DBEHCA", "False"],["BIHDGEC", "False"],
#["DIGHBAC", "False"],["GADCIFHE", "False"],["GDHAEFIB", "False"]]

#CortoCandidato
#trials = [["IG", "False"],["AI", "False"],["EBA", "False"],["CGA", "False"],["IEFC", "False"],["IHGD", "False"],
#["HDABI", "False"],["AGHEB", "False"],["CEGADB", "False"],["BEDHIG", "False"],["BCDEIFH", "False"],
#["GBIDHFC", "False"],["FEDIGACB", "False"],["GDABIEHC", "False"]]

#for i in range(len(trials)):
#    trials[i][1] = sum(trials_raw.distances(trials[i][0]))

#print (trials)


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

# pc0 = [['BE', 1.1401754250991378], ['DB', 2.2677080940897136], ['FEG', 4.7044847843371347], ['GDA', 2.5541212628271319], ['GHIF', 4.8091201481793124], ['FIEB', 4.4624095160803794], ['AGIEC', 7.4838426220812657], ['ABIHD', 8.5947876646298909], ['ICEDHF', 12.129229376670329], ['AFCIHD', 12.262998406839101], ['CIDGAFH', 17.057692286774742], ['IAHGCBD', 16.588493272376766], ['CADGFBEI', 16.015326017964934], ['CADGFBIE', 17.152210100212937]]
# pc1 = [['EB', 1.1401754250991378], ['EF', 1.4764823060233405], ['CDA', 4.685223602595288], ['CBA', 4.2045907545531707], ['ADBH', 6.4774969735887442], ['AHGB', 8.1880711909347941], ['CFAGD', 9.9498866240376351], ['DHGFC', 9.4792303047741768], ['BFGEIC', 13.908415300192962], ['BGIFCE', 10.550383055181355], ['DEHFBIA', 16.585670499374913], ['EDFABGH', 18.78501555383502], ['EBDCAIGF', 21.601055595118236], ['FDGCIEAB', 19.856968273991061]]
# pc2 = [['AD', 0.98488578017961048], ['EB', 1.1401754250991378], ['FEB', 2.6166577311224781], ['DGH', 3.0114559928331173], ['CBEF', 4.1977965612066681], ['CFHG', 6.0986719140741679], ['DICBG', 10.081104157830831], ['DBCIG', 8.8581353110282226], ['ECDABH', 11.875219412883562], ['EDHCBG', 13.77053210169804], ['GAIHFBD', 15.191169493475972], ['GIFDHBA', 16.641265396845228], ['DHFABCEG', 19.173786523989314], ['BADCHEIF', 17.040471187965657]]
# pc3 = [['IF', 2.00124960961895], ['DA', 0.98488578017961048], ['EBG', 4.5811055319161884], ['ECF', 2.6454812675404034], ['EGHI', 6.0358730168741559], ['ECFI', 4.646730877159353], ['BCEAG', 8.5235734669729091], ['EIGAB', 8.7656537600503732], ['HIADBC', 9.6377689821191197], ['HIADCB', 11.070398710445083], ['AIBFEHG', 13.591977245501766], ['IABEGCD', 18.68447291438271], ['BEDGIFHC', 16.9458304717764], ['EFCGBIHA', 17.723002018229256]]

# secsAevaluar = []

# for i in range(6,7):
#     secsAevaluar = []
#     secsAevaluar.append(pc0[i][0])
#     secsAevaluar.append(pc0[i+1][0])
#     secsAevaluar.append(pc1[i][0])
#     secsAevaluar.append(pc1[i+1][0])
#     secsAevaluar.append(pc2[i][0])
#     secsAevaluar.append(pc2[i+1][0])
#     secsAevaluar.append(pc3[i][0])
#     secsAevaluar.append(pc3[i+1][0])

# print(secsAevaluar)
# dameDosMejoresSecuencias(secsAevaluar)

# ['GHIF', 'FIEB', 'ADBH', 'AHGB', 'CBEF', 'CFHG', 'EGHI', 'ECFI']
# (('ADBH', 'ECFI'), 12.0, 0, 0)--
# (('GHIF', 'ADBH'), 11.0, 0, 0)-
# (('FIEB', 'ADBH'), 11.0, 0, 0)-
# (('FIEB', 'CFHG'), 11.0, 0, 0)--
# (('ADBH', 'CBEF'), 11.0, 0, 0)
# (('ADBH', 'CFHG'), 11.0, 0, 0)
# (('ADBH', 'EGHI'), 11.0, 0, 0)
# (('CBEF', 'EGHI'), 11.0, 0, 0)
# (('GHIF', 'FIEB'), 10.0, 0, 0)
# (('GHIF', 'CBEF'), 10.0, 0, 0)
# (('GHIF', 'ECFI'), 10.0, 0, 0)
# (('FIEB', 'EGHI'), 10.0, 0, 0)
# (('FIEB', 'AHGB'), 10.0, 0, 1)
# (('AHGB', 'CBEF'), 11.0, 1, 0)
# (('AHGB', 'ECFI'), 12.0, 1, 0)
# (('AHGB', 'EGHI'), 10.0, 1, 0)


#secs48PC = ["BFEC","IGFC","ADBE","FCBE"]
#dameDosMejoresSecuencias(secs48PC)
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

#secs812PC = ["HADEIBCF","AGDECFBH","GAHIFEBD","AEICFDGB"]
#dameDosMejoresSecuencias(secs812PC)
# (('HADEIBCF', 'GAHIFEBD'), 16.0)
# (('HADEIBCF', 'AGDECFBH'), 15.0)
# (('HADEIBCF', 'AEICFDGB'), 15.0)
# (('AGDECFBH', 'GAHIFEBD'), 15.0)
# (('AGDECFBH', 'AEICFDGB'), 15.0)
# (('GAHIFEBD', 'AEICFDGB'), 15.0)


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
