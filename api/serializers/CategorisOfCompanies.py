from rest_framework import serializers
from api.models import Companies
from api.models import CategoriesOfCompanies
from api.serializers.CompanySerializer import CompanySerializer

class CategoriesOfCompaniesSerializer(serializers.ModelSerializer):
    categ_comp = serializers.SerializerMethodField()

    class Meta:
        model = CategoriesOfCompanies
        fields = 'categ_comp'

    def get_category_comp(self, obj):
        company = Companies.objects.filter(company=obj)
        company_serializer = CompanySerializer(company, many=True, context=self.context).data
        return company_serializer


