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
	#tokenA = {"codigo": "(", "linea": 0, "colum": 0}
	#tokenC = {"codigo": ")", "linea": 0, "colum": 0}
	#tokenI = {"codigo": sig_token["codigo"], "linea": 0, "colum": 0}
 	#tuplaI = sig_token["codigo"]
tokenE = {"codigo": "=", "linea": 0, "colum": 0}
tokenMI = {"codigo": "+=", "linea": 0, "colum": 0}
tokenIF = {"codigo": "if", "linea": 0, "colum": 0}
tokenDO = {"codigo": "do", "linea": 0, "colum": 0}
tokenW = {"codigo": "while", "linea": 0, "colum": 0}
	#tokenAc = {"codigo": "{", "linea": 0, "colum": 0}	
	#tokenCc = {"codigo": "}", "linea": 0, "colum": 0}
tokenSL = {"codigo": "SL", "linea": 0, "colum": 0}
tokenPC = {"codigo": ";", "linea": 0, "colum": 0}
tokenDW = {"codigo": "document.write", "linea": 0, "colum": 0}
tokenP = {"codigo": "prompt", "linea": 0, "colum": 0}
tokenF = {"codigo" : "function", "linea" : 0, "colum": 0}

def scan(token):


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
	if sig_token[codigo] == firstF[codigo]:
		f = estadoF()
		pp = estadoPprima()
		if f == "tipo_ok":
			return pp
		else:
			return "tipo_error"

	# Caso P' -> SP'1
	# First de regla: P' -> SP' : id, do, document.write, prompt, return, id
	elif sig_token[codigo] in [firstIF[codigo], firstDO[codigo], firstDW[codigo], firstP[codigo], firstR[codigo]] or TSactiva.busca_lexema(sig_token["codigo"]):
		s = estadoS()
		pp = estadoPprima()
		if s == "tipo_ok":
			return pp
		else:
			return "tipo_error"

	# Caso P' -> DP'1
	# First de regla: P' -> DP' : var
	elif sig_token[codigo] == firstV[codigo]:
		d = estadoD()
		pp = estadoPprima()
		return pp

	# Caso P' -> Lambda	
	else:
		return "tipo_ok"

def estadoS():
	if sig_token["codigo"] == tokenIF["codigo"]:
		sig_token = tokens.pop()
		if sig_token["codigo"] == "(":
			sig_token = tokens.pop()
			e = estadoE()
			if sig_token["codigo"] == ")":
				sig_token = tokens.pop()
				s = estadoS()
			else:
				error(sig_token)
		else:
			error(sig_token)
		if e == "logico":
			return s
		else:
			return "tipo_error"
	elif sig_token["codigo"] == tokenDO["codigo"]:
		sig_token = tokens.pop()
		if sig_token["codigo"] == "{":
			sig_token = tokens.pop()
			if sig_token["codigo"] == tokenSL["codigo"]:
				sig_token = tokens.pop()
				s = estadoS()
				s1 = estadoSuno()
				if sig_token["codigo"] == tokenSL["codigo"]:
					sig_token == tokens.pop()
					if sig_token["codigo"] == "}":
						sig_token == tokens.pop()
						if sig_token["codigo"] == tokenW["codigo"]:
							sig_token == tokens.pop()
							if sig_token["codigo"] == "(":
								sig_token == tokens.pop()
								e = estadoE()
								if sig_token["codigo"] == ")":
									sig_token == tokens.pop()
									if sig_token["codigo"] == tokenSL["codigo"]:
										if ((e = logico) and (s1 = "tipo_ok")
											return "tipo_ok"
										else:
											return "tipo_error"
									else:
										error(sig_token)
								else:
									error(sig_token)
							else:
								error(sig_token)
						else:
							error(sig_token)
					else:
						error(sig_token)
				else:
					error(sig_token)
			else:
				error(sig_token)
		else:
			error(sig_token)
	elif sig_token["codigo"] == tokenDW["codigo"]:
		sig_token = tokens.pop()
		if sig_token["codigo"] == "(":
			sig_token == tokens.pop()
			e = estadoE()
			if sig_token["codigo"] == ")":
				sig_token = tokens.pop()
				if sig_token["codigo"] == tokenPC["codigo"]:
					sig_token = tokens.pop()
					if sig_token["codigo"] == tokenSL["codigo"]):
						sig_token = tokens.pop()
						if e != "tipo_error":
							return "tipo_ok"
						else:
							return "tipo_error"
					else:
						error(sig_token)
				else:
					error(sig_token)
			else:
				error(sig_token)
		else:
			error(sig_token)
	
	elif....... :


def estadoD():


def estadoZ():


def estadoI():


def estadoSuno():


def estadoR():


def estadoF():


def estadoE():


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
