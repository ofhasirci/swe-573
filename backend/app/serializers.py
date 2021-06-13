from django.db.models import fields
from django.db.models.base import Model
from rest_framework import serializers
from app.models import CleanArticle 

class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CleanArticle
        fields = ['PMID', 'Title', 'Abstract', 'Authors', 'Keywords', 'Tokenized', 'TopicClass']