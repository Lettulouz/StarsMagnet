from django.db import models
from django.conf import settings
from .companies import Companies



OPINIONS_SIDE = (
    ("user", "User comment"),
    ("company", "Company reply")
)

class Opinions(models.Model):
    rating = models.FloatField()
    comment = models.TextField()
    side_of_comment = models.CharField(choices=OPINIONS_SIDE, max_length=30)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, to_field='id', db_column='user_id', on_delete=models.CASCADE)
    company = models.ForeignKey(Companies, on_delete=models.CASCADE)

