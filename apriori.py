# encoding: utf-8
import numpy as np

# Leitura dos dados
def lerDados(path):
	aux = np.genfromtxt(path, dtype= str, delimiter=";") 
	(linhas, colunas) = aux.shape
	# print linhas, colunas
	nomes = aux[0, :]
	data = []
	for i in range(1, linhas):
		row = []
		j = 0
		for d in aux[i, :]:
			if d != ' ':
				row.append(nomes[j]+d)
			j += 1
		data.append(row)
	return data

def candMinS(dadosConj, candidatos, minSupport):
	aux = {}
	for item in dadosConj:
		for i in candidatos:
			if i.issubset(item):
				aux.setdefault(i, 0)
				aux[i] += 1
	
	n = float(len(dadosConj))
	listCands = []
	dadosSupport = {}
	for k in aux:
		s = aux[k] / n
		if s >= minSupport:
			listCands.insert(0, k)
		dadosSupport[k] = s

	return listCands, dadosSupport

def gereCandidatosK(itemsets,k):
	listCandsK = []
	n = len(itemsets)
	for i in range(n):
		for j in range(i+1, n):
			aux1 = list(itemsets[i])[: k-2]
			aux2 = list(itemsets[j])[: k-2]
			aux1.sort()
			aux2.sort()
			if aux1 == aux2 :
				listCandsK.append(itemsets[i] | itemsets[j])
	return listCandsK

def apriori(dados, minSupport):

	aux = []
	for item in dados:
		for i in item:
			if [i] not in aux:
				aux.append([i])
	aux.sort()
	
	candidatos = map(frozenset, aux) # candidatos de tamanho 1
	data = map(set, dados)

	listCands, dadosSupport = candMinS(data, candidatos, minSupport)
	
	itemsetsCands = [listCands]
	k = 2 
	while (len(itemsetsCands[k-2]) > 0):
		Candsk = gereCandidatosK(itemsetsCands[k-2], k)
		listCandsK, dadosSupportK = candMinS(data, Candsk, minSupport)
		dadosSupport.update(dadosSupportK)
		itemsetsCands.append(listCandsK)
		k += 1

	return itemsetsCands, dadosSupport

def calculeConf(itemsets, conj, dadosSuport, rgrs, minConf):
	poda = []
	for item in conj:
		conf = dadosSuport[itemsets] / dadosSuport[itemsets - item]
		if conf >= minConf :
			# print itemsets - item, ' >>>>> ', item, '----', conf
			rgrs.append((itemsets - item, item, round(conf,2)))
			poda.append(item) 
	return poda

def regrasCand(itemsets, conj, dadosSuport, rgrs, minConf):
	n = len(conj[0])
	m = len(itemsets)
	if m > (n+1):
		aux1 = gereCandidatosK(conj, n+1)
		aux2 = calculeConf(itemsets, aux1, dadosSuport, rgrs, minConf)
		if len(aux2) > 1:
			regrasCand(itemsets, aux2, dadosSuport, rgrs, minConf)

def regras(itemsets, dadosSuport, minConf):
	rgrs = []
	for i in range(1, len(itemsets)):
		for item in itemsets[i]:
			conj = [frozenset([x]) for x in item]
			if i <= 1 :
				calculeConf(item, conj, dadosSuport, rgrs, minConf)
			else:
				regrasCand(item, conj, dadosSuport, rgrs, minConf)

	return rgrs

def escreverResultados(regras):
	arq = open('resultados.txt', 'w')
	result = []
	for r in regras:
		row = ' ('
		for i in list(r[0]):
			row+= ' ' + i + '  '
		row+= ' ) --->  (' 
		for i in list(r[1]):
			row+= ' ' + i + '  '
		row += ')  CONF.: ' +str(r[2])
		result.append(row+'\n')
	arq.writelines(result)
	arq.close()
