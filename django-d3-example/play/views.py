from django.http import JsonResponse
from django.shortcuts import render

from .models import Play
from django.http import HttpResponse
#from .forms import NameForm
from django.views.decorators.csrf import csrf_exempt

from .BSTAuto import *

JSONlocal = [] #global
a = arbol()
#a.crearArbol([13, 36, 75, 14, 27,10,9,8,76,77,78,90,1,2,3,4,5,6]) #13, 36, 75, 14, 27,10,9,8,76,77,78,90,1,2,3,4,5,6 [50,20,70,15,25,60,80,10,5,3,2,1,17]
volatil = [23, 54, 89, 39, 13, 36, 75, 14, 27,10,9,8,76,77,78,90]
#volatil = [11, 13, 16, 17, 19, 25, 27, 32, 33, 39, 43, 46, 48, 52, 54, 59, 62, 66, 75, 92, 95, 100, 102, 103, 105, 109, 111, 113, 124, 125, 127, 131, 137, 152, 155, 158, 164, 166, 175, 184, 185, 187, 193, 194, 201, 205, 208, 210, 211, 217, 237, 247, 251, 257, 259, 268, 272, 274, 276, 282, 284, 285,293, 297, 298, 301, 308, 317, 319, 328, 329, 337, 338, 339, 340, 354, 358, 374, 387, 388, 390, 399, 404, 413, 414, 420, 422, 430, 434, 437, 446, 448, 456, 468, 473, 480, 482, 483, 486, 493]
a.crearArbol(volatil)
a.autobalanceo()
JSONlocal = a.generarJSON()
print('EJECUTANDO DESDE ARRIBA______')
#This populates a global VAR named JSON.

@csrf_exempt
def get_name(request):
    # if this is a POST request we need to process the form data
    sanitized = []
    if request.method == 'POST':
        print('METHOD POST')
        arr = request.POST.getlist('arr[]')
        #arr = list(map(arr,lambda x: x.replace('u','')))
        
        for item in arr:
            print (item)
            sanitized.append(int(item))

        a = arbol()
        a.crearArbol(sanitized)
        a.autobalanceo()
        JSONlocal = []
        JSONlocal = a.generarJSON([]) #actualizamos el JSON
        print('JSON locals')
        print(JSONlocal)
        data('fakeRequest') #actualizamos nuestro RESTful API 
        return JsonResponse( ([JSONlocal, sanitized]) , safe=False)
    else:
        return JsonResponse( (sanitized) , safe=False)



def graph(request):
    return render(request, 'graph/graph.html')



def data(request, data={'void':'void'}):
    print('en dataaaaa')
    '''
    dic = {}
    if request:
        print(data)
        dic = data
    else:
        dic = {}

    dic = {"nodes": [],"links": []}
    
    for item in JSON:
        element = {'id':item['id'],'group':item['altura'] }
        dic['nodes'].append(element)

        if(item['hDer'] != 'None'): #Strin not None #FIX LATER WITH NILL
            link = {'source': item['id'] , 'target':item['hDer']}
            dic['links'].append(link)

        if(item['hIzq'] != 'None'):
            link = {'source': item['id'] , 'target':item['hIzq']}
            dic['links'].append(link)
            
    print(dic)
    request
    '''


    return JsonResponse([JSONlocal,volatil], safe=False)


'''    
    dic = {
    "nodes": [
        {"id": "1", "group": 1},
        {"id": "2", "group": 2},
        {"id": "3", "group": 2},
        {"id": "4", "group": 3},
        {"id": "5", "group": 3},
        {"id": "6", "group": 3},
        {"id": "7", "group": 3},
        {"id": "8", "group": 4}

    ],
    "links": [
        {"source": "1", "target": "2", "value": 1},
        {"source": "1", "target": "3", "value": 8},
        {"source": "2", "target": "4", "value": 1},
        {"source": "2", "target": "5", "value": 1},
        {"source": "3", "target": "6", "value": 3},
        {"source": "3", "target": "7", "value": 8},

    ]
    }
'''