from rest_framework import serializers
from api.models import Companies
from api.models import Opinions
from api.serializers.OpinionSerializer import OpinionSerializer
from django.db.models import Avg


class CompanySerializer(serializers.ModelSerializer):
    avg_ratings = serializers.SerializerMethodField()
    opinions = serializers.SerializerMethodField()

    class Meta:
        model = Companies
        fields = ("id",
                  'name',
                  'site',
                  "avg_ratings",
                  "opinions")

    def get_opinions(self, obj):
        if not self.context.get('many', False):
            opinions = Opinions.objects.filter(company=obj)
            opinion_serializer = OpinionSerializer(opinions, many=True, context=self.context).data
            return opinion_serializer
        return None

    def get_avg_ratings(self, obj):
        avg_ratings = Opinions.objects.filter(company=obj).aggregate(rating=Avg('rating'))
        return avg_ratings['rating']
