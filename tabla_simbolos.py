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
	espacios = {"entero": 2, "logico": 1, "entlog": 2}

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