from rest_framework import serializers
from api.models import Opinions


class OpinionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Opinions
        fields = ("rating",
                  "rating_date",
                  'comment',
                  'comment_date',
                  'company_response',
                  "response_date")

