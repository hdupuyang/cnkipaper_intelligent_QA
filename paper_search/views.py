from django.shortcuts import render
from django.views import View
# Create your views here.
from .paper_graph.chatbot import chatbot
from django.http import HttpResponse
class demo(View):
    #处理GET请求
    def get(self,request):
        return render(request,'search/search.html')

class neo4jsearch(View):
    def get(self,request):
        search = request.GET.get('search')
        if search==None:
            ans = []
            return HttpResponse(ans)#返回ans字符串数组
        c=chatbot()
        ans=c.chat_main(search)
        return HttpResponse(ans)

