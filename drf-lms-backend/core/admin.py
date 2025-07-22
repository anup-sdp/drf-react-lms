from django.contrib import admin
from .models import Category, Course, Lesson, Material, Enrollment, QuestionAnswer
# Register your models here.


admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Material)
admin.site.register(Enrollment)
admin.site.register(QuestionAnswer)


"""
alternatively:
admin.site.register([Category, Course, Lesson, Material, Enrollment, QuestionAnswer])  # List
admin.site.register((Category, Course, Lesson, Material, Enrollment, QuestionAnswer))  # Tuple
for model in [Category, Course, Lesson, Material, Enrollment, QuestionAnswer]:
    admin.site.register(model)
"""