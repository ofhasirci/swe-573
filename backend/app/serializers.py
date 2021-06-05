from django.db.models import fields
from django.db.models.base import Model
from rest_framework import serializers
from app.models import Article 

class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Article
        fields = ['PMID', 'Title', 'Abstract', 'Authors', 'Keywords']