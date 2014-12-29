"""
	En este archivo se encuentra el código correspondiente a
	la tabla de símbolos, y la gestión de la misma mediante
	los diferentes métodos declarados.
"""

class Info(object):
	tipo = ""
	ambito = ""
	desplazamiento = 0
	num_par = 0
	tipo_par = []

	# Constructor
	def __init__(self, tipo, ambito, desplazamiento, num_par, tipo_par):
		self.tipo = tipo
		self.ambito = ambito
		self.desplazamiento = desplazamiento
		self.num_par = num_par
		self.tipo_par = tipo_par

class Tabla:
	entradas = {}
	pal_res = ["var", "function", "return", "if", "do", "while", "true", "false", "prompt", "document.write"]
	desplazamiento_ts_global = 0
	desplazamiento_ts_local = 0
	desplazamiento = {"entero": 2, "logico": 1, "entlog": 2}
	tipos = ["entero", "logico", "entlog"]

	# Constructor
	def __init__(self, general):
		# general es un booleano que, siendo cierto, crea una tabla global
		# Si es falso, crea una tabla local 

		self.entradas = {}
		if general:
			for palabra in pal_res:
				info = Info("reservada", "global", 0, 0, [])
				self.entradas[palabra] = info

	# Buscar en TS devuelve un booleano 
	def busca_lexema(lexema):
		dev = False
		if lexema in entradas.keys():
			dev = True
		return dev

	# Comprobar si un lexema es palabra reservada devuelve también un booleano
	def es_PR(lexema):
		dev = False
		if lexema in pal_res:
			dev = True
		return dev

	# Añadir identificador a la TS devuelve True si se realizo correctamente o False si no se pudo insertar
	# Por ejemplo porque ya hay un id con ese lexema
	def anadirIDTS(lexema):
		dev = false;
		if lexema not in pal_res:
			if busca_lexema == false:
				info = Info("identificador", ambito, 0, 0, [])
				self.entradas[lexema] = info
				dev = true
		elif lexema == function:
			info = Info("function", ambito, 0,0,[])
			self.entradas[lexema] = info
			dev true
		return dev

	def anadirTipoTS(tipo, lexema, ambito):
		global desplazamiento_ts_global, desplazamiento_ts_local, desplazamiento, tipo
		if busca_lexema(lexema) == true:
			if tipo in tipos:
				if lexema not in pal_res:
					self.entradas[lexema].tipo = tipo
					self.entradas[lexema].ambito = ambito
					if ambito = "global":
						self.entradas[lexema].desplazamiento = desplazamiento_ts_global
						desplazamiento_ts_global = desplazamiento_ts_global + desplazamiento[tipo]
						return true
					else:
						self.entradas[lexema].desplazamiento = desplazamiento_ts_local
						desplazamiento_ts_local = desplazamiento_ts_local + desplazamiento[tipo]
						return true
				elif lexema == "function":
					self.entradas[lexema].tipo = tipo
					self.entradas[lexema].ambito = ambito
					return true
		return false