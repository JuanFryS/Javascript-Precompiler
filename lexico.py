# Juan Francisco Salamanca Carmona #

import sys

letras = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
		'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
digitos = ['0','1','2','3','4','5','6','7','8','9']
sep = ['(',')','{','}',';',',']
ops = ["+","=","|"]
palres =["if","do","while",'var','function','return',"true","false","prompt","document.write"]
coment = ['/']

salida = open("./salida.txt","w")
tokens = []
linea = 0 
colum = 0
lexema = ""
caracter = ''
fuente = open(sys.argv[1]) #abrimos el fichero
entrada = fuente.readlines() #lo ponemos en entrada

# Axioma S. Seria el primer estado del AFD

def main():
	global lexema,letras,sep,ops,caracter,linea,colum,tokens
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
			print("ERROR: "+caracter+" no es un simbolo valido ["+str(linea+1)+","+str(colum)+"]")
			caracter = sigCar();
	print tokens
#	return tokens
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
		return

def identificador():
	global lexema, caracter
#	caracter = sigCar()
	while caracter in letras or caracter in digitos or caracter == '_':
		lexema = lexema + caracter
		caracter = sigCar()
		if caracter == '.':
			lexema = lexema + caracter
			caracter = sigCar()
			escritura()
			return
	if lexema in palres:
		TokenPR(lexema)
	else:
		TokenID(lexema)
		
def escritura():
	global lexema, caracter
	while caracter in letras:
		lexema = lexema + caracter
		caracter = sigCar()
	if lexema != 'document.write':
		print("ERROR: "+lexema+" no es una palabra valida ["+str(linea+1)+","+str(colum)+"]")
	else:
		TokenPR(lexema)

def separador():
	TokenSEP(lexema)


def comentario():
	global caracter, lexema
	if caracter in coment:
		while caracter != '\n':
			lexema = lexema + caracter
			caracter = sigCar()
	else: 		
		print("ERROR: \""+lexema+"\" no es un comentario valido. Ayuda: \"//\" ["+str(linea+1)+","+str(colum)+"]")

# Funcion para avanzar de caracter

def sigCar():
	global colum, linea, entrada
	lin = entrada[linea]
	car = lin[colum]
	colum = colum + 1
	return car
	
# Definicion de los tokens

def TokenDEC(lexema):
	global tokens, salida
	tdec ={"codigo": lexema, "linea": linea, "colum": colum}
	tokens.append(tdec)
	salida.write("(DEC, "+lexema+")\n")
#	print("(DECIMAL, "+lexema+")")
	
def TokenCAD(lexema):
	global tokens
	tcad ={"codigo": lexema, "linea": linea, "colum": colum}
	tokens.append(tcad)
	salida.write("(CAD, "+lexema+")\n")

def TokenOP(lexema):
	global tokens,salida
	top ={"codigo": lexema, "linea": linea, "colum": colum}
	tokens.append(top)
	salida.write("(OP, "+lexema+")\n")

def TokenSEP(lexema):
	global tokens,salida
	tsep ={"codigo": lexema, "linea": linea, "colum": colum}
	tokens.append(tsep)
	salida.write("(SEP, "+lexema+")\n")
	
def TokenID(lexema):
	global tokens,salida
	tid ={"codigo": lexema, "linea": linea, "colum": colum}
	tokens.append(tid)
	salida.write("(ID, "+lexema+")\n")
	
def TokenPR(lexema):
	global tokens, salida
	tpr ={"codigo": lexema, "linea": linea, "colum": colum}
	tokens.append(tpr)
	salida.write("(PR, "+lexema+")\n")

def TokenSL():
	global tokens,salida
	tsl ={"codigo": "SL", "linea": linea, "colum": colum}
	tokens.append(tsl)
	salida.write("(SL, "+lexema+")\n")

# MAIN

if __name__ == "__main__":
	main()