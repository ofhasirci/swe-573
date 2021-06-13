from django.shortcuts import render
from django.http import HttpResponse
from app.getArticles import getArticle
from app.analysis import tokenize, analyze
from app.models import CleanArticle
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.conf import settings
import os

LDA_HTML_PATH = os.path.join(settings.BASE_DIR, "\\app\\lda_model\\lda.html")

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
            analyze()
            print("analyze")
            html = '<h1>analyze</h1>'

    return HttpResponse(html)

@api_view(['POST'])
def search(request):
    print("post request")
    if request.method == 'POST':
        data = JSONParser().parse(request)
        term = data['term']
        print("term: " + term)
    
    return Response(data, status=status.HTTP_200_OK)