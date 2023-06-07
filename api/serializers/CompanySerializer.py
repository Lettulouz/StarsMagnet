from rest_framework.pagination import PageNumberPagination
from rest_framework import serializers
from api.models import Companies
from api.models import Opinions
from api.models import Categories
from api.models import CategoriesOfCompanies
from api.serializers.OpinionSerializer import OpinionSerializer
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

    def get_opinions(self, obj):
        if 'request' in self.context:
            opinions = Opinions.objects.filter(company=obj).order_by('-id')
            paginator = PageNumberPagination()
            paginated_opinions = paginator.paginate_queryset(opinions, self.context['request'])
            opinion_serializer = OpinionSerializer(paginated_opinions, many=True, context=self.context).data
            return paginator.get_paginated_response(opinion_serializer).data
        return None

    def get_avgRatings(self, obj):
        avg_ratings = Opinions.objects.filter(company=obj).aggregate(rating=Avg('rating'))
        return avg_ratings['rating']

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
        if 'request' in self.context:
            representation["opinions"] = self.get_opinions(instance)
        return representation

