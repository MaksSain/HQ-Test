from rest_framework import generics, permissions
from django.db.models import Count, Sum
from django.db.models.functions import Coalesce
from .models import Lesson, LessonView, Product
from .serializers import LessonSerializer, LessonViewSerializer, ProductSerializer

class LessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        lessons = Lesson.objects.filter(products__productaccess__user=user)
        for lesson in lessons:
            try:
                lesson_view = LessonView.objects.get(user=user, lesson=lesson)
                lesson.viewed = lesson_view.viewed
                lesson.viewed_time = lesson_view.viewed_time
            except LessonView.DoesNotExist:
                lesson.viewed = False
                lesson.viewed_time = 0
        return lessons

class LessonByProductView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        product_id = self.kwargs['product_id']
        lessons = Lesson.objects.filter(products__id=product_id, products__productaccess__user=user)
        for lesson in lessons:
            try:
                lesson_view = LessonView.objects.filter(user=user, lesson=lesson).latest('viewed_time')
                lesson.viewed = lesson_view.viewed
                lesson.viewed_time = lesson_view.viewed_time
                lesson.last_viewed_date = lesson_view.date
            except LessonView.DoesNotExist:
                lesson.viewed = False
                lesson.viewed_time = 0
                lesson.last_viewed_date = None
        return lessons

class ProductStatisticsView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        products = Product.objects.all()
        for product in products:
            product.viewed_lessons_count = LessonView.objects.filter(lesson__products=product, viewed=True).count()
            product.total_viewed_time = LessonView.objects.filter(lesson__products=product, viewed=True).aggregate(total_time=Coalesce(Sum('viewed_time'), 0))['total_time']
            product.num_students = ProductAccess.objects.filter(product=product).count()
            total_users_count = User.objects.count()
            product_access_count = ProductAccess.objects.filter(product=product).count()
            product.purchase_percentage = (product_access_count / total_users_count) * 100 if total_users_count > 0 else 0
        return products
