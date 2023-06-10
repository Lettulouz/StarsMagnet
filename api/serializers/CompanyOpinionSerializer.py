from django.contrib.auth import get_user_model
from rest_framework import serializers
from api.models import Opinions
import datetime
User = get_user_model()


class CompanyOpinionSerializer(serializers.ModelSerializer):
    userId = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    companyResponse = serializers.CharField(source='company_response')

    class Meta:
        model = Opinions
        fields = ('companyResponse', 'userId')
        extra_kwargs = {'companyResponse': {'required': True}}

    def save(self):
        actual_time = datetime.datetime.now()
        company_id = self.context['request'].user.id
        user_id = self.validated_data['userId'].id

        opinion = Opinions.objects.get(company_id=company_id, user_id=user_id)
        opinion.company_response = self.validated_data['company_response']
        opinion.response_date = actual_time

        opinion.save()
        return opinion
