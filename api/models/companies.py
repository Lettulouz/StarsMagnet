from django.db import models

COMPANIES_STATUS = (
    ('pending', 'Waiting for acceptation'),
    ('accepted', 'Application accepted'),
    ('rejected', 'Application rejected'),
    ('banned', 'Company banned')
)


class Companies(models.Model):
    name = models.CharField(max_length=80)
    site = models.URLField()
    token = models.CharField(max_length=32)
    login = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    status = models.CharField(choices=COMPANIES_STATUS, max_length=30, default='pending')

