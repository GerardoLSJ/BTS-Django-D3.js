import os
import random

class vertex:
	def __init__(self,v):
		self.id = v
		self.padre = None
		self.hizq = None
		self.hder = None
		self.altura = -1
		self.FE = 0

class arbol:
	def __init__(self):
		self.raiz = None

	def agregar(self,act, ver):
		if ver.id > act.id:			#Vertice mayor que actual
			if act.hder != None:	#Si hay hDer aplicar recursividad
				self.agregar(act.hder,ver)
			else:					#Si no hay hDer se inserta como su hIzq
				act.hder = ver
				ver.padre = act
		else:						#Vertice menor que actual
			if act.hizq != None:	#Si hay hIzq aplicar recursividad
				self.agregar(act.hizq,ver)
			else:					#Si no hay hIzq se inserta como su hIzq
				act.hizq = ver
				ver.padre = act
		
	def agregarVertice(self,v):
		ver = vertex(v)
		if self.raiz == None:
			self.raiz = ver
		else:
			self.agregar(self.raiz, ver)

	def crearArbol(self,listVer):
		for i in range(len(listVer)):
			self.agregarVertice(listVer[i])

	def imprimir(self,act = False):	#recorrido infix
		if act is False: act = self.raiz
		if act != None:
			self.imprimir(act.hizq)
			if act.padre == None:
				padre = "None"
			else:
				padre = act.padre.id
			if act.hizq == None:
				hIzq = "None"
			else:
				hIzq = act.hizq.id
			if act.hder == None:
				hDer = "None"
			else:
				hDer = act.hder.id
			print("Nodo: {:<7} FE: {:<3} Altura: {:<5} Padre: {:<7} hIzq: {:<7} hDer: {}".format(act.id,act.FE,act.altura,padre,hIzq,hDer))
			self.imprimir(act.hder)

	def altura(self,act = False):	#Recorrido postorden,calcula la altura de las hojas a la raiz
		if act is False: act = self.raiz
		if act != None:
			a1 = self.altura(act.hizq)
			a2 = self.altura(act.hder)
			#print(max([a1,a2]))
			act.altura = max([a1,a2]) + 1
			return act.altura
		else:
			return -1

	def imprimirDesv(self,arrDesv,act = False):
		if act is False: act = self.raiz
		if act != None:
			self.imprimirDesv(arrDesv,act.hizq)
			if act.hizq != None and act.hder != None:
				#print(act.id)
				diferencia = act.hder.altura - act.hizq.altura
				if  diferencia < -1:
					arrDesv.append([act.id,"izq"])
				elif diferencia > 1:
					arrDesv.append([act.id,"der"])
			elif (act.hizq == None and act.hder != None) and act.hder.altura > 0:
				#print(act.id)
				arrDesv.append([act.id,"der"])
			elif (act.hizq != None and act.hder == None) and act.hizq.altura > 0:
				#print(act.id)
				arrDesv.append([act.id,"izq"])
			self.imprimirDesv(arrDesv,act.hder)
		return arrDesv

	def obtenerOBJDesv(self,arrDesv,act = False): #Devuelve los vertices desviados como OBJ
		if act is False: act = self.raiz
		if act != None:
			self.obtenerOBJDesv(arrDesv,act.hizq)
			if act.hizq != None and act.hder != None:
				#print(act.id)
				diferencia = act.hder.altura - act.hizq.altura
				if  diferencia < -1:
					arrDesv.append([act,"izq"])
				elif diferencia > 1:
					arrDesv.append([act,"der"])
			elif (act.hizq == None and act.hder != None) and act.hder.altura > 0:
				#print(act.id)
				arrDesv.append([act,"der"])
			elif (act.hizq != None and act.hder == None) and act.hizq.altura > 0:
				#print(act.id)
				arrDesv.append([act,"izq"])
			self.obtenerOBJDesv(arrDesv,act.hder)
		return arrDesv

	def calcFE(self,act = False): #Factor de equilibrio
		if act is False: act = self.raiz
		if act != None:
			self.calcFE(act.hizq)
			if act.hizq != None and act.hder != None:
				act.FE = act.hder.altura - act.hizq.altura
			elif (act.hizq == None and act.hder != None):
				act.FE = act.hder.altura + 1
			elif (act.hizq != None and act.hder == None):
				act.FE = -act.hizq.altura  - 1
			else:
				act.FE = 0
			self.calcFE(act.hder)
			
	def RR(self,n,act = False):	#Rotacion a la derecha (n = int)
		if act is False: act = self.raiz
		#print("act: ", act.id)
		if (act.hizq != None) and act.id == n :
			#Saber si actual es hIzq o IDer de su padre
			if act.padre != None:
				if act.padre.hizq == act:
					ladoRef = "izq"
				else:
					ladoRef = "der"

			nr = act.hizq	#nr = Nodo Referencia
			act.hizq = nr.hder
			nr.hder = act
			nr.padre = act.padre
			act.padre = nr 
			if act.hizq != None:
				act.hizq.padre = act

			if nr.padre != None:
				if ladoRef == "izq":
					nr.padre.hizq = nr
				elif ladoRef == "der":
					nr.padre.hder = nr

			if self.raiz == act:
				self.raiz = nr
		else:
			if act.hizq != None and act.hder != None:
				self.RR(n,act.hizq)
				self.RR(n,act.hder)
			elif act.hizq != None and act.hder == None:
				self.RR(n,act.hizq)
			elif act.hizq == None and act.hder != None:
				self.RR(n,act.hder)
	
	def LR(self,n,act = False):	#Rotacion a la izquierda
		if act is False: act = self.raiz
		#print("act: ", act.id)
		if (act.hder != None) and act.id == n :
			#Saber si actual es hIzq o IDer de su padre
			if act.padre != None:
				if act.padre.hizq == act:
					ladoRef = "izq"
				else:
					ladoRef = "der"

			nr = act.hder	#nr = Nodo Referencia
			act.hder = nr.hizq
			nr.hizq = act
			nr.padre = act.padre
			act.padre = nr 
			if act.hder != None:
				act.hder.padre = act

			if nr.padre != None:
				if ladoRef == "izq":
					nr.padre.hizq = nr
				elif ladoRef == "der":
					nr.padre.hder = nr

			if self.raiz == act:
				self.raiz = nr
		else:
			if act.hizq != None and act.hder != None:
				self.LR(n,act.hizq)
				self.LR(n,act.hder)
			elif act.hizq != None and act.hder == None:
				self.LR(n,act.hizq)
			elif act.hizq == None and act.hder != None:
				self.LR(n,act.hder)

	def RDR(self,o): #Rotación doble a la derecha (o = obj)
		self.LR(o.hizq.id)
		self.RR(o.id)

	def LDR(self,o): #Rotación doble a la izquierda (o = obj)
		self.RR(o.hder.id)
		self.LR(o.id)

	def autobalanceado(self):
		self.altura()
		self.calcFE()
		#self.imprimir()
		#arrDesv = self.imprimirDesv([])  #Solo para verificar arreglo de desvalanceados
		#print("Nodos desequilibrados: ", arrDesv)
		arrObjDesv = self.obtenerOBJDesv([])
		#if len(arrObjDesv) is not 0: print("Nodo desequilibrado: ", arrObjDesv[0][0].id,arrObjDesv[0][1])#,arrObjDesv[0][0])
		#print("")

		while(len(arrObjDesv)>0):
			ladoDesv = arrObjDesv[0][1]
			objDesv = arrObjDesv[0][0]
			
			#if objDesv.hizq is not None: print("PRUEBA:", objDesv.hder, objDesv.hizq.altura,objDesv.hizq.FE,  objDesv.hizq.id)
			#if objDesv.hder is not None: print("PRUEBA:", objDesv.hder, objDesv.hder.altura,objDesv.hder.FE,  objDesv.hder.id)
			
			#print("EQUILIBRANDO NODO ", objDesv.id)
			if objDesv.hder == None and objDesv.hizq != None and objDesv.hizq.altura >= 1 and objDesv.hizq.FE == 1:
				#print("ENTRANDO A RDR-A")
				self.RDR(objDesv)
				#print("SALIENDO DE RDR-A")
			elif objDesv.hder != None and objDesv.hizq != None and (objDesv.hizq.altura-objDesv.hder.altura>=2) and objDesv.hizq.FE == 1:
				#print("ENTRANDO A RDR-B")
				self.RDR(objDesv)
				#print("SALIENDO DE LDR-B")

			elif objDesv.hizq == None and objDesv.hder != None and objDesv.hder.altura >= 1  and objDesv.hder.FE == -1:
				#print("ENTRANDO A LDR-A")
				self.LDR(objDesv)
				#print("SALIENDO DE LDR-A")
			elif objDesv.hizq != None and objDesv.hder != None and (objDesv.hder.altura-objDesv.hizq.altura >=2) and objDesv.hizq.FE == -1:
				#print("ENTRANDO A LDR-B")
				self.LDR(objDesv)
				#print("SALIENDO DE LDR-B")

			elif ladoDesv == "izq":
				#print("ENTRANDO A RR")
				self.RR(objDesv.id)
				#print("SALIENDO DE RR")
			elif ladoDesv == "der":
				#print("ENTRANDO A LR")
				self.LR(objDesv.id)
				#print("SALIENDO DE LR")
			else:
				#print("NO SE ENTRO A NINGUNA OPCION")
				pass
				

			self.altura()
			self.calcFE()
			#self.imprimir();
			#arrDesv = self.imprimirDesv([])
			#print("Nodos desequilibrados: ", arrDesv)
			arrObjDesv = self.obtenerOBJDesv([])
			
			#if len(arrObjDesv) is not 0: print("Nodos desequilibrados: ", arrObjDesv[0][0].id,arrObjDesv[0][1],"\n")
			#os.system("pause")
			#print("\n\n")
			
		#self.imprimir()

	

class main():
	os.system("cls")
	a = arbol()
	#a.crearArbol([23, 54, 89, 39, 13, 36, 75, 14, 27,10,9,8,76,77,78,90])
	#a.crearArbol([1,2,3,4,5,6,7,8,9,10])
	#a.crearArbol([10,9,8,7,6,5,4,3,2,1])
	#a.crearArbol([50,10,14])
	#a.autobalanceado()


	for i in range(4000):
		print("\n\n\nINSERTANDO EL NODO ", i)
		#a.agregarVertice(random.randrange(0,1000000))
		a.agregarVertice(i)
		a.autobalanceado()
		#os.system("pause")
	a.imprimir()
