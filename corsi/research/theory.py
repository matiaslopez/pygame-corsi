import trials_raw
import itertools
import csv
import statistics
import random
from random import shuffle

#Chequea que el trial no sea subsecuencia de los ya cargados
def notIsSubsequence(trial,selected_trials):
	trial = "".join(trial)
	print (selected_trials)	
	#Veo si no hay substrings con los anteriores (los de mayor longitud)
	for i in range(len(trial),len(selected_trials)):
		print ("Chequeo si ",trial," es substring de: ",selected_trials[i][0])
		if trial in str(selected_trials[i][0]):
			print(trial, " is in ",selected_trials[i][0])
			return False
				
	return True

#Chequea que el trial no contenga subsecuencias (tomando de a 2) de los ya cargados
def notHasSubsequence(trial,selected_trials):
	print ("Analizo: "+"".join(trial))
	#Veo si no hay substrings con los anteriores (los de mayor longitud)
	for j in range(len(trial),len(selected_trials)):
		#Si no hay con quien analizar, salto
		if selected_trials[j][0] == 'X':
			return True

		#Tomo el trial de a 2
		for i in range(1,len(trial)):
			deAdos = []
			deAdos.append(trial[i-1])
			deAdos.append(trial[i])
			junto = "".join(deAdos)
			print ("Chequeo si ",junto," es substring de: ",selected_trials[j][0])
			if junto in str(selected_trials[j][0]):
				print(junto, " is in ",selected_trials[j][0])
				return False

	return True

#Chequea si el trial que voy a cargar tiene subsecuencias ya utilizadas
def noHaySubsecuenciasCargadas(trial, selected_trials):
	print ("Analizo: "+"".join(trial))
	#Veo si no hay substrings con los anteriores (los de menor longitud)
	for j in range(1,len(trial)-1):
		#Si no hay con quien analizar, salto
		if selected_trials[j][0] == 'X':
			return True
		#Tomo el trial de a 2
		for i in range(1,len(trial)):
			deAdos = []
			deAdos.append(trial[i-1])
			deAdos.append(trial[i])
			junto = "".join(deAdos)
			print ("Chequeo si ",junto," es substring de: ",selected_trials[j][0])
			if junto in str(selected_trials[j][0]):
				print(junto, " is in ",selected_trials[j][0])
				return False

	return True

#Cuenta la cantidad de apariciones de cada letra en los trials seleccionados
def cantApariciones(letters,selected_trials):
	array_apariciones = []
	for letter in letters:
		apariciones = (str(selected_trials)).count(letter)
		array_apariciones.append(apariciones)
		print (letter," aparece: ",str(apariciones))

	return array_apariciones

def total_distance(selected_trials):
	total_distance = 0
	for i in range(0,len(selected_trials)):
		 total_distance+=selected_trials[i][1]

	return total_distance

#letters = sorted(trials_raw.box_positions.keys())
letters = list(trials_raw.box_positions.keys())

#Desordeno la lista de letras
#random.shuffle(letters)

letters = ['B', 'C', 'G', 'E', 'H', 'F', 'A', 'I', 'D']

print (letters)
input()

source = "".join(letters)

data = []
seqs = []
data.append(["Trial","NumberMoves","Leftness","Frontness","Length"])
max_distance = 0
selected_trials = [['X',0],['X',0],['X',0],['X',0],['X',0],['X',0],['X',0],['X',0]]
data_trial = []
#for i in range(8,0,-1): #Construyo de mayor a menor
for i in range(0,8+1): #Construyo de menor a mayor
	#max_distance = 0
	min_distance = 100
	c = 0
	for seq in itertools.combinations(letters,i):
		#print ("for ", "".join(seq))
		for trial in itertools.permutations(seq):
			c += 1
			data.append(["".join(trial),                  #trial
						i,                             # number
						trials_raw.leftness(trial),     # leftness
						trials_raw.frontness(trial),    # frontness length
						sum(trials_raw.distances(trial)),    # length
			]) #ntrial,  umber, leftness, frontness, length
			#if sum(trials_raw.distances(trial)) >= max_distance and notHasSubsequence(trial,selected_trials):
			#if sum(trials_raw.distances(trial)) <= min_distance and notHasSubsequence(trial,selected_trials):
			#if sum(trials_raw.distances(trial)) >= max_distance and noHaySubsecuenciasCargadas(trial, selected_trials):
			if sum(trials_raw.distances(trial)) <= min_distance and noHaySubsecuenciasCargadas(trial, selected_trials):
				print("Va ganando ","".join(trial)," con distancia: ",sum(trials_raw.distances(trial)))
				#max_distance = sum(trials_raw.distances(trial))
				min_distance = sum(trials_raw.distances(trial))
				data_trial = ["".join(trial),sum(trials_raw.distances(trial))]
				selected_trials[i-1] = data_trial
				print (selected_trials)
	#print("For ", i, " there are ", c, "different trials")

print (selected_trials)
array_apariciones = cantApariciones(letters,selected_trials)
print ("Varianza: ",str(statistics.variance(array_apariciones)))
print ("Distancia: ",str(total_distance(selected_trials)))

with open("theory.csv", 'w') as fp:
    a = csv.writer(fp, delimiter=';')
    a.writerows(data)
