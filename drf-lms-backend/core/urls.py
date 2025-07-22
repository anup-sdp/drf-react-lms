from django.urls import path
from .views import category_list_create, course_list_create, course_detail, lesson_list_create, material_list_create, enrollment_list_create, questionanswer_list_create

urlpatterns = [
    path('categories/', category_list_create, name='category_list_create'),
    path('courses/', course_list_create, name='course_list_create'),
    path('courses/<int:pk>/', course_detail, name='course_detail'),
    path('lessons/', lesson_list_create, name='lesson_list_create'),
    path('materials/', material_list_create, name='material_list_create'),
    path('enrollments/', enrollment_list_create, name='enrollment_list_create'),
    path('questions/', questionanswer_list_create, name='questionanswer_list_create'),
]
