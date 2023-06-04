from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=30, unique=True)
    icon = models.CharField(max_length=55)

    class Meta:
        verbose_name_plural = "Categories"

