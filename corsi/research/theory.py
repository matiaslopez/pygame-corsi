import trials_raw
import itertools
import csv
import statistics
import json
import random
from random import shuffle
from collections import deque


total_sequences_inserted = 0
#letters = sorted(trials_raw.box_positions.keys())
letters = list(trials_raw.box_positions.keys())
shuffle_letters = list(trials_raw.box_positions.keys())



#Chequea que el todo trial no sea subsecuencia de los ya cargados (pero no partes de el)
def notIsSubsequence(trial,selected_trials):
	trial = "".join(trial)
	#print (selected_trials)	
	#Veo si no hay substrings con los anteriores (los de mayor longitud)
	for i in range(len(trial),len(selected_trials)):
		print ("Chequeo si ",trial," es substring de: ",selected_trials[i][0])
		if trial in str(selected_trials[i][0]):
			print(trial, " is in ",selected_trials[i][0])
			return False
				
	return True

#Chequea que el trial no contenga subsecuencias (tomando de a 2) de los ya cargados
def notHasSubsequence(trial,selected_trials, sum_distances_trials,total_sequences_inserted): #Para construccion de mayor a menor
	#print ("Analizo: "+"".join(trial),"con distancia: ",sum_distances_trials)
	#Veo si no hay substrings con los anteriores (los de mayor longitud)
	for j in range(len(selected_trials)-total_sequences_inserted,len(selected_trials)):
		#Si no hay con quien analizar, salto
		if selected_trials[j][0] == 'X':
			return True

		#Tomo el trial de a 2
		for i in range(1,len(trial)):
			deAdos = []
			deAdos.append(trial[i-1])
			deAdos.append(trial[i])
			junto = "".join(deAdos)
			#print ("Chequeo si ",junto," es substring de: ",selected_trials[j][0])
			if junto in str(selected_trials[j][0]):
				#print(junto, " is in ",selected_trials[j][0])
				return False

	return True

#Chequea si el trial que voy a cargar tiene subsecuencias ya utilizadas 
def noHaySubsecuenciasCargadas(trial, selected_trials, sum_distances_trials,total_sequences_inserted): #Para construccion de menor a mayor
	#print ("Analizo: "+"".join(trial),"con distancia: ",sum_distances_trials)
	#Si hay al menos 5 insertados, comparo con menos cantidad
	if (total_sequences_inserted < 5):
		start_index = 0
	else:
		start_index = total_sequences_inserted-5

	#Veo si no hay substrings con los anteriores (los de menor longitud)
	for j in range(start_index,total_sequences_inserted):
		#Si no hay con quien analizar, salto
		if selected_trials[j][0] == 'X':
			return True
		#Tomo el trial de a 2
		for i in range(1,len(trial)):
			deAdos = []
			deAdos.append(trial[i-1])
			deAdos.append(trial[i])
			junto = "".join(deAdos)
			#print ("Chequeo si ",junto," es substring de: ",selected_trials[j][0])
			if junto in str(selected_trials[j][0]):
				#print(junto, " is in ",selected_trials[j][0])
				return False

	return True

#Chequea que el trial no contenga subsecuencias entre los best_trials
def best_sequences_has_not_subsequences(trial,best_trials):
	#print ("Analizo: "+"".join(trial)," en best_sequences: ")
	#Veo si no hay substrings con los anteriores (los de menor longitud)
	for bt in best_trials:
		#Tomo el trial de a 2
		for i in range(1,len(trial)):
			deAdos = []
			deAdos.append(trial[i-1])
			deAdos.append(trial[i])
			junto = "".join(deAdos)
			#print ("Chequeo si ",junto," es substring deque: ",bt[0])
			if junto in str(bt[0]):
				#print(junto, " is in ",bt[0])
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
print("Longitud maxima: (2-9)[8]")
trial_max_length = input()
if trial_max_length != "" and 2 <= int(trial_max_length) <= 9:
	trial_max_length = int(trial_max_length)
else:
	trial_max_length = 8

print("Trials por cada longitud: (1-6)[2]")
trials_per_length = input()
if trials_per_length != "" and 1 <= int(trials_per_length) <= 6:
	trials_per_length = int(trials_per_length)
else:
	trials_per_length = 2

#Inicializo array
selected_trials = []
for s in range(4,(trial_max_length-1)*trials_per_length+4):
	selected_trials.append(['X',0])


print("Protocolo facil (e) o dificil (h): [h]")
difficulty = input()
if difficulty == "e":
	#Con los faciles minimizo distancias, inicio grande
	distance_reference = 1000
else: 
	#Con los dificiles maximizo distancias, inicio en 0
	distance_reference = 0
	difficulty = "h"

print("Construyo menor a mayor (n) o mayor a menor (y): [n]")
mayor_menor = input()

if mayor_menor == "y": #Si eligio de mayor a menor
	start_index = trial_max_length
	end_index = 1
	step = -1
else: #Si eligio de menor a mayor
	mayor_menor = "n"
	start_index = 2
	end_index = trial_max_length+1
	step = 1

print (letters)
print(selected_trials)
input()

source = "".join(letters)

test_trials = ['A','BC','D','EF']

data = []
seqs = []
data.append(["Trial","NumberMoves","Leftness","Frontness","Length"])
max_distance = 0
#selected_trials = [['X',0],['X',0],['X',0],['X',0],['X',0],['X',0],['X',0],['X',0]]

#Multiplicador para la cantidad de variantes
best_sequences_multiplier = 4
best_trials = deque(maxlen=trials_per_length*best_sequences_multiplier)
#best_trials = deque(maxlen=trials_per_length)
data_trial = []
for i in range(start_index,end_index,step):
	#Desordeno la lista de letras
	random.shuffle(letters)

	#print ("Index: ",i)
	best_trials.clear()
	#Cantidad de secuencias de esta longitud insertadas
	sequences_inserted = 0
	num_iteration = 0

	distance_reference = reset_distance_reference(difficulty)
	for seq in itertools.combinations(letters,i):
		#print ("for ", "".join(seq))
		for trial in itertools.permutations(seq):			
			#print ("Evaluo: ", "".join(trial))
			sum_distances_trials = sum(trials_raw.distances(trial))

		# #Si todavia no agregue un minimo, determino que se agregue por mas que sea feo
		# #Esto me evita que pinche por haber empezado a seleccionar entre los y no llegue a la cantidad minima
		# if (num_iteration < trials_per_length):
		# 	#print("Entra de una: ","".join(trial))
		# 	add_trial = True
		# 	num_iteration+=1
		# else:	
		 	#A menos que mejore, no agrego trial
			add_trial = False

			#Si hay que armar protocolos faciles y de menor a mayor
			if difficulty == "e" and mayor_menor == "n":
				if sum_distances_trials < distance_reference and noHaySubsecuenciasCargadas(trial,selected_trials,sum_distances_trials,total_sequences_inserted): #menor a Mayor, minimo
					#Comparo contra las temporales
						if best_sequences_has_not_subsequences(trial,best_trials):
							add_trial = True

			#Si hay que armar protocolos faciles y de mayor a menor
			elif difficulty == "e" and mayor_menor == "y":
				if sum_distances_trials < distance_reference and notHasSubsequence(trial,selected_trials,sum_distances_trials,total_sequences_inserted): #mayor a menor, minimo
					#Comparo contra las temporales
						if best_sequences_has_not_subsequences(trial,best_trials):
							add_trial = True

			#Si hay que armar protocolos dificiles y de menor a mayor
			elif difficulty == "h" and mayor_menor == "n":
				if sum_distances_trials > distance_reference and noHaySubsecuenciasCargadas(trial, selected_trials,sum_distances_trials,total_sequences_inserted): #menor a mayor, maximo
					#Comparo contra las temporales
						if best_sequences_has_not_subsequences(trial,best_trials):
							add_trial = True

			#Si hay que armar protocolos dificiles y de mayor a menor
			elif difficulty == "h" and mayor_menor == "y":
				if sum_distances_trials > distance_reference and notHasSubsequence(trial,selected_trials,sum_distances_trials,total_sequences_inserted): #mayor a menor, maximo
					#Comparo contra las temporales
						if best_sequences_has_not_subsequences(trial,best_trials):
							add_trial = True

			#Si hay que agregar el Trial
			if add_trial:
					#print("Va ganando ","".join(trial)," con distancia: ",str(sum_distances_trials))
					data_trial = ["".join(trial),sum_distances_trials]
					#Agrego a la lista de mejores secuencias
					best_trials.appendleft(data_trial)
					#print("Best trials: ",best_trials)
					#input()
					distance_reference = sum_distances_trials

	#Al finalizar de recorrer las posibilidades para esa longitud
	for k in range(trials_per_length):
		#Selecciono al azar
		sel_trial = random.choice(best_trials)
		selected_trials[i*trials_per_length-4+sequences_inserted] = sel_trial
		#Elimino para no volver a elegirlo
		best_trials.remove(sel_trial)
		sequences_inserted+=1
		total_sequences_inserted+=1
		print (selected_trials)

#selected_trials = [['CI', 2.5465663156493688], ['AF', 4.718315377335432], ['EIG', 3.7837065525672413], ['FBC', 3.989457745842649], ['BACD', 10.510972570693527], ['DCGB', 11.695386943927009], ['CEAID', 10.53479450854563], ['CHAFE', 13.359770070414678], ['IFGEBA', 13.39742254660991], ['DBEHCA', 14.004627912917869], ['BIHDGEC', 12.1102144876221], ['DIGHBAC', 16.452949334268038], ['GADCIFHE', 17.493655490522194], ['GDHAEFIB', 16.1998722513828]]
#selected_trials = [['IG', 2.4627220712049507], ['AI', 3.438386249390839], ['EBA', 3.763627349568119], ['CGA', 6.912614297708431], ['IEFC', 4.101307268426162], ['IHGD', 4.377106021207884], ['HDABI', 8.214023416434735], ['AGHEB', 7.490400975095277], ['CEGADB', 10.180732422097144], ['BEDHIG', 9.8569588763519], ['BCDEIFH', 14.51610681356319], ['GBIDHFC', 15.215536127771989], ['FEDIGACB', 17.138275366649765], ['GDABIEHC', 15.185178745925693]]

print("Trials generados: ")
print (selected_trials)
array_apariciones = cantApariciones(letters,selected_trials)
print ("Varianza: ",str(statistics.variance(array_apariciones)))
print ("Distancia: ",str(total_distance(selected_trials)))

json_trials = ""

#Armo formato json para protocolo
for i in range(len(selected_trials)+len(test_trials)):
	if i <=3:
		registro = "\""+format(i+1)+"\": [\""+test_trials[i]+"\", \"True\"],\n"
		json_trials+=registro
	else:
		registro = "\""+format(i+1)+"\": [\""+selected_trials[i-4][0]+"\", \"False\"],\n"
		json_trials+=registro

#Le saco la ultima coma
json_trials = json_trials[0:-2]

with open('trials.txt', 'w') as outfile:
    outfile.write(json_trials)