# coding=utf-8
import os
import random
#global
JSON = []

class vertex:
    def __init__(self,v):
        self.id = v
        self.padre = None
        self.hizq = None
        self.hder = None
        self.altura = -1
        self.profundidad = -1
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
        
    def insertarVertice(self,v):
        ver = vertex(v)
        if self.raiz == None:
            self.raiz = ver
        else:
            self.agregar(self.raiz, ver)

    def eliminarVertice(selv,v):
    	pass

    def crearArbol(self,listVer):
        for i in range(len(listVer)):
            self.insertarVertice(listVer[i])

    def generarJSON(self,JSON=[],act = False,):	#recorrido infix
        #global JSON
        if act is False: act = self.raiz
        if act != None:
            self.generarJSON(JSON,act.hder)
            
            if act.padre == None:
                padre = "" #Instead of NONE 
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
                
            #print("Nodo: {:<7} FE: {:<3} Altura: {:<5} Padre: {:<7} hIzq: {:<7} hDer: {}".format(act.id,act.FE,act.altura,padre,hIzq,hDer))
            JSON.append({ 'name': str(act.id),'parent': str(padre)})

            self.generarJSON(JSON,act.hizq)
            return JSON

    def imprimir(self,act = False): #recorrido infix
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
                
            print("Nodo: {:<7} FE: {:<3} Altura: {:<5} Profundidad: {:<5} Padre: {:<7} hIzq: {:<7} hDer: {}".format(act.id,act.FE,act.altura,act.profundidad,padre,hIzq,hDer))

            self.imprimir(act.hder)

    def alturas(self,act = False,prof = 0):	#Recorrido postorden,calcula la altura de las hojas a la raiz, y la profundidad
        if act is False: act = self.raiz
        if act != None:
            act.profundidad = prof;
            a1 = self.alturas(act.hizq,prof+1)
            a2 = self.alturas(act.hder,prof+1)
            #print(max([a1,a2]))
            act.altura = max([a1,a2]) + 1
            return act.altura
        else:
            return -1

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

    def imprimirDesv(self,arrDesv,act = False):
        if act is False: 
        	act = self.raiz
        	self.alturas()
        	self.calcFE()
        if act != None:
            self.imprimirDesv(arrDesv,act.hizq)
            if act.FE > 1:
            	#print(act.id)
            	arrDesv.append([act.id,"der"])
            elif act.FE < -1:
            	#print(act.id)
            	arrDesv.append([act.id,"izq"])
            self.imprimirDesv(arrDesv,act.hder)
        return arrDesv

    def obtenerOBJDesv(self,arrDesv,act = False): #Devuelve los vertices desviados como OBJ
        if len(arrDesv) < 1:
	        if act is False: 
	        	act = self.raiz
	        	self.alturas()
	        	self.calcFE()
	        if act != None:
	            self.obtenerOBJDesv(arrDesv,act.hizq)
	            if len(arrDesv) < 1:
		            if act.FE > 1:
		            	#print(act.id)
		            	arrDesv.append([act,"der"])
		            elif act.FE < -1:
		            	#print(act.id)
		            	arrDesv.append([act,"izq"])
		            self.obtenerOBJDesv(arrDesv,act.hder)
	        return arrDesv


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

    def autobalanceo(self):
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

            #self.imprimir();
            #arrDesv = self.imprimirDesv([])
            #print("Nodos desequilibrados: ", arrDesv)
            arrObjDesv = self.obtenerOBJDesv([])
            
            #if len(arrObjDesv) is not 0: print("Nodos desequilibrados: ", arrObjDesv[0][0].id,arrObjDesv[0][1],"\n")
            #os.system("pause")
            #print("\n\n")
            
        #self.imprimir()

    def buscarVertice(self,v, act = False): #Retorna un arreglo, Encontrado:[1, objAct]; No encontrado:[0]
    	if act is False: 
    		act = self.raiz

    	if act != None:
    		#print("actual", act.id)
	    	if act.id == v:
	    		#print("Vertice: ", act.id, "\t", "Profundidad: ", act.profundidad)
	    		return [1,act]
	    	else:
	    		if act.id < v:
	    			retorno = self.buscarVertice(v, act.hder)
	    		elif act.id > v:
	    			retorno = self.buscarVertice(v,act.hizq)
    	else:
    		#print("Vertice {} no encontrado".format(v))
    		return [0]

    	return retorno



    def obtenerMin(self):
    	act = self.raiz
    	if self.raiz != None:
	    	while act.hizq:
	    		#print(act.id)
	    		act = act.hizq
	    	print("Elemento menor:", act.id)

    def obtenerMax(self):
    	act = self.raiz
    	if self.raiz != None:
	    	while act.hder:
	    		#print(act.id)
	    		act = act.hder
	    	print("Elemento mayor:", act.id)



    def leerArchivo(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        rute = os.path.join(os.path.dirname(BASE_DIR), 'static')
        a = open( rute + '/leerArbol.txt',"r")
        arr = a.readlines()
        a.close()
        #print("Arreglo de prueba: " + arr)
        for line in arr:
            line = line.split(',')
            line = list(map(int, line))

        return line

    def guardarArchivo(self,arr):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        rute = os.path.join(os.path.dirname(BASE_DIR), 'static')
        a = open( rute + '/leerArbol.txt',"w")
        #print("Arreglo " , arr)

        for item in range(len(arr)-1):
            a.write(str(arr[item])+",")
        a.write(str(arr[len(arr)-1]))

        a.close()
        #print("Arreglo de prueba: " + arr)


   
#Ejemplo para leer de archivo     
"""
class main():
    #os.system("cls")
    a = arbol()
    a.crearArbol(a.leerArchivo())
    a.autobalanceo()
    a.imprimir()
"""

#Ejemplo de busqueda de nodo
"""
class main():
    #os.system("cls")
    volatil = [11, 13, 16, 17, 19, 25, 27, 32, 33, 39, 43, 46, 48, 52, 54, 59, 62, 66, 75, 92, 95, 100, 102, 103, 105, 109, 111, 113, 124, 125, 127, 131, 137, 152, 155, 158, 164, 166, 175, 184, 185, 187, 193, 194, 201, 205, 208, 210, 211, 217, 237, 247, 251, 257, 259, 268, 272, 274, 276, 282, 284, 285,293, 297, 298, 301, 308, 317, 319, 328, 329, 337, 338, 339, 340, 354, 358, 374, 387, 388, 390, 399, 404, 413, 414, 420, 422, 430, 434, 437, 446, 448, 456, 468, 473, 480, 482, 483, 486, 493]
    a = arbol()
    a.crearArbol(volatil)
    #a.crearArbol([23, 54, 89, 39, 13, 36, 75, 14, 27,10,9,8,76,77,78,90])
    #a.crearArbol([0,1,2,3,4,5,6,7,8,9])
    #a.crearArbol([10,9,8,7,6,5,4,3,2,1])
    #a.crearArbol([50,10,14])
    
    a.autobalanceo()
    a.imprimir()
    
    x = 2
    while x:
    	x = x-1
    	vertice = int(input("Vertice a buscar: "))
    	resultado = a.buscarVertice(vertice)
    	if resultado[0] == 0:
    		print("Vertice {} no encontrado".format(vertice))
    	else:
            nodo = resultado[1]
            print("Nodo {} encontrado a una profundidad {} ".format(nodo.id,nodo.profundidad))
            


    a.obtenerMax()
    a.obtenerMin()
"""

"""
    for i in range(5):
        #print("\n\n\nINSERTANDO EL NODO ", i)
        #a.insertarVertice(random.randrange(0,1000000))
        a.insertarVertice(i)
        a.autobalanceo()
        #os.system("pause")
    a.imprimir()
    print(vars(a))
    print(JSON)
"""