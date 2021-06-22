from django.shortcuts import render
from django.http import HttpResponse, response
from app.getArticles import getArticle
from app.analysis import tokenize, analyze
from app.wikiData import WikiData
from app.models import CleanArticle
from app.serializers import ArticleSerializer
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
        terms = data['terms']
        offset = data['offset']
        count = data['count']
        offset = offset * count
        count = offset + count
        print(terms)
        sentence = " "
        for id in terms:
            wiki = WikiData(id)
            sentence = sentence + " " + wiki.getSentence()
        class_number = analyze(sentence)
        articles = CleanArticle.objects.filter(TopicClass=class_number).order_by('-ClassValue').values('PMID', 'Title', 'Abstract', 'Authors', 'Keywords', 'Tags')
        serializer = ArticleSerializer(articles, many=True)
        resp = {
            'articles': serializer.data[offset:count],
            'ldaUrl': "http://localhost:8080/static/lda_model.html",
            'numOfArticle': len(serializer.data),
            'classNumber': class_number
        }

        return Response(resp, status=status.HTTP_200_OK)


@api_view(['POST'])
def pagination(request):
    print("paginition request")
    if request.method == 'POST':
        data = JSONParser().parse(request)
        class_number = data['class_no']
        offset = data['offset']
        count = data['count']
        offset = offset * count
        count = offset + count
        articles = CleanArticle.objects.filter(TopicClass=class_number).order_by('-ClassValue').values('PMID', 'Title', 'Abstract', 'Authors', 'Keywords', 'Tags')[offset:count]
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def saveTags(request):
    print("save tags request")
    if request.method == 'POST':
        data = JSONParser().parse(request)
        pmid = data['pmid']
        tags = data['tags']
        article = CleanArticle.objects.get(pk=pmid)
        articleTags = article.Tags
        print(articleTags)
        if articleTags:
            tags = articleTags + tags
        print(tags)
        update_serializer = ArticleSerializer(article, data={'Tags':tags}, partial=True)
        if update_serializer.is_valid():
            update_serializer.save()
            print("updated")
        return Response(tags, status=status.HTTP_200_OK)

