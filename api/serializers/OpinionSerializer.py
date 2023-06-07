from rest_framework import serializers
from api.models import Opinions


class OpinionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Opinions
        fields = ("user_id",
                  'company_id',
                  'rating',
                  "rating_date",
                  'comment',
                  'comment_date',
                  'company_response',
                  "response_date")

