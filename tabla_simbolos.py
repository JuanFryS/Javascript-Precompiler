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
