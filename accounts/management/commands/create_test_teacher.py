from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Teacher
from datetime import datetime

class Command(BaseCommand):
    help = 'Creates a test teacher account'

    def handle(self, *args, **kwargs):
        try:
            # Check if user already exists
            username = 'teacher1'
            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.WARNING(f'User {username} already exists'))
                return

            # Create user
            user = User.objects.create_user(
                username=username,
                password='teacher123',
                first_name='Test',
                last_name='Teacher',
                email='teacher@example.com'
            )

            # Create teacher profile with all required fields
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

            self.stdout.write(self.style.SUCCESS(f'Successfully created teacher account with username: {username} and password: teacher123'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating teacher account: {str(e)}')) 