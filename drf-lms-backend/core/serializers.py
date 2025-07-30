from rest_framework import serializers
from .models import Course, Category, Lesson, Material, Enrollment, QuestionAnswer
from users.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'role', 'mobile_no')

# option to set instructors when creating/updating a course
class CourseSerializer(serializers.ModelSerializer):
    # Read side: show full instructor details
    instructors_details = InstructorSerializer(source='instructors', many=True, read_only=True)
    # Write side: accept list of instructor IDs
    instructors = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.filter(role='teacher'),
        write_only=True
    )
    # This will show instructor IDs in both input and output:
    # instructors = serializers.PrimaryKeyRelatedField(
    #     many=True,
    #     queryset=User.objects.filter(role='teacher')
    # )
    category_title = serializers.CharField(source='category.title', read_only=True)
    
    class Meta:
        model = Course
        fields = '__all__'
        # Or specify fields explicitly:
        # fields = ('id', 'title', 'description', 'banner', 'price', 'duration', 
        #           'is_active', 'category', 'instructors', 'category_title', 
        #           'created_at', 'updated_at')

    def create(self, validated_data):
        instructors_data = validated_data.pop('instructors', [])
        course = Course.objects.create(**validated_data)
        course.instructors.set(instructors_data)
        return course
    
    def update(self, instance, validated_data):
        instructors_data = validated_data.pop('instructors', None)
        if instructors_data is not None:
            instance.instructors.set(instructors_data)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student_id.username', read_only=True)
    course_title = serializers.CharField(source='course_id.title', read_only=True)
    
    class Meta:
        model = Enrollment
        fields = '__all__'

class QuestionAnswerSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user_id.username', read_only=True)
    lesson_title = serializers.CharField(source='lesson_id.title', read_only=True)
    
    class Meta:
        model = QuestionAnswer
        fields = '__all__'

