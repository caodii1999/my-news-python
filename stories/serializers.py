''' Serialisers.py'''
# from django.contrib.auth.models import User, Group
from .models import Category, Story
from rest_framework import serializers

class StorySerializer(serializers.HyperlinkedModelSerializer):    
    category = serializers.CharField(source='category.id')    
    class Meta:
        model = Story    
        fields = '__all__'

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    stories = StorySerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ('name', 'stories')
        