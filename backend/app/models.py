from django.db import models
from django.db.models.base import Model
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Article(models.Model):
    PMID = models.CharField(primary_key=True, max_length=16)
    Title = models.TextField(max_length=512)
    Abstract = models.TextField(max_length=5000, null=True)
    Authors = ArrayField(models.CharField(max_length=40, blank=True))
    Keywords = ArrayField(models.CharField(max_length=40, blank=True))

    def __str__(self):
        return self.PMID