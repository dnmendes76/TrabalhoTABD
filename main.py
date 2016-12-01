#!/usr/bin/env python

# encoding: utf-8
import sys
from apriori import *

suporte = 0.2
confianca = 0.8 

if __name__ == '__main__':
	
	path = sys.argv[1:]
	if len(path) == 0:
		print 'Por favor informe a entrada !!'
	else :
		dataset = lerDados(path[0])
		itemsets, dadosSuport = apriori(dataset, suporte)
		regras  = regras(itemsets, dadosSuport, confianca)
		print len(regras)
		escreverResultados(regras)
