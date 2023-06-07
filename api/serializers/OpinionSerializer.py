from rest_framework import serializers
from api.models import Opinions


class OpinionSerializer(serializers.ModelSerializer):
    ratingDate = serializers.DateTimeField(source='rating_date')
    commentDate = serializers.DateTimeField(source='comment_date')
    responseDate = serializers.DateTimeField(source='response_date')
    companyResponse = serializers.CharField(source='company_response')
    userId = serializers.CharField(source='user_id')
    companyId = serializers.CharField(source='company_id')

    class Meta:
        model = Opinions
        fields = ("userId",
                  'companyId',
                  'rating',
                  "ratingDate",
                  'comment',
                  'commentDate',
                  'companyResponse',
                  "responseDate")


