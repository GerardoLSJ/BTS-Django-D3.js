from django.conf.urls import url


from .views import graph, data

urlpatterns = [
    url(r'^$', graph),
    url(r'^api/data', data, name='data'),
]
