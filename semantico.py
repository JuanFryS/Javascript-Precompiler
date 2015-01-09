# Juan Francisco Salamanca Carmona #

"""
	En este archivo se encuentra el código correspondiente al
	Analizador Semantico Descendente Recursivo
"""

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
	print("ERROR: En la línea "+token["linea"]+", columna "+token["colum"])+", se recibe el valor no esperado: "+token["codigo"])
	fich_err.write("ERROR: En la línea "+token["linea"]+", columna "+token["colum"])+", se recibe el valor no esperado: "+token["codigo"]+"\n")

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
	if sig_token[codigo] == tokenF[codigo]:
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
		if e = "logico" and s1 = "tipo_ok":
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

def estadoD():
	Declaracion = True
	scan(tokenV)
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
	# Se añade este else para contemplar un error???=
	else:
		error(sig_token["codigo"])
		return "tipo_error"

def estadoSprima():
	# S' -> =E; \n
	if sig_token["codigo"] == "="
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
	if sig_token["codigo"] == tokenF["codigo"]:
		scan(tokenF)
		zona_funcion = True
		tokenID = {"codigo": sig_token["codigo"], "linea": 0, "colum": 0}
		if TSactiva.busca_lexema(tokenID["codigo"]):
			scan(tokenID)
			TSactiva.anadirTipoTS("funcion", tokenID["codigo"],global)
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
	t = estadoT()
	eprima = estadoEprima()
	if t in enterologico and eprima == "entlog":
		return t
	elif t == eprima and t in enterologico:

def estadoEprima():


def estadoT():


def estadoTprima():


def estadoX():


def estadoXprima():


def estadoG():


def estadoGprima():	


def estadoL():


def estadoLprima():	


def estadoW():


def estadoWprima():	



if __name__ == "__main__":
	main()
