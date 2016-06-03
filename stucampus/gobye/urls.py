from django.conf.urls import url, patterns

from stucampus.gobye.views import index,result

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^result/$', result, name='result')
]
