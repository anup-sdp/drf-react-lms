# core, views.py:
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly  # is AdminOrReadOnly, custom
from rest_framework import status
from .models import Category, Course, Lesson, Material, Enrollment, QuestionAnswer
from .serializers import (
    CategorySerializer, CourseSerializer, LessonSerializer, MaterialSerializer,
    EnrollmentSerializer, QuestionAnswerSerializer
)
from drf_yasg.utils import swagger_auto_schema

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions

class IsAdminOrTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'teacher']

class IsAdminOrInstructor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        return request.user in obj.instructors.all()

@swagger_auto_schema(method='post', request_body=CategorySerializer)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])  # Optional: restrict all, then manually handle roles
def category_list_create(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True, context={'request': request}) # serialize or deserialize a collection of objects (a queryset or list) instead of a single object.
        return Response(serializer.data)

    elif request.method == 'POST':
        if request.user.role != 'admin':
            return Response({"detail": "Only admin can create categories."}, status= status.HTTP_403_FORBIDDEN) # or status=403

        serializer = CategorySerializer(data=request.data, context={'request': request})  # data for a single category
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@swagger_auto_schema(method='post', request_body=CourseSerializer)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, IsAdminOrTeacher])  # IsAuthenticated, AllowAny  # authentication_classes ?
def course_list_create(request):
    if not request.user.is_authenticated:
        return Response({'detail': 'error: user is not Authenticated'}, status=403)
    if request.method == 'GET':
        if request.user.role in ['admin', 'teacher', 'student']:
            courses = Course.objects.all()        
        else:
            return Response({'detail': 'Unauthorized role'}, status=403)
        
        serializer = CourseSerializer(courses, many=True, context={'request': request}) # Pass request context to serializer
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # Allow both admin and teacher to create courses
        if request.user.role not in ['admin', 'teacher']:
            return Response({'detail': 'Only admins or teachers can create courses.'}, status=403)
                
        serializer = CourseSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='put', request_body=CourseSerializer)
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
        
        
	

@swagger_auto_schema(method='post', request_body=LessonSerializer)
@api_view(['GET', 'POST'])
def lesson_list_create(request):
    if request.method == 'GET':
        lessons = Lesson.objects.all()
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='post', request_body=MaterialSerializer)
@api_view(['GET', 'POST'])
def material_list_create(request):
    if request.method == 'GET':
        materials = Material.objects.all()
        serializer = MaterialSerializer(materials, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = MaterialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='post', request_body=EnrollmentSerializer)
@api_view(['GET', 'POST'])
def enrollment_list_create(request):
    if request.method == 'GET':
        enrollments = Enrollment.objects.all()
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = EnrollmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='post', request_body=QuestionAnswerSerializer)
@api_view(['GET', 'POST'])
def questionanswer_list_create(request):
    if request.method == 'GET':
        questions = QuestionAnswer.objects.all()
        serializer = QuestionAnswerSerializer(questions, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = QuestionAnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)