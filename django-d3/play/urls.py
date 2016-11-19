from django.conf.urls import url


from .views import graph, data, get_tree, readFrom, saveTo, MaxMin,mySearch

urlpatterns = [
    url(r'^$', graph),
    url(r'^api/data', data, name='data'),
    url(r'^send/$',get_tree ),
    url(r'^api/read',readFrom),
    url(r'^api/save',saveTo),
    url(r'^api/MaxMin',MaxMin),
    url(r'^api/search',mySearch),

    
]
