from django.core.exceptions import ValidationError
from django.db import models
from .companies import Companies
from .categories import Categories


class CategoriesOfCompanies(models.Model):
    company = models.ForeignKey(Companies, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "CategoriesOfCompanies"

    def __str__(self):
        return self.category.name +"-"+ self.company.name

