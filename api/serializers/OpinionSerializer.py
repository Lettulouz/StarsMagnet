from django.contrib.auth import get_user_model
from rest_framework import serializers
from api.models import Opinions
User = get_user_model()

class OpinionSerializer(serializers.ModelSerializer):
    ratingDate = serializers.DateTimeField(source='rating_date')
    commentDate = serializers.DateTimeField(source='comment_date')
    responseDate = serializers.DateTimeField(source='response_date')
    companyResponse = serializers.CharField(source='company_response')
    userId = serializers.IntegerField(source='user_id')
    username = serializers.SerializerMethodField()
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = Opinions
        fields = ["userId",
                  "username",
                  "fullname",
                  'rating',
                  "ratingDate",
                  'comment',
                  'commentDate',
                  'companyResponse',
                  "responseDate"]

    def get_fullname(self, obj):
        user = User._default_manager.filter(id=obj.user_id).first()
        if user:
            return f"{user.first_name} {user.last_name}"
        return ""

    def get_username(self, obj):
        user = User._default_manager.filter(id=obj.user_id).first()
        if user:
            return user.username
        return ""