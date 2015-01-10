# -*- coding: UTF-8 -*-
# Juan Francisco Salamanca Carmona #

#
#	En este archivo se encuentra el código correspondiente al
#	Analizador Semantico Descendente Recursivo
#

import sys
import tabla_simbolos
import lexico

digitos = ['0','1','2','3','4','5','6','7','8','9']
enterologico = ["entero", "logico", "entlog"]
tsGeneral = None
fich_err = open("errores.txt", "w")
tokens = []
sig_token = {} 
TSactiva = None

tokenPR = {"codigo": "return", "linea": 0, "colum": 0}
tokenIF = {"codigo": "if", "linea": 0, "colum": 0}
tokenDO = {"codigo": "do", "linea": 0, "colum": 0}
tokenW = {"codigo": "while", "linea": 0, "colum": 0}
tokenSL = {"codigo": "SL", "linea": 0, "colum": 0}
tokenPC = {"codigo": ";", "linea": 0, "colum": 0}
tokenDW = {"codigo": "document.write", "linea": 0, "colum": 0}
tokenP = {"codigo": "prompt", "linea": 0, "colum": 0}
tokenF = {"codigo" : "function", "linea" : 0, "colum": 0}
tokenV = {"codigo": "var", "linea": 0, "colum": 0}

tokenTerm = {"codigo" : "", "linea": 0, "colum": 0}	

def error(token):
	print("ERROR: En la línea "+token["linea"]+", columna "+token["colum"]+", se recibe el valor no esperado: "+token["codigo"])
	fich_err.write("ERROR: En la línea "+token["linea"]+", columna "+token["colum"]+", se recibe el valor no esperado: "+token["codigo"]+"\n")

def scan(token):
	global sig_token
	if sig_token["codigo"] == token["codigo"]:
		sig_token = tokens.pop()
		return True	
	else:
		error(sig_token)
		return False

def main():
	fich = open(sys.argv[1])
	entrada = fich.readlines()
	tsGeneral = tabla_simbolos.Tabla(True)
	tokens = lexico.main(entrada, tsGeneral, sys.argv[1], fich_err)
	tokenFIN = {"codigo": "EOF", "linea": 0, "colum": 0}
	tokens.append(tokenFIN)
	tokens.reverse()
	sig_token = tokens.pop()
	estadoP()
	fich.close()
	fich_err.close()

def estadoP():
	TSactiva = tsGeneral
	estadoPprima()
	tabla_simbolos.imprimirTS() #Dependiendo del nombre que se ponga en TS
	tabla_simbolos.vaciar()

def estadoPprima():
	global TSactiva
	# First de regla: P' -> FP'1 : function
	# Caso P' -> FP'1
	if sig_token["codigo"] == tokenF["codigo"]:
		f = estadoF()
		pp = estadoPprima()
		if f == "tipo_ok":
			return pp
		else:
			return "tipo_error"

	# Caso P' -> SP'1
	# First de regla: P' -> SP' : if, do, document.write, prompt, return, id
	elif sig_token[codigo] in [tokenIF[codigo], tokenDO[codigo], tokenDW[codigo], tokenP[codigo], tokenR[codigo]] or TSactiva.busca_lexema(sig_token["codigo"]):
		s = estadoS()
		pp = estadoPprima()
		if s == "tipo_ok":
			return pp
		else:
			return "tipo_error"

	# Caso P' -> DP'1
	# First de regla: P' -> DP' : var
	elif sig_token[codigo] == tokenV[codigo]:
		d = estadoD()
		pp = estadoPprima()
		return pp

	# Caso P' -> Lambda	
	else:
		return "tipo_ok"

def estadoS():
	# S -> if(E) S1
	if sig_token["codigo"] == tokenIF["codigo"]:
		scan(tokenIF)
		tokenTerm["codigo"] = "("
		scan(tokenTerm)
		e = estadoE()
		tokenTerm["codigo"] = ")"
		scan(tokenTerm)
		s = estadoS()
		if e == "logico":
			return s
		else:
			return "tipo_error"

	# S -> do {\n S1S'' \n}while (E)\n
	elif sig_token["codigo"] == tokenDO["codigo"]:
		scan(tokenDO)
		tokenTerm["codigo"] = "{"
		scan(tokenTerm)
		scan(tokenSL)
		s = estadoS()
		s1 = estadoS2prima()
		scan(tokenSL)
		tokenTerm["codigo"] = "}"
		scan(tokenTerm)
		scan(tokenW)
		tokenTerm["codigo"] = "("
		scan(tokenTerm)
		e = estadoE()
		tokenTerm["codigo"] = ")"
		scan(tokenTerm)
		scan(tokenSL)
		if e == "logico" and s1 == "tipo_ok":
			return "tipo_ok"
		else:
			return "tipo_error"

	# S -> doc.write(E); \n
	elif sig_token["codigo"] == tokenDW["codigo"]:
		scan(tokenDW)
		tokenTerm["codigo"] = "("
		scan(tokenTerm)
		e = estadoE()
		tokenTerm["codigo"] = ")"
		scan(tokenTerm)
		scan(tokenPC)
		scan(tokenSL)
		if not (e == "tipo_error"):
			return "tipo_ok"
		else:
			return "tipo_error"

	# S -> prompt(id); \n	
	elif sig_token["codigo"] == tokenP["codigo"]:
		scan(tokenP)
		tokenTerm["codigo"] = "("
		scan(tokenTerm)
		if TSactiva.busca_lexema(sig_token["codigo"]):
			tipo = TSactiva.buscaTipoTS(sig_token["codigo"])
			if tipo == "":
				TSactiva.anadirTipoTS("entero",sig_token["codigo"], "global")
			tokenTerm["codigo"] = ")"
			scan(tokenTerm)	
			scan(tokenPC)
			scan(tokenSL)	
			return "tipo_ok"
		else:
			return "tipo_error"

	# S -> return R; \n
	elif sig_token["codigo"] == tokenPR["codigo"]:
		scan(tokenPR)
		r = estadoR()
		scan(tokenPC)
		scan(tokenSL)
		if funcion: # No sé qué es función
			if r == "enterologico":
				return "tipo_ok"
			else:
				return "tipo_error"
		else:
			##### TENGO QUE DEFINIR QUE ERROR IRÁ AQUÍ.
			error(sig_token["codigo"])
	
	# S -> idS'
	elif TSactiva.busca_lexema(sig_token["codigo"]):
		tipo = TSactiva.buscaTipoTS(sig_token["codigo"])
		if tipo == "":
			TSactiva.anadirTipoTS("entlog", sig_token["codigo"], "global")
		sig_token = tokens.pop()
		sprima = estadoSprima()
		if TSactiva.buscaTipoTS(sig_token["codigo"]) in enterologico and sprima in enterologico:
			return "tipo_ok"
		else:
			return "tipo_error"

#def estadoD():
#	Declaracion = True
#	scan(tokenV)
	# PREGUNTAR A LUIS!!!
			
def estadoZ():
	# Z -> = I
	tokenTerm["codigo"] = "="
	if sig_token["codigo"] == tokenTerm["codigo"]:
		scan(tokenTerm)
		i = estadoI()
		return i
	else:
		return "entero"

def estadoI():
	# I = true
	if sig_token["codigo"] == "true":
		tokenTerm["codigo"] = "true"
		scan(tokenTerm)
		return "logico"
	# I = false
	elif sig_token["codigo"] == "false":
		tokenTerm["codigo"] = "false"
		scan(tokenTerm)
		return logico
	# I = entero
	elif sig_token["codigo"].isdigit():
		scan(sig_token["codigo"])
		return "entero"
	# Se añade este else para contemplar un error???
	else:
		error(sig_token["codigo"])
		return "tipo_error"

def estadoSprima():
	# S' -> =E; \n
	if sig_token["codigo"] == "=":
		tokenTerm["codigo"] = "="
		scan(tokenTerm)
		e = estadoE()
		scan(tokenPC)
		scan(tokenSL)
		return e
	# S' -> +=E; \n
	elif sig_token["codigo"] == "+=":
		tokenTerm["codigo"] = "+="
		scan(tokenTerm)
		e = estadoE()
		scan(tokenPC)
		scan(tokenSL)
		return e
	# Se añade este else para contemplar un error???=
	else:
		error(sig_token["codigo"])
		return "tipo_error"	

def estadoS2prima():
	 # S'' -> SS''1
	if sig_token[codigo] in [tokenIF[codigo], tokenDO[codigo], tokenDW[codigo], tokenP[codigo], tokenR[codigo]] or TSactiva.busca_lexema(sig_token["codigo"]):
		s = estadoS()
		s2prima = estadoS2prima()
		if s == "tipo_ok":
			return s2prima
		else:
			return "tipo_error"
	# S'' -> LAMBDA
	else:
		return "tipo_ok"

def estadoR():
	# R -> E
	# First(E): (, id, ent

	if sig_token["codigo"] == "(" or sig_token["codigo"].isdigit() or TSactiva.busca_lexema(sig_token["codigo"]): 
		e = estadoE()
		return e
	# R -> LAMBDA
	else:
		return "entlog"

def estadoF():
	# F -> function (id)W{S}
	if sig_token["codigo"] == tokenF["codigo"]:
		scan(tokenF)
		zona_funcion = True
		tokenID = {"codigo": sig_token["codigo"], "linea": 0, "colum": 0}
		if TSactiva.busca_lexema(tokenID["codigo"]):
			scan(tokenID)
			TSactiva.anadirTipoTS("funcion", tokenID["codigo"],"global")
			ambito = tokenID["codigo"]
			tokenTerm["codigo"] = "("
			scan(tokenTerm)
			w = estadoW()
			tokenTerm["codigo"] = ")"
			TSactiva.anadirTipoArgs(tokenID["codigo"],w)
			tokenTerm["codigo"] = "{"
			scan(tokenTerm)
			scan(tokenSL)
			s = estadoS
			tokenTerm["codigo"] = "}"
			scan(tokenTerm)
			scan(tokenSL)
			if s == "tipo_ok":
				return "tipo_ok"
			else:
				s == "tipo_error"
			zona_funcion = False

def estadoE():
	# E -> TE'
	t = estadoT()
	eprima = estadoEprima()
	if t in enterologico and eprima == "entlog":
		return t
	elif t in enterologico and eprima in enterologico:
		return "entero"
	else:
		return "tipo_error"

def estadoEprima():
	# E' -> +TE'
	if sig_token["codigo"] == "+":
		tokenTerm["codigo"] = "+"
		scan(tokenTerm)
		t = estadoT()
		eprima = estadoEprima()
		if t in enterologico and eprima == "entlog":
			return t
		elif t in enterologico and eprima in enterologico:
			return "entero"
		else:
			return "tipo_error"
	# E' -> LAMBDA
	else:
		return "entlog"


def estadoT():
	# T -> XT'
	x = estadoX()
	tprima = estadoTprima()
	if x in enterologico and tprima == "entlog":
		return x
	elif x in enterologico and tprima in enterologico:
		return "entero"
	else:
		return "tipo_error"

def estadoTprima():
	# T' -> ==XT'
	if sig_token["codigo"] == "==":
		tokenTerm["codigo"] = "=="
		scan(tokenTerm)
		x = estadoX()
		tprima = estadoTprima()
		if x in enterologico and tprima == "entlog":
			return x
		elif x in enterologico and tprima in enterologico:
			return "logico"
		else:
			return "tipo_error"
	# T' -> LAMBDA		
	else:
		return "entlog"

def estadoX():
	# X -> GX'
	g = estadoG()
	xprima = estadoXprima()
	if g in enterologico and xprima == "entlog":
		return g
	elif g in enterologico and xprima in enterologico:
		return "logico"
	else:
		return "tipo_error"

def estadoXprima():
	# X' -> ||GX'
	if sig_token["codigo"] == "||":
		tokenTerm["codigo"] = "||"
		scan(tokenTerm)
		g = estadoG()
		xprima = estadoXprima()
		if g in enterologico and xprima == "entlog":
			return g
		elif g in enterologico and xprima in enterologico:
			return "logico"
		else:
			return "tipo_error"
	# X' -> LAMBDA
	else:
		return "entlog"

def estadoG():
	# G -> (E)
	if sig_token["codigo"] == "(":
		tokenTerm["codigo"] = "("
		scan(tokenTerm)
		e = estadoE()
		if sig_token["codigo"] == ")":
			tokenTerm["codigo"] = ")"
			scan(tokenTerm)
			return e
	# G -> idG'
	elif TSactiva.busca_lexema(sig_token["codigo"]):
		tipo = TSactiva.buscaTipoTS(sig_token["codigo"])
		if tipo == "":
			TSactiva.anadirTipoTS("entero", tokenID["codigo"],"global")
			tipo = activa.buscaTipoTS(sig_token["codigo"])
		scan(sig_token["codigo"])
		gprima = estadoGprima()
		if tipo in enterologico and gprima == "entlog":
			return tipo
		elif tipo in enterologico and not gprima == "entlog":
			if TSactiva.sonTiposIguales(tipo, gprima):
				return "entlog"
			else:
				return "tipo_error"
		else:
			return "tipo_error"
	# G -> ent
	elif sig_token["codigo"].isdigit():
		scan(sig_token["codigo"])
		return "entero"
	else:
		return "tipo_error"

def estadoGprima():	
	# G' -> (L)
	if sig_token["codigo"] == "(":
		tokenTerm["codigo"] = "("
		scan(tokenTerm)
		l = esadoL()
		if sig_token["codigo"] == ")":
			tokenTerm["codigo"] = ")"
			scan(tokenTerm)
			return l
		else:
			return "tipo_error"
	# G' -> LAMBDA
	else:
		return "entlog"

def estadoL():
	#L -> EL'
	if sig_token["codigo"] == "(" or sig_token["codigo"].isdigit() or TSactiva.busca_lexema(sig_token["codigo"]): 
		e = estadoE()
		auxiliar.append(e)
		lprima = estadoLprima()
		if e == "tipo_error" or lprima == "tipo_error":
			return "tipo_error"
		elif lprima == "tipo_ok":
			return e
		else:
			tupla = tuple(auxiliar)
			return auxiliar
	# L -> LAMBDA
	else:
		return "tipo_ok"


def estadoLprima():	
	# L' -> ,L
	if sig_token["codigo"] == ",":
		tokenTerm["codigo"] = ","
		scan(tokenTerm)
		l = estadoL()
		return l
	# L' -> LAMBDA
	else:
		return "tipo_ok"

def estadoW():
	#W -> idW'
	if TSactiva.busca_lexema(sig_token["codigo"]):
		TSactiva.anadirTipoTS("entlog", sig_token["codigo"], ambito)
		scan(sig_token["codigo"])
		auxiliar.append("entlog")
		wprima = estadoWprima()
		if wprima == "tipo_ok":
			return "entlog"
		else:
			t = tuple(aux_params)
			return t
	# W -> LAMBDA
	else:
		return "tipo_ok"

def estadoWprima():	
	# W' -> ,W
	if sig_token["codigo"] == ",":
		tokenTerm["codigo"] = ","
		scan(tokenTerm)
		w = estadoW()
		return w
	# W' -> LAMBDA
	else:
		return "tipo_ok"

if __name__ == "__main__":
	main()
