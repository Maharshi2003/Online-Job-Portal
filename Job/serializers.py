from rest_framework import serializers
from .models import Job_Seeker
from .models import Category
from .models import Company

class Job_SeekerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job_Seeker
        fields = '_all_'
        
class CategorySerializer(serializers.ModelSerializer):
      class Meta:
        model = Category
        fields = '_all_'
        
class CompanySerializer(serializers.ModelSerializer):
      class Meta:
        model = Company
        fields = '_all_'