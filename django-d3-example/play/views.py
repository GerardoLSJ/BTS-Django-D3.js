#from django.db import connections
#from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render

from .models import Play


#from django.shortcuts import render
from django.http import HttpResponse

from .forms import NameForm

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        print('METHOD POST')
        print(request)
        data = {'name': 'gerry'}
        #HttpResponse("Here's the text of the Web page.")
        #return HttpResponse(data, content_type='application/json')
        return JsonResponse( (data) , safe=False)
    else:
        return render(request, 'graph/graph.html')



def graph(request):
    return render(request, 'graph/graph.html')


def data(request, data={'void':'void'}):
    dic = {}
    if request:
        print(data)
        dic = data
    else:
        dic = {}

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
    #nodes = [dict1,dict1,dict1,dict1,dict1]

    '''
    data = Play.objects.all() \
        .extra(
            select={
                'month': connections[Play.objects.db].ops.date_trunc_sql('month', 'date')
            }
        ) \
        .values('month') \
        .annotate(count_items=Count('id'))
    '''
    return  HttpResponse(dic)#JsonResponse((dic), safe=False)
