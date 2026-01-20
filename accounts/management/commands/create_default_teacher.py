from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Teacher
from datetime import datetime

class Command(BaseCommand):
    help = 'Create a default teacher user'

    def handle(self, *args, **kwargs):
        username = 'default_teacher'
        email = 'teacher@example.com'
        password = 'TeacherPass123!'
        
        try:
            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.WARNING('Default teacher user already exists.'))
                return
                
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name='Default',
                last_name='Teacher'
            )
            user.is_staff = True
            user.save()

            # Create teacher profile with all required fields
            Teacher.objects.create(
                user=user,
                teacher_id='TCH001',
                first_name='Default',
                last_name='Teacher',
                email=email,
                phone_number='+1234567890',
                department='Mathematics',
                subjects='Mathematics, Algebra, Geometry',
                joining_date=datetime.now().date(),
            )

            self.stdout.write(self.style.SUCCESS('Default teacher user created successfully.'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating default teacher: {str(e)}')) 