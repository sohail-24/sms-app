from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Teacher
from datetime import datetime

class Command(BaseCommand):
    help = 'Reset and create a new teacher account'

    def handle(self, *args, **kwargs):
        try:
            # Delete existing teacher account if exists
            User.objects.filter(username='teacher1').delete()
            Teacher.objects.filter(email='teacher@example.com').delete()
            
            # Create new user
            user = User.objects.create_user(
                username='teacher1',
                password='teacher123',
                first_name='Test',
                last_name='Teacher',
                email='teacher@example.com'
            )
            
            # Create teacher profile
            teacher = Teacher.objects.create(
                user=user,
                teacher_id='TCH001',
                first_name='Test',
                last_name='Teacher',
                email='teacher@example.com',
                phone_number='+1234567890',
                department='Mathematics',
                subjects='Mathematics, Algebra, Geometry',
                joining_date=datetime.now().date()
            )
            
            self.stdout.write(self.style.SUCCESS('Successfully created teacher account'))
            self.stdout.write('Username: teacher1')
            self.stdout.write('Password: teacher123')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}')) 