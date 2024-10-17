from django.db import models
import random



# Create your models here.
class Summaries(models.Model):
    ticker = models.CharField(max_length=8)
    date = models.DateField()
    overall_rating = models.FloatField(null=True)
    
    
class Articles(models.Model):
    ticker = models.CharField(max_length=8)
    date = models.DateField()
    title = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    pos_score = models.FloatField(null=True)
    neg_score = models.FloatField(null=True)
    overall_rating = models.FloatField(null=True)