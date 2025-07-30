# core, moels.py:
from django.db import models
# from django.contrib.auth.models import User
from users.models import User


class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)  # Added description field
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    banner = models.ImageField(upload_to='course_banners/', blank=True)  # MEDIA_ROOT/course_banners/ ---- image
    price = models.FloatField()
    duration = models.FloatField()
    is_active = models.BooleanField()    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Changed from category_id
    #instructor_id = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role' : 'teacher'})
    instructors = models.ManyToManyField(User, limit_choices_to={'role': 'teacher'}, related_name='courses')  # made m2m field 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    video = models.FileField(upload_to='lesson_videos')
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Material(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    file_type= models.CharField(max_length=100)
    file = models.FileField(upload_to='materials/')
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Enrollment(models.Model):
    student_id = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role' : 'student'})
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    price = models.FloatField()
    progress = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    total_mark = models.FloatField(default=0)
    is_certificate_ready = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student_id.username} - {self.course_id.title}"

class QuestionAnswer(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson_id = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user_id.username} --> {self.lesson_id.title} --> {self.description}"
    