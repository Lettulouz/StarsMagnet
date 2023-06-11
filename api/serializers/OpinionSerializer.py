from django.contrib.auth import get_user_model
from rest_framework import serializers
from api.models import Opinions
User = get_user_model()

class OpinionSerializer(serializers.ModelSerializer):
    """
    Serializer to display opinions.
    """
    ratingDate = serializers.DateTimeField(source='rating_date')
    commentDate = serializers.DateTimeField(source='comment_date')
    responseDate = serializers.DateTimeField(source='response_date')
    companyResponse = serializers.CharField(source='company_response')
    userId = serializers.IntegerField(source='user_id')
    fullname = serializers.SerializerMethodField()
    countOfReviews = serializers.SerializerMethodField()

    class Meta:
        """
        Metadata for OpinionSerializer.
        Contains opinions model and field
        """
        model = Opinions
        fields = ["userId",
                  "fullname",
                  "countOfReviews",
                  'rating',
                  "ratingDate",
                  'comment',
                  'commentDate',
                  'companyResponse',
                  "responseDate"]

    def get_fullname(self, obj):
        """
        Method returns the name of the commenter for a given opinions
        :param obj: opinion obj
        :return: fullname of commenter
        """
        user = User._default_manager.filter(id=obj.user_id).first()
        if user:
            return f"{user.first_name} {user.last_name}"
        return ""

    def get_countOfReviews(self, obj):
        """
        The method returns the number of reviews of a given user
        :param obj: opinion object
        :return: the number of reviews of a given user
        """
        user = User._default_manager.filter(id=obj.user_id).first()
        if user:
            return Opinions.objects.filter(user_id=user.id).count()
        return 0