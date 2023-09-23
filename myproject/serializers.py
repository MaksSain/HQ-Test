from rest_framework import serializers
from .models import Product, Lesson, LessonView

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'owner')

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'title', 'video_link', 'duration_seconds', 'products')

class LessonViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonView
        fields = ('id', 'user', 'lesson', 'viewed', 'viewed_time')
