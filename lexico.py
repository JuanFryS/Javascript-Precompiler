# -*- coding: UTF-8 -*-
# Juan Francisco Salamanca Carmona #

#
#	En este archivo se encuentra el código correspondiente al
#	Analizador Léxico
#


import sys

letras = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
		'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
digitos = ['0','1','2','3','4','5','6','7','8','9']
sep = ['(',')','{','}',';',',']
ops = ["+","=","|"]
palres =["if","do","while",'var','function','return',"true","false","prompt","document.write"]
coment = ['/']
tokens = []
linea = 0 
colum = 0
lexema = ""
caracter = ''
ambito = "global"

cont = 100
aux = ""

fich_tokens = open("./resultados/tokens.txt","w")
ts = None
entrada = None

# Axioma S. Seria el primer estado del AFD

def main(entradaSem, tablaGeneral, nombre, fich_error):
	global lexema,letras,sep,ops,caracter,linea,colum,tokens, entrada, ts
	entrada = entradaSem
	ts = tablaGeneral
	fich_tokens.write("---------------> ")
	fich_tokens.write(nombre)
	fich_tokens.write(" <---------------\n")

	caracter = sigCar()
	while(caracter):
		lexema = ""
		if caracter in digitos: # DIGITOS
			lexema = lexema + caracter
			caracter = sigCar()
			digito()
		elif caracter == '\"': # CADENAS
			caracter = sigCar()
			cadena()
		elif caracter in ops: # OPERADORES
			lexema = lexema + caracter
			caracter = sigCar()
			operador() 
		elif caracter in letras: # DECLARACIONES/IDENTIFICADORES
			lexema = lexema + caracter
			caracter = sigCar()
			identificador()
		elif caracter in sep: #ELEMENTOS SEPARADORES
			lexema = lexema + caracter
			separador()
			caracter = sigCar()
		elif caracter in coment: # COMENTARIOS
			lexema = lexema + caracter
			caracter = sigCar()
			comentario()
			colum = 0
			linea = linea + 1
			if linea < len(entrada):
				caracter = sigCar()
			else: 
				caracter = None
		elif caracter == ' ' or caracter == '\t': # ESPACIOS EN BLANCO O TABULACIONES
			caracter = sigCar()
		elif caracter == '\n': # SALTOS DE LINEA
			colum = 0
			linea = linea + 1
			TokenSL()
			if linea < len(entrada):
				caracter = sigCar()
			else: 
				caracter = None		
		else: # CASO EN EL QUE NO SE CUMPLA NINGUNA DE LAS REGLAS ANTERIORES -> LO LEIDO NO ES ENTENDIDO POR LA GRAMATICA
			fich_tokens.write("ERROR: "+caracter+" no es un simbolo valido ["+str(linea+1)+","+str(colum)+"]\n")
			caracter = sigCar();
	fich_tokens.close()
	return tokens
# Los diferentes estados del automata

def digito():
	global lexema, caracter
	while caracter in digitos:
		lexema = lexema + caracter
		caracter = sigCar()
	TokenDEC(lexema)

def cadena():
	global lexema, caracter
	while caracter != '\"':
		lexema = lexema + caracter
		caracter = sigCar()
	caracter = sigCar()
	TokenCAD(lexema)

def operador():
	global lexema, caracter
#	caracter = sigCar()
	if caracter == '=':
		lexema = lexema + caracter
		caracter = sigCar()
		TokenOP(lexema)
	elif caracter == '|':
		lexema = lexema + caracter
		caracter = sigCar()
		TokenOP(lexema)
	elif lexema == '+' or lexema == '=':
		TokenOP(lexema)
	else:
		print("ERROR: "+lexema+" no es un simbolo valido ["+str(linea+1)+","+str(colum-1)+"]")
		fich_error.write("ERROR: "+lexema+" no es un simbolo valido ["+str(linea+1)+","+str(colum-1)+"]")

def identificador():
	global lexema, caracter, ambito, ts,cont,aux
#	caracter = sigCar()
	while caracter in letras or caracter in digitos or caracter == '_':
		lexema += caracter
		caracter = sigCar()	
		if caracter == ".":
			if lexema == "document":
				lexema += caracter
				caracter = sigCar()
				escritura()
			else:
				print("Error en la línea " + str(linea) + ", columna " + str(colum) + ": se recibe un punto (.) cuando no corresponde")
				fich_error.write("Error en la línea " + str(linea) + ", columna " + str(colum) + ": se recibe un punto (.) cuando no corresponde")

	if ts.esPR(lexema):
		if lexema == "function":
			cont = 2
#			print("ambito en el lexico:")
#			print(ambito)
		TokenPR(lexema)
	elif not ts.busca_lexema(lexema):
		cont = cont - 1
#		print("contador: ")
#		print(cont)
#		if cont == 1:
#			print("lexema:")
#			print(lexema)
#			aux = lexema
		if cont == 0:
#			print("aux?")
#			print(aux)
			ts.anadirIDTS(lexema,"")
			cont = 1000
		else:
#			print("lexema:")
#			print(lexema)
#			print("resultado busqueda:")
#			print(ts.busca_lexema(lexema))
#			print("ambito:")
#			print(ambito)
			ts.anadirIDTS(lexema,ambito)
			ambito = "global"
#			print("resultado añadir:")
#			print(ts.busca_lexema(lexema))
		TokenID(lexema)
	else:
		TokenID(lexema)
		
def escritura():
	global lexema, caracter
	while caracter in letras:
		lexema = lexema + caracter
		caracter = sigCar()
	if lexema != "document.write":
		print("ERROR: "+lexema+" no es una palabra valida ["+str(linea+1)+","+str(colum)+"]")
		fich_error.write("ERROR: "+lexema+" no es una palabra valida ["+str(linea+1)+","+str(colum)+"]")
	#else:
	#	TokenPR(lexema)

def separador():
	TokenSEP(lexema)

def comentario():
	global caracter, lexema,fich_error
	if caracter in coment:
		while caracter != '\n':
			lexema = lexema + caracter
			caracter = sigCar()
	else: 		
		print("ERROR: \""+lexema+"\" no es un comentario valido. Ayuda: \"//\" ["+str(linea+1)+","+str(colum)+"]")
		fich_error.write("ERROR: \""+lexema+"\" no es un comentario valido. Ayuda: \"//\" ["+str(linea+1)+","+str(colum)+"]")
# Funcion para avanzar de caracter

def sigCar():
	global colum, linea, entrada, lin
	lin = entrada[linea]
	car = lin[colum]
	colum = colum + 1
	return car
	
# Definicion de los tokens

def TokenDEC(lexema):
	global tokens, fich_tokens
	tdec ={"codigo": lexema, "linea": linea, "colum": colum}
	tokens.append(tdec)
	fich_tokens.write("(DEC, "+lexema+")\n")
#	print("(DECIMAL, "+lexema+")")

def TokenCAD(lexema):
	global tokens, fich_tokens
	tcad = {"codigo": lexema, "linea": linea, "colum": colum}
	tokens.append(tcad)
	fich_tokens.write("(CAD, "+lexema+")\n")

def TokenOP(lexema):
	global tokens,fich_tokens
	top ={"codigo": lexema, "linea": linea, "colum": colum}
	tokens.append(top)
	fich_tokens.write("(OP, "+lexema+")\n")

def TokenSEP(lexema):
	global tokens,fich_tokens
	tsep ={"codigo": lexema, "linea": linea, "colum": colum}
	tokens.append(tsep)
	fich_tokens.write("(SEP, "+lexema+")\n")
	
def TokenID(lexema):
	global tokens,fich_tokens
	tid ={"codigo": lexema, "linea": linea, "colum": colum}
	tokens.append(tid)
	fich_tokens.write("(ID, "+lexema+")\n")
	
def TokenPR(lexema):
	global tokens, fich_tokens
	tpr ={"codigo": lexema, "linea": linea, "colum": colum}
	tokens.append(tpr)
	fich_tokens.write("(PR, "+lexema+")\n")

def TokenSL():
	global tokens,fich_tokens
	tsl ={"codigo": "SL", "linea": linea, "colum": colum}
	tokens.append(tsl)
	fich_tokens.write("(SL, "+lexema+")\n")

# MAIN

if __name__ == "__main__":
	main(entrada, ts)