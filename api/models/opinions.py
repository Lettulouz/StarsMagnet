from django.db import models
from django.conf import settings
from .companies import Companies
from django.core.exceptions import ValidationError

OPINIONS_SIDE = (
    ("user", "User comment"),
    ("company", "Company reply")
)


def validate_interval(value):
    if value < 0.0 or value > 10.0:
        raise ValidationError('Rating must be in range [0, 10]')


class Opinions(models.Model):
    rating = models.FloatField(validators=[validate_interval])
    rating_date = models.DateTimeField()
    comment = models.TextField(null=True, blank=True)
    comment_date = models.DateTimeField(null=True, blank=True)
    company_response = models.TextField(null=True, blank=True)
    response_date = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, to_field='id', db_column='user_id', on_delete=models.CASCADE)
    company = models.ForeignKey(Companies, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Opinions"

