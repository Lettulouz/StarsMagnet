from rest_framework import serializers
from api.models import Companies


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Companies
        fields = ("id",
                  'name',
                  'site')
