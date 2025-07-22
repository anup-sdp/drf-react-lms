project requirement (vs BRD - business requirement document -- search)
# LMS Project - DRF - Ostad

## Project Target

To build a Learning Platform with Django Rest Framework where Admin can manage users and courses, 
teachers can create read update delete their courses, and students can enroll to courses.

## User Roles & Features

### Admin

- Can create and manage users (teachers and students)
- Can create and manage course categories
- Can see platform-wide statistics (like total users, total courses)
- Can moderate or remove courses if needed

### Teacher

- Can create, edit, and delete courses
- Can upload lessons and learning materials (like videos or PDFs)
- Can view a list of students enrolled in their courses
- Can track student progress and provide feedback

### Student

- Can view available courses and enroll in them (paid / free)
- Course search and filtering by category
- Can watch videos and access materials in the course
- Can track their own progress in each course
- Can ask questions related to lessons
- Certificate generation after completing a course

### Authentication
- JWT
- pagination
- rate limiting

# -------------------------------------------------------------
erd: 
https://drawsql.app/teams/phitron/diagrams/lms
https://dbdiagram.io/d/LMS_erd-683c7788bd74709cb78c8e86
https://app.quickdatabasediagrams.com/#/d/JoXmLv
