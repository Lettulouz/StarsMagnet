import math
from rest_framework import serializers
from api.models import Companies
from api.models import Opinions
from api.models import Categories
from api.models import CategoriesOfCompanies
from django.db.models import Avg


class CompanySerializer(serializers.ModelSerializer):
    avgRatings = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    opinionsCount = serializers.SerializerMethodField()

    class Meta:
        model = Companies
        fields = ("id",
                  'name',
                  'site',
                  "avgRatings",
                  "opinionsCount",
                  "categories")

    def get_avgRatings(self, obj):
        avg_ratings = Opinions.objects.filter(company=obj).aggregate(rating=Avg('rating'))
        if avg_ratings['rating'] is None:
            return avg_ratings['rating']
        return math.ceil(avg_ratings['rating'] * 10) / 10

    def get_opinionsCount(self, obj):
        return Opinions.objects.filter(company=obj).count()

    def get_categories(self, obj):
        categories = CategoriesOfCompanies.objects.filter(company_id=obj.id)
        return [{'name': category.category.name, 'icon': category.category.icon, 'id': category.category.id } for category in categories]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if 'category' in self.context:
            category = Categories.objects.filter(pk=self.context['category']).first()
            representation["category_name"] = category.name
        return representation

