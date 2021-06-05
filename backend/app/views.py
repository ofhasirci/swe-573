from django.shortcuts import render
from django.http import HttpResponse
from app.getArticles import getArticle
from background_task.models import Task
import datetime

# Create your views here.
def homePageView(request):
    return HttpResponse('<h1>Hello World!</h1>')

def collectionManager(request):
    html = '<h1>Not Get</h1>'
    if request.method == 'GET':
        start = request.GET.get('start')
        print('start ' + start)
        if start and start == '1':
            getArticle(term='amygdala')
            print("Start Collecting")
            html = '<h1>Started</h1>'
        if start and start == '0':
            print("Stop Collecting")
            html = '<h1>Stopped</h1>'

    return HttpResponse(html)
