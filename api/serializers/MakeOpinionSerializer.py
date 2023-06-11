from rest_framework import serializers
from api.models import Opinions, Companies
import datetime


class MakeOpinionSerializer(serializers.ModelSerializer):
    """
    Serializer for adding and editing user reviews, i.e. ratings and comments
    """
    companyId = serializers.PrimaryKeyRelatedField(queryset=Companies.objects.all())

    class Meta:
        """
        Metadata for MakeOpinionSerializer.
        Contains opinions model and field
        """
        model = Opinions
        fields = ('rating', 'comment', 'companyId')

    def save(self):
        """
        Method to save new or edited opinion in database.
        :return: opinion object
        """
        actual_time = datetime.datetime.now()
        company_id = self.validated_data['companyId'].id
        user_id = self.context['request'].user.id

        try:
            opinion = Opinions.objects.get(company_id=company_id, user_id=user_id)
            if opinion.rating != self.validated_data['rating']:
                opinion.rating = self.validated_data['rating']
                opinion.rating_date = actual_time
            if self.validated_data.get('comment') is not None:
                opinion.comment = self.validated_data['comment']
                opinion.comment_date = actual_time
        except Opinions.DoesNotExist:
            opinion = Opinions.objects.create(
                rating=self.validated_data['rating'],
                rating_date=actual_time,
                company_id=self.validated_data['companyId'].id,
                user_id=self.context['request'].user.id
            )

            comment = self.validated_data.get('comment')
            if comment is not None:
                opinion.comment = comment
                opinion.comment_date = actual_time

        opinion.save()
        return opinion
