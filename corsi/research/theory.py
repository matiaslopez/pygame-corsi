import trials_raw
import itertools
import csv

def notIsSubsequence(trial,selected_trials):
	notIsSubsequence = True
	print selected_trials	
	#Veo si no hay substrings con los anteriores
	for i in range(0,len(trial)-1):
		print "Chequeo si "+"".join(trial)+" tiene algun elemento en: "+selected_trials[i][0]
		for j in range(0,len(trial)):
			if str(trial[j]) in str(selected_trials[i][0]):
				print(str(trial[j]), " is in ",selected_trials[i][0])
				return False
				

	return True


print "###################################################################################"
letters = sorted(trials_raw.box_positions.keys())

source = "".join(letters)

data = []
seqs = []
data.append(["Trial","NumberMoves","Leftness","Frontness","Length"])
max_distance = 0
selected_trials = [['X',0],['X',0],['X',0],['X',0],['X',0]]
data_trial = []
for i in range(1,5,1):
	max_distance = 0
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
			if notIsSubsequence(trial,selected_trials) and sum(trials_raw.distances(trial)) > max_distance:
				print("Va ganando ","".join(trial)," con distancia: ",sum(trials_raw.distances(trial)))
				max_distance = sum(trials_raw.distances(trial))
				data_trial = ["".join(trial),sum(trials_raw.distances(trial))]
				selected_trials[i-1] = data_trial
	#print("For ", i, " there are ", c, "different trials")
print selected_trials

with open("theory.csv", 'w') as fp:
    a = csv.writer(fp, delimiter=';')
    a.writerows(data)
