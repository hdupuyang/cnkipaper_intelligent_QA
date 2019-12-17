from django.shortcuts import render
from django.views import View
# Create your views here.
from .paper_graph.chatbot import chatbot

class demo(View):
    #处理GET请求
    def get(self,request):
        search=request.GET.get('search')
        if search==None:
            ans = []
            context = {'ans': ans}
            return render(request,'search/search.html',context)
        c=chatbot()
        ans=c.chat_main(search)
        context={'ans':ans}

        return render(request,'search/search.html',context)