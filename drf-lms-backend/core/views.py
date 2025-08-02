# core, views.py:
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework import status
from .models import Category, Course, Lesson, Material, Enrollment, QuestionAnswer
from .serializers import (
    CategorySerializer, CourseSerializer, LessonSerializer, MaterialSerializer,
    EnrollmentSerializer, QuestionAnswerSerializer
)
from django.db.models import Count
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsAdminOrTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'teacher']

class IsAdminOrInstructor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        return request.user in obj.instructors.all()

class IsAuthenticatedForGetOrAdminTeacherForPost(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
            
        if request.method == 'GET':
            return True  # Allow any authenticated user for GET
        elif request.method == 'POST':
            return request.user.role in ['admin', 'teacher']  # Restrict POST to admin/teacher
        return False

@swagger_auto_schema(method='get', responses={200: CategorySerializer(many=True)})
@swagger_auto_schema(method='post', request_body=CategorySerializer, responses={201: CategorySerializer})
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def category_list_create(request):
    if request.method == 'GET':
        #categories = Category.objects.all()
        categories = Category.objects.annotate(courses_count=Count('course'))
        serializer = CategorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        if request.user.role != 'admin':
            return Response({"detail": "Only admin can create categories."}, status=status.HTTP_403_FORBIDDEN)
        serializer = CategorySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='get', responses={200: CategorySerializer})
@swagger_auto_schema(method='put', request_body=CategorySerializer, responses={200: CategorySerializer})
@swagger_auto_schema(method='delete', responses={204: 'No Content'})
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def category_detail(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response({'detail': 'Category not found'}, status=404)
    
    if request.method == 'GET':
        serializer = CategorySerializer(category, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        if request.user.role != 'admin':
            return Response({"detail": "Only admin can update categories."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = CategorySerializer(category, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        if request.user.role != 'admin':
            return Response({"detail": "Only admin can delete categories."}, status=status.HTTP_403_FORBIDDEN)
        
        if Course.objects.filter(category=category).exists():
            return Response(
                {"detail": "Cannot delete category because it is associated with courses."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@swagger_auto_schema(method='get', responses={200: CourseSerializer(many=True)})
@swagger_auto_schema(method='post', request_body=CourseSerializer, responses={201: CourseSerializer})
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedForGetOrAdminTeacherForPost])  # Fixed permission class
def course_list_create(request):
    if request.method == 'GET':
        # All authenticated users can see the course list        
        courses = Course.objects.all().order_by('category__title', 'title')  # Sort by category title, then course title
        serializer = CourseSerializer(courses, many=True, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # Only admins and teachers can create courses
        # (This is now handled by the permission class, but we keep the check for clarity)
        if request.user.role not in ['admin', 'teacher']:
            return Response({'detail': 'Only admins or teachers can create courses.'}, status=status.HTTP_403_FORBIDDEN)
                
        serializer = CourseSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='get', responses={200: CourseSerializer})
@swagger_auto_schema(method='put', request_body=CourseSerializer, responses={200: CourseSerializer})
@swagger_auto_schema(method='delete', responses={204: 'No Content'})
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated, IsAdminOrInstructor])
def course_detail(request, pk):
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response({'detail': 'Course not found'}, status=404)
    
    if request.method == 'GET':
        # Admin can view any course
        if request.user.role == 'admin':
            pass
        # Teacher can view only courses they're instructing
        elif request.user.role == 'teacher':
            if request.user not in course.instructors.all():
                return Response({'detail': 'Permission denied'}, status=403)
        # Student can view any course
        elif request.user.role == 'student':
            pass
        else:
            return Response({'detail': 'Unauthorized role'}, status=403)
        
        serializer = CourseSerializer(course, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        # Admin can update any course
        if request.user.role == 'admin':
            pass
        # Teacher can update only courses they're instructing
        elif request.user.role == 'teacher':
            if request.user not in course.instructors.all():
                return Response({'detail': 'Only instructors of this course can update it.'}, status=403)
        else:
            return Response({'detail': 'Unauthorized role'}, status=403)
        serializer = CourseSerializer(course, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        # Admin can delete any course
        if request.user.role == 'admin':
            pass
        # Teacher can delete only courses they're instructing
        elif request.user.role == 'teacher':
            if request.user not in course.instructors.all():
                return Response({'detail': 'Only instructors of this course can delete it.'}, status=403)
        else:
            return Response({'detail': 'Unauthorized role'}, status=403)
        
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
@swagger_auto_schema(method='get', responses={200: LessonSerializer(many=True)})
@swagger_auto_schema(method='post', request_body=LessonSerializer, responses={201: LessonSerializer})
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])  # Added authentication requirement
def lesson_list_create(request):
    if request.method == 'GET':
        lessons = Lesson.objects.all()
        serializer = LessonSerializer(lessons, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = LessonSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='get', responses={200: MaterialSerializer(many=True)})
@swagger_auto_schema(method='post', request_body=MaterialSerializer, responses={201: MaterialSerializer})
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])  # Added authentication requirement
def material_list_create(request):
    if request.method == 'GET':
        materials = Material.objects.all()
        serializer = MaterialSerializer(materials, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = MaterialSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='get', responses={200: EnrollmentSerializer(many=True)})
@swagger_auto_schema(method='post', request_body=EnrollmentSerializer, responses={201: EnrollmentSerializer})
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])  # Added authentication requirement
def enrollment_list_create(request):
    if request.method == 'GET':
        enrollments = Enrollment.objects.all()
        serializer = EnrollmentSerializer(enrollments, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = EnrollmentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='get', responses={200: QuestionAnswerSerializer(many=True)})
@swagger_auto_schema(method='post', request_body=QuestionAnswerSerializer, responses={201: QuestionAnswerSerializer})
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])  # Added authentication requirement
def questionanswer_list_create(request):
    if request.method == 'GET':
        questions = QuestionAnswer.objects.all()
        serializer = QuestionAnswerSerializer(questions, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = QuestionAnswerSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)