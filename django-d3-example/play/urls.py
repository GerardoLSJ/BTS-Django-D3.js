from django.conf.urls import url


from .views import graph, data, get_name

urlpatterns = [
    url(r'^$', graph),
    url(r'^api/data', data, name='data'),
    url(r'^send/$',get_name ),
]
