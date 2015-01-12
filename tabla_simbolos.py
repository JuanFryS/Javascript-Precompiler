# -*- coding: UTF-8 -*-
#
#	En este archivo se encuentra el código correspondiente a
#	la tabla de símbolos, y la gestión de la misma mediante
#	los diferentes métodos declarados.
#

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
	global pal_res
	global entradas
	global tipos
	global desplazamiento
	global desplazamiento_ts_global
	global desplazamiento_ts_local
	
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
	@staticmethod 
	def busca_lexema(lexema):
		global entradas
		dev = False
		if lexema in entradas.keys():
			dev = True
		return dev

	# Comprobar si un lexema es palabra reservada devuelve también un booleano
	@staticmethod 
	def esPR(lexema):
		global pal_res
		dev = False
		if lexema in pal_res:
			dev = True
		return dev

	# Añadir identificador a la TS devuelve True si se realizo correctamente o False si no se pudo insertar
	# Por ejemplo porque ya hay un id con ese lexema
	@staticmethod 
	def anadirIDTS(lexema, ambito):
		global pal_res, entradas
		dev = False
		if lexema not in pal_res:
			if not lexema in entradas.keys():
				info = Info("", ambito, 0, 0, [])
				entradas[lexema] = info
				dev = True
		if ambito == "local":
			info = Info("function", ambito, 0, 0, [])
			entradas[lexema] = info
			dev = True
		return dev

	@staticmethod 
	def buscaTipoTS(lexema):
		global entradas, tipos
		if lexema in entradas.keys():
			tipo = entradas[lexema].tipo
			if tipo in tipos:
				return tipo
			else:
				return ""

	@staticmethod 
	def anadirTipoTS(tipo, lexema, ambito):
		global entradas, pal_res, desplazamiento_ts_global, desplazamiento_ts_local, desplazamiento, desplazamiento_ts_global
		dev = False
		if lexema in entradas.keys():
			if tipo in tipos:
				if lexema not in pal_res:
					entradas[lexema].tipo = tipo
					if ambito == "global":
						entradas[lexema].desplazamiento = desplazamiento_ts_global
						desplazamiento_ts_global = desplazamiento_ts_global + desplazamiento[tipo]
						dev = True
					else:
						entradas[lexema].desplazamiento = desplazamiento_ts_local
						desplazamiento_ts_local = desplazamiento_ts_local + desplazamiento[tipo]
						dev = True
		return dev

	# Añadir argumentos recibe el id de la funcion y una lista con los tipos de los argumentos
	@staticmethod 
	def anadirTipoArgs(lexema, args):
		global entradas
		dev = False
		info = entradas.get(lexema, False)
		if info:
			info.num_par = len(args)
			for tipo in args:
				info.tipo_par.append(tipo)
			dev = True
		return dev

	# Son tipos iguales dice si los argumentos de una funcion son los que se declararon
	@staticmethod 
	def sonTiposIguales(args1, args2):
		global tipos
		dev = True
		for tipo1,tipo2 in zip(args1,args2):
			if tipo1 not in tipos or tipo2 not in tipos:
				dev = False

		return dev

	# Vaciar tabla reinicia la tabla, borra todo el contenido
	@staticmethod 
	def vaciar():
		global entradas
		entradas.clear()

	# Cambia ámbito convierte el desplazamiento local en 0
	@staticmethod 
	def cambiarAmbito():
		global desplazamiento_ts_local
		self.desplazamiento_ts_local = 0

	@staticmethod 
	def imprimirTS(fichero, nombre):
		global entradas
		if nombre == "global":
			fichero.write("\n############# Tabla General ############\n")
		else:
			fichero.write("\n############# Tabla Local ##############")
			fichero.write(nombre)
			fichero.write("\n")
		for clave, valor in entradas.iteritems():
			if valor.tipo  == "reservada":
				fichero.write("%s\n", clave)
			elif valor.tipo == "proc":
				fichero.write("lexema: {0}, tipo: {1}, num_par: {2}, ".format(clave, valor.tipo, str(valor.num_par)))
				fichero.write("tipo_par: [ ")
				for tipo in valor.tipo_par:
					fichero.write("{0} ".format(tipo))
				fichero.write("], ")
				fichero.write("ambito: {0}\n".format(valor.ambito))
			elif valor.tipo == "entero" or valor.tipo == "entlog" or valor.tipo == "logico":
				fichero.write("lexema: {0}, tipo: {1}, desplazamiento: {2}, ambito: {3}\n".format(clave, 
					valor.tipo, str(valor.desplazamiento), valor.ambito))

		fichero.write("########################################\n\n")