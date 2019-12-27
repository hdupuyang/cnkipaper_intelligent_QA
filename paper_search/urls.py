# 引入path
from django.urls import path
from . import views
# 正在部署的应用的名称
app_name = 'article'

urlpatterns = [
    path('',views.demo.as_view(),name='demo'),
    path('s/',views.neo4jsearch.as_view(),name='neo4jsearch')
]