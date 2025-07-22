from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser  # vs AbstractBaseUser (more customization)

USER_ROLES = (('admin', 'Admin'),('teacher', 'Teacher'),('student', 'Student'))  # tuple of 2-value tuples 

class User(AbstractUser):
    role = models.CharField(max_length=10, choices=USER_ROLES)
    mobile_no = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


"""
user = User.objects.create(username="alice", role="teacher")
# In the database, role = "teacher" (lowercase)
print(user.role)  # Output: "teacher"
# In Django Admin/forms, this displays as "Teacher"
# Use the second elements ('Admin', 'Teacher', 'Student') for human-readable output via methods like get_role_display() # user.get_role_display()
"""	

# AbstractUser provides standard fields like  username, email, first_name, last_name, is_staff, is_superuser, etc.


# preferred ways:
"""
class User(AbstractUser):
    class RoleChoices(models.TextChoices):
        STUDENT = "s", "Student"
        TEACHER = "t", "Teacher"
        ADMIN = "a", "Admin"

    mobile_no = models.CharField(max_length=15, unique=True)
    role = models.CharField(
        max_length=20,
        choices=RoleChoices.choices,
        default=RoleChoices.STUDENT,
    )

# Example:
# User.objects.filter(role="s")
# User.objects.filter(role=User.RoleChoices.STUDENT)
"""


"""
# enum:
from django.db import models
from django.contrib.auth.models import AbstractUser
import enum

class UserRole(enum.TextChoices): # or enum.IntegerChoices if you prefer numeric values
    ADMIN = 'admin', 'Admin'
    TEACHER = 'teacher', 'Teacher'
    STUDENT = 'student', 'Student'

class User(AbstractUser):
    role = models.CharField(
        max_length=10,
        choices=UserRole.choices,
        default=UserRole.STUDENT # Optional: set a default role
    )
    mobile_no = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})" # Use get_role_display() for the human-readable value
"""