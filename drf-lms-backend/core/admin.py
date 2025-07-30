from django.contrib import admin
from .models import Category, Course, Lesson, Material, Enrollment, QuestionAnswer

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'duration', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at', 'instructors')
    search_fields = ('title', 'description')
    filter_horizontal = ('instructors',)  # pretty multi-select

admin.site.register(Lesson)
admin.site.register(Material)
admin.site.register(Enrollment)
admin.site.register(QuestionAnswer)


"""
alternatively: pre m2m:
admin.site.register([Category, Course, Lesson, Material, Enrollment, QuestionAnswer])  # List
admin.site.register((Category, Course, Lesson, Material, Enrollment, QuestionAnswer))  # Tuple
for model in [Category, Course, Lesson, Material, Enrollment, QuestionAnswer]:
    admin.site.register(model)
"""