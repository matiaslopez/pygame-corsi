import trials_raw
import itertools
import csv
import statistics
import random
from random import shuffle

#Chequea que el todo trial no sea subsecuencia de los ya cargados (pero no partes de el)
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
def notHasSubsequence(trial,selected_trials, sum_distances_trials): #Para construccion de mayor a menor
	print ("Analizo: "+"".join(trial),"con distancia: ",sum_distances_trials)
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
def noHaySubsecuenciasCargadas(trial, selected_trials, sum_distances_trials): #Para construccion de menor a mayor
	print ("Analizo: "+"".join(trial),"con distancia: ",sum_distances_trials)
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

def reset_distance_reference(difficulty):
	if difficulty == "e":
		#Con los faciles minimizo distancias, inicio grande
		return 1000
	else: 
		#Con los dificiles maximizo distancias, inicio en 0
		return 0


#Consulto parametros al usuario
print("Longitud maxima: (1-9)[8]")
trial_max_length = input()
if trial_max_length != "" and 1 <= int(trial_max_length) <= 9:
	trial_max_length = int(trial_max_length)
else:
	trial_max_length = 8

print("Trials por cada longitud: (1-6)[2]")
trials_per_length = input()
if trials_per_length != "" and 1 <= int(trials_per_length) <= 6:
	trials_per_length = int(trials_per_length)
else:
	trials_per_length = 2

print("Protocolo facil (e) o dificil (h): [h]")
difficulty = input()
if difficulty == "e":
	#Con los faciles minimizo distancias, inicio grande
	distance_reference = 1000
else: 
	#Con los dificiles maximizo distancias, inicio en 0
	distance_reference = 0
	difficulty = "h"

print("Construyo menor a mayor (n) o mayor a menor (y): [y]")
mayor_menor = input()
#Si eligio de menor a mayor
if mayor_menor == "n":
	start_index = 1
	end_index = trial_max_length+1
	step = 1
else: #Si eligio de mayor a menor
	mayor_menor = "y"
	start_index = trial_max_length
	end_index = 0
	step = -1

#letters = sorted(trials_raw.box_positions.keys())
letters = list(trials_raw.box_positions.keys())

#Desordeno la lista de letras
#random.shuffle(letters)

print (letters)
input()

source = "".join(letters)

data = []
seqs = []
data.append(["Trial","NumberMoves","Leftness","Frontness","Length"])
max_distance = 0
selected_trials = [['X',0],['X',0],['X',0],['X',0],['X',0],['X',0],['X',0],['X',0]]
data_trial = []
for i in range(start_index,end_index,step):
	print ("Index: ",i)
	#Reinicio distance_reference
	distance_reference = reset_distance_reference(difficulty)
	for seq in itertools.combinations(letters,i):
		#print ("for ", "".join(seq))
		for trial in itertools.permutations(seq):			
			#print ("Evaluo: ", "".join(trial))
			sum_distances_trials = sum(trials_raw.distances(trial))

			#A menos que mejore, no agrego trial
			add_trial = False

			#Si hay que armar protocolos faciles y de menor a mayor
			if difficulty == "e" and mayor_menor == "n":
				if sum_distances_trials <= distance_reference and noHaySubsecuenciasCargadas(trial,selected_trials,sum_distances_trials): #menor a Mayor, minimo
					add_trial = True

			#Si hay que armar protocolos faciles y de mayor a menor
			elif difficulty == "e" and mayor_menor == "y":
				if sum_distances_trials <= distance_reference and notHasSubsequence(trial,selected_trials,sum_distances_trials): #mayor a menor, minimo
					add_trial = True

			#Si hay que armar protocolos dificiles y de menor a mayor
			elif difficulty == "h" and mayor_menor == "n":
				if sum_distances_trials >= distance_reference and noHaySubsecuenciasCargadas(trial, selected_trials,sum_distances_trials): #menor a mayor, maximo
					add_trial = True

			#Si hay que armar protocolos dificiles y de mayor a menor
			elif difficulty == "h" and mayor_menor == "y":
				if sum_distances_trials >= distance_reference and notHasSubsequence(trial,selected_trials,sum_distances_trials): #mayor a menor, maximo
					add_trial = True

			#Si hay que agregar el Trial
			if add_trial:
					print("Va ganando ","".join(trial)," con distancia: ",str(sum_distances_trials))
					data_trial = ["".join(trial),sum_distances_trials]
					selected_trials[i-1] = data_trial
					distance_reference = sum_distances_trials
					print (selected_trials)


print (selected_trials)
array_apariciones = cantApariciones(letters,selected_trials)
print ("Varianza: ",str(statistics.variance(array_apariciones)))
print ("Distancia: ",str(total_distance(selected_trials)))

#with open("theory.csv", 'w') as fp:
#    a = csv.writer(fp, delimiter=';')
#    a.writerows(data)
