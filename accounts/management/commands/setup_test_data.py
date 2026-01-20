from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Student, Teacher, Course, Activity, Notice
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Sets up test data for the student dashboard'

    def handle(self, *args, **kwargs):
        try:
            # Create teacher
            teacher_user = User.objects.create_user(
                username='teacher001',
                password='teacher123',
                email='teacher001@school.com',
                first_name='Test',
                last_name='Teacher'
            )
            
            teacher = Teacher.objects.create(
                user=teacher_user,
                teacher_id='TCH001',
                first_name='Test',
                last_name='Teacher',
                email='teacher001@school.com',
                phone_number='+1234567890',
                department='Science',
                subjects='Physics',
                joining_date=datetime.now().date()
            )
            
            # Create course
            course = Course.objects.create(
                course_code='PHY101',
                title='Physics 101',
                description='Introduction to Physics',
                teacher=teacher,
                credits=3
            )
            
            # Get the student
            student = Student.objects.get(student_id='STU001')
            
            # Enroll student in course
            course.students.add(student)
            
            # Create some assignments
            for i in range(3):
                Activity.objects.create(
                    title=f'Assignment {i+1}',
                    description=f'This is test assignment {i+1}',
                    course=course,
                    activity_type='assignment',
                    due_date=datetime.now() + timedelta(days=i+1)
                )
            
            # Create some notices
            for i in range(3):
                Notice.objects.create(
                    title=f'Test Notice {i+1}',
                    content=f'This is test notice {i+1}',
                    notice_type='general',
                    target_audience='students',
                    created_by=teacher_user
                )
            
            self.stdout.write(self.style.SUCCESS('Successfully created test data'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating test data: {str(e)}')) 