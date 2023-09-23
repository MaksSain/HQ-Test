from django.urls import path
from . import views

urlpatterns = [
    path('lessons/', views.LessonListView.as_view(), name='lesson-list'),
    path('lessons/by-product/<int:product_id>/', views.LessonByProductView.as_view(), name='lesson-by-product'),
    path('product-statistics/', views.ProductStatisticsView.as_view(), name='product-statistics'),
]
