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
	def esPR(lexema):
		global pal_res
		dev = False
		if lexema in pal_res:
			dev = True
		return dev

	# Añadir identificador a la TS devuelve True si se realizo correctamente o False si no se pudo insertar
	# Por ejemplo porque ya hay un id con ese lexema
	def anadirIDTS(lexema, ambito):
		dev = False
		if lexema not in pal_res:
			if busca_lexema(lexema) == False:
				info = Info("", ambito, 0, 0, [])
				self.entradas[lexema] = info
				dev = True
		if ambito == "local":
			info = Info("function", ambito, 0, 0, [])
			self.entradas[lexema] = info
			dev = True
		return dev

	def buscaTipoTS(lexema):
		if busca_lexema(lexema) == True:
			tipo = lexema["tipo"]
			if tipo in tipos:
				return tipo
			else:
				return ""

	def anadirTipoTS(tipo, lexema, ambito):
		# global desplazamiento_ts_global, desplazamiento_ts_local, desplazamiento, tipo
		dev = False
		if busca_lexema(lexema) == True:
			if tipo in tipos:
				if lexema not in pal_res:
					self.entradas[lexema].tipo = tipo
					if ambito == "global":
						self.entradas[lexema].desplazamiento = desplazamiento_ts_global
						desplazamiento_ts_global = desplazamiento_ts_global + desplazamiento[tipo]
						dev = True
					else:
						self.entradas[lexema].desplazamiento = desplazamiento_ts_local
						desplazamiento_ts_local = desplazamiento_ts_local + desplazamiento[tipo]
						dev = True
		return dev

	# Añadir argumentos recibe el id de la funcion y una lista con los tipos de los argumentos
	def anadirTipoArgs(lexema, args):
		dev = False
		info = entradas.get(lexema, False)
		if info:
			info.num_par = len(args)
			for tipo in args:
				info.tipo_par.append(tipo)
			dev = True
		return dev

	# Son tipos iguales dice si los argumentos de una funcion son los que se declararon
	def sonTiposIguales(args1, args2):
		dev = True
		for tipo1,tipo2 in zip(args1,args2):
			if tipo1 not in tipos or tipo2 not in tipos:
				dev = False

		return dev

	# Vaciar tabla reinicia la tabla, borra todo el contenido
	def vaciar():
		entradas.clear()

	# Cambia ámbito convierte el desplazamiento local en 0
	def cambiarAmbito():
		self.desplazamiento_ts_local = 0

	def imprimirTS(fichero, nombre):
		if nombre == "global":
			fichero.write("############# Tabla General ############\n")
		else:
			fichero.write("############# Tabla Local ##############")
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
				fichero.write("lexema: {0}, tipo: {1}, desplazamiento: {3}, ambito: {4}\n".format(clave, 
					valor.tipo, str(valor.desplazamiento), valor.ambito))

		fichero.write("############################################\n\n")