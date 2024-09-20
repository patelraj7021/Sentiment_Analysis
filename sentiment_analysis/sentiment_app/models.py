from django.db import models
import random


""" def generate_ID():
    length = 7
    while True:
        ID = random.randint(0, 10**6)
        if Analysis.objects.filter(ID=ID).count() == 0:
            break
    return  """

# Create your models here.
class Analysis(models.Model):
    ticker = models.CharField(max_length=8)
    date = models.DateField()
    pos_sentiment = models.FloatField(default=0., null=True)
    neg_sentiment = models.FloatField(default=0., null=True)