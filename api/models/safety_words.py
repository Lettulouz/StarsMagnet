from django.db import models
from .companies import Companies


class Safety_Words(models.Model):
    user = models.ForeignKey(Companies, on_delete=models.CASCADE)
    word1 = models.CharField(max_length=7);
    word2 = models.CharField(max_length=7);
    word3 = models.CharField(max_length=7);
    word4 = models.CharField(max_length=7);
    word5 = models.CharField(max_length=7);
    word6 = models.CharField(max_length=7);
    word7 = models.CharField(max_length=7);
    word8 = models.CharField(max_length=7);
    word9 = models.CharField(max_length=7);
    word10 = models.CharField(max_length=7);

