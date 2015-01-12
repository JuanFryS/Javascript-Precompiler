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
fich_err = open("pruebas/errores.txt", "w")
fich_parse = "pruebas/parse_" + sys.argv[1] + ".txt"
parse = open(fich_parse,"w")
fich_ts = open("./pruebas/fich_ts.txt","w")
tokens = []
sig_token = {} 
TSactiva = None
reglas=[]

tokenPR = {"codigo": "return", "linea": 0, "colum": 0}
tokenIF = {"codigo": "if", "linea": 0, "colum": 0}
tokenDO = {"codigo": "do", "linea": 0, "colum": 0}
tokenW = {"codigo": "while", "linea": 0, "colum": 0}
tokenSL = {"codigo": "SL", "linea": 0, "colum": 0}
tokenPC = {"codigo": ";", "linea": 0, "colum": 0}
tokenDW = {"codigo": "document.write", "linea": 0, "colum": 0}
tokenP = {"codigo": "prompt", "linea": 0, "colum": 0}
tokenF = {"codigo": "function", "linea" : 0, "colum": 0}
tokenV = {"codigo": "var", "linea": 0, "colum": 0}
tokenR = {"codigo": "return", "linea": 0, "colum": 0}
# Token auxiliar para simbolos diferentes a los contemplados anteriormente.
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
	global sig_token,tokens,tsGeneral
	fich = open(sys.argv[1])
	entrada = fich.readlines()
	tsGeneral = tabla_simbolos.Tabla(True)
	tokens = lexico.main(entrada, tsGeneral, sys.argv[1], fich_err)
	tokenFIN = {"codigo": "EOF", "linea": 0, "colum": 0}
	tokens.append(tokenFIN)
	tokens.reverse()
	sig_token = tokens.pop()

	fich_ts.write("---------------> ")
	fich_ts.write("Tabla de simbolos de: " + sys.argv[1] )
	fich_ts.write(" <---------------\n")

	estadoP()
	for regla in reglas:
		parse.write(regla + "\n")
	parse.close()
	fich.close()
	fich_err.close()

def estadoP():
	global TSactiva, reglas
	TSactiva = tsGeneral
	reglas.append("D 1 ")
	estadoPprima()
	tsGeneral.imprimirTS(fich_ts,"global") #Dependiendo del nombre que se ponga en TS
	tsGeneral.vaciar()

def estadoPprima():
	global  sig_token, reglas, TSactiva
	# First de regla: P' -> FP'1 : function
	# Caso P' -> FP'1
	if sig_token["codigo"] == tokenF["codigo"]:
		reglas.append("2 ")
		f = estadoF()
		pp = estadoPprima()
		if f == "tipo_ok":
			return pp
		else:
			return "tipo_error"

	# Caso P' -> SP'1
	# First de regla: P' -> SP' : if, do, document.write, prompt, return, id
	elif sig_token["codigo"] in [tokenIF["codigo"], tokenDO["codigo"], tokenDW["codigo"], tokenP["codigo"], tokenR["codigo"]] or TSactiva.busca_lexema(sig_token["codigo"]):
		reglas.append("3 ")
		s = estadoS()
		pp = estadoPprima()
		if s == "tipo_ok":
			return pp
		else:
			return "tipo_error"

	# Caso P' -> DP'1
	# First de regla: P' -> DP' : var
	elif sig_token["codigo"] == tokenV["codigo"]:
		reglas.append("4 ")
		d = estadoD()
		pp = estadoPprima()
		return pp

	# Caso P' -> Lambda	
	else:
		reglas.append("5 ")
		return "tipo_ok"

def estadoS():
	global sig_token,reglas,tokenTerm,TSactiva
	# S -> if(E) S1
	if sig_token["codigo"] == tokenIF["codigo"]:
		reglas.append("6 ")
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
		reglas.append("7 ")
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
		reglas.append("8 ")
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
		reglas.append("9 ")
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
		reglas.append("10 ")
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
		reglas.append("11 ")
		tipo = TSactiva.buscaTipoTS(sig_token["codigo"])
		if tipo == "":
			TSactiva.anadirTipoTS("entlog", sig_token["codigo"], "global")
		sig_token = tokens.pop()
		sprima = estadoSprima()
		if TSactiva.buscaTipoTS(sig_token["codigo"]) in enterologico and sprima in enterologico:
			return "tipo_ok"
		else:
			return "tipo_error"

def estadoD():
	# D -> var id Z ;\n
	global TSactiva, zonaDeclaracion, reglas, ambito
	reglas.append("12 ")
	zonaDeclaracion = True
	scan(tokenV)
	tokenID = {"codigo": sig_token["codigo"], "linea": 0, "colum": 0}
	tuplaI = sig_token["codigo"]
	scan(tokenI)
	z = estadoZ(tokenI)
	scan(tokenPC)
	scan(tokenSL)
	if not (z == "tipo_error"):
		if TSactiva.buscaTipoTS(tokenID["codigo"]) == "":
			TSactiva.anadirTipoTS(z,tokenID["codigo"], ambito)
		else:
			zonaDeclaracion = False
			error(sig_token["codigo"])
			return "tipo_error"
		zonaDeclaracion = False
		return "tipo_ok"
	else:
			error(sig_token["codigo"])
			zonaDeclaracion = False
			return "tipo_error"
			
def estadoZ():
	global tokenTerm,sig_token,reglas
	# Z -> = I
	tokenTerm["codigo"] = "="
	if sig_token["codigo"] == tokenTerm["codigo"]:
		reglas.append("13 ")
		scan(tokenTerm)
		i = estadoI()
		return i
	else:
		reglas.append("14 ")
		return "entero"

def estadoI():
	global sig_token,reglas,tokenTerm
	# I = true
	if sig_token["codigo"] == "true":
		reglas.append("16 ")
		tokenTerm["codigo"] = "true"
		scan(tokenTerm)
		return "logico"
	# I = false
	elif sig_token["codigo"] == "false":
		reglas.append("17 ")
		tokenTerm["codigo"] = "false"
		scan(tokenTerm)
		return logico
	# I = entero
	elif sig_token["codigo"].isdigit():
		reglas.append("15 ")
		scan(sig_token["codigo"])
		return "entero"
	# Se añade este else para contemplar un error???
	else:
		error(sig_token["codigo"])
		return "tipo_error"

def estadoSprima():
	global sig_token,tokenTerm,reglas
	# S' -> =E; \n
	if sig_token["codigo"] == "=":
		reglas.append("18 ")
		tokenTerm["codigo"] = "="
		scan(tokenTerm)
		e = estadoE()
		scan(tokenPC)
		scan(tokenSL)
		return e
	# S' -> +=E; \n
	elif sig_token["codigo"] == "+=":
		reglas.append("19 ")
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
	global sig_token,reglas,TSactiva
	 # S'' -> SS''1
	if sig_token[codigo] in [tokenIF[codigo], tokenDO[codigo], tokenDW[codigo], tokenP[codigo], tokenR[codigo]] or TSactiva.busca_lexema(sig_token["codigo"]):
		reglas.append("20 ")
		s = estadoS()
		s2prima = estadoS2prima()
		if s == "tipo_ok":
			return s2prima
		else:
			return "tipo_error"
	# S'' -> LAMBDA
	else:
		reglas.append("21 ")
		return "tipo_ok"

def estadoR():
	global sig_token,TSactiva,reglas
	# R -> E
	# First(E): (, id, ent
	if sig_token["codigo"] == "(" or sig_token["codigo"].isdigit() or TSactiva.busca_lexema(sig_token["codigo"]): 
		reglas.append("22 ")
		e = estadoE()
		return e
	# R -> LAMBDA
	else:
		reglas.append("23 ")
		return "entlog"

def estadoF():
	global sig_token,zona_funcion,TSactiva,ambito,tokenTerm,reglas
	# F -> function (id)W{S}
	if sig_token["codigo"] == tokenF["codigo"]:
		reglas.append("24 ")
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
	global reglas
	reglas.append("25 ")
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
	global reglas, tokenTerm
	# E' -> +TE'
	if sig_token["codigo"] == "+":
		reglas.append("26 ")
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
		reglas.append("27 ")
		return "entlog"


def estadoT():
	global reglas
	reglas.append("28 ")
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
	global sig_token,tokenTerm,reglas
	# T' -> ==XT'
	if sig_token["codigo"] == "==":
		reglas.append("29 ")
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
		reglas.append("30 ")
		return "entlog"

def estadoX():
	global reglas
	reglas.append("31 ")
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
	global reglas,sig_token,tokenTerm
	# X' -> ||GX'
	if sig_token["codigo"] == "||":
		reglas.append("32 ")
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
		reglas.append("33 ")
		return "entlog"

def estadoG():
	global TSactiva,sig_token,tokenTerm,reglas
	# G -> (E)
	if sig_token["codigo"] == "(":
		reglas.append("34 ")
		tokenTerm["codigo"] = "("
		scan(tokenTerm)
		e = estadoE()
		if sig_token["codigo"] == ")":
			tokenTerm["codigo"] = ")"
			scan(tokenTerm)
			return e
	# G -> idG'
	elif TSactiva.busca_lexema(sig_token["codigo"]):
		reglas.append("35 ")
		tipo = TSactiva.buscaTipoTS(sig_token["codigo"])
		tokenID = {"codigo": sig_token["codigo"], "linea": 0, "colum": 0}
		if tipo == "":
			TSactiva.anadirTipoTS("entero", tokenID["codigo"],"global")
			tipo = TSactiva.buscaTipoTS(sig_token["codigo"])
		scan(sig_token)
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
		reglas.append("36 ")
		scan(sig_token)
		return "entero"
	else:
		return "tipo_error"

def estadoGprima():	
	global sig_token,tokenTerm,reglas
	# G' -> (L)
	if sig_token["codigo"] == "(":
		reglas.append("37 ")
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
		reglas.append("38 ")
		return "entlog"

def estadoL():
	global sig_token,TSactiva,reglas
	#L -> EL'
	if sig_token["codigo"] == "(" or sig_token["codigo"].isdigit() or TSactiva.busca_lexema(sig_token["codigo"]): 
		reglas.append("39 ")
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
		reglas.append("40 ")
		return "tipo_ok"


def estadoLprima():	
	global reglas,sig_token,tokenTerm
	# L' -> ,L
	if sig_token["codigo"] == ",":
		reglas.append("41 ")
		tokenTerm["codigo"] = ","
		scan(tokenTerm)
		l = estadoL()
		return l
	# L' -> LAMBDA
	else:
		reglas.append("42 ")
		return "tipo_ok"

def estadoW():
	global TSactiva,sig_token,ambito,reglas
	#W -> idW'
	if TSactiva.busca_lexema(sig_token["codigo"]):
		reglas.append("43 ")
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
		reglas.append("44 ")
		return "tipo_ok"

def estadoWprima():	
	global reglas,sig_token,tokenTerm
	# W' -> ,W
	if sig_token["codigo"] == ",":
		reglas.append("45 ")
		tokenTerm["codigo"] = ","
		scan(tokenTerm)
		w = estadoW()
		return w
	# W' -> LAMBDA
	else:
		reglas.append("46 ")
		return "tipo_ok"

if __name__ == "__main__":
	main()
