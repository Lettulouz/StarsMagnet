import math
from rest_framework import serializers
from api.models import Companies
from api.models import Opinions
from api.models import Categories
from api.models import CategoriesOfCompanies
from django.db.models import Avg


class CompanySerializer(serializers.ModelSerializer):
    """
    Serializer to display companies with additional information.
    """
    avgRatings = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    opinionsCount = serializers.SerializerMethodField()

    class Meta:
        """
       Metadata for CompanySerializer.
       Contains companies model and field
       """
        model = Companies
        fields = ("id",
                  'name',
                  'site',
                  "avgRatings",
                  "opinionsCount",
                  "categories")

    def get_avgRatings(self, obj):
        """
        The method returns the average value of the ratings of a given company
        :param obj: company object
        :return: grade point average rounded to one decimal place
        """
        avg_ratings = Opinions.objects.filter(company=obj).aggregate(rating=Avg('rating'))
        if avg_ratings['rating'] is None:
            return avg_ratings['rating']
        return math.ceil(avg_ratings['rating'] * 10) / 10

    def get_opinionsCount(self, obj):
        """
        The method returns the number of reviews of a given company
        :param obj: company object
        :return: the number of reviews of a given company
        """
        return Opinions.objects.filter(company=obj).count()

    def get_categories(self, obj):
        """
        Method collects all categories for a given company
        :param obj: company object
        :return: list of categories of a particular company
        """
        categories = CategoriesOfCompanies.objects.filter(company_id=obj.id)
        return [{'name': category.category.name, 'icon': category.category.icon, 'id': category.category.id } for category in categories]

    def to_representation(self, instance):
        """
        Converts the model object to its representation in the format that will be returned in the response
        :param instance: model object
        :return: object representatuib
        """
        representation = super().to_representation(instance)
        if 'category' in self.context:
            category = Categories.objects.filter(pk=self.context['category']).first()
            representation["category_name"] = category.name
        return representation

