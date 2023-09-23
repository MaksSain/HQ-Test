from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

class Lesson(models.Model):
    title = models.CharField(max_length=100)
    video_link = models.URLField()
    duration_seconds = models.IntegerField()
    products = models.ManyToManyField(Product)

class LessonView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    viewed = models.BooleanField(default=False)
    viewed_time = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)