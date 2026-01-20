from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Set or update admin credentials to username: admin, password: admin123'

    def handle(self, *args, **options):
        new_username = 'admin'
        new_password = 'admin123'
        new_email = 'admin@example.com'
        old_username = 'kaushik'
        
        try:
            # Check if old kaushik user exists and remove it
            try:
                old_user = User.objects.get(username=old_username)
                old_user.delete()
                self.stdout.write(self.style.SUCCESS(f'Removed old admin user "{old_username}"'))
            except User.DoesNotExist:
                self.stdout.write(f'Old admin user "{old_username}" not found (already removed)')
            
            # Ensure the new admin user exists with correct credentials
            try:
                user = User.objects.get(username=new_username)
                self.stdout.write(f'Admin user "{new_username}" already exists. Updating credentials...')
            except User.DoesNotExist:
                # Create new admin user
                user = User.objects.create_user(
                    username=new_username,
                    email=new_email,
                    password=new_password,
                    first_name='Admin',
                    last_name='User',
                    is_staff=True,
                    is_superuser=True
                )
                self.stdout.write(self.style.SUCCESS(f'Created new admin user "{new_username}"'))
                self.stdout.write(f'Username: {new_username}')
                self.stdout.write(f'Password: {new_password}')
                return
            
            # Update password and permissions for existing user
            user.set_password(new_password)
            user.is_staff = True
            user.is_superuser = True
            user.email = new_email
            user.first_name = 'Admin'
            user.last_name = 'User'
            user.save()
            
            self.stdout.write(self.style.SUCCESS('Successfully updated admin credentials:'))
            self.stdout.write(f'Username: {new_username}')
            self.stdout.write(f'Password: {new_password}')
            self.stdout.write(f'Email: {new_email}')
            
            # Display remaining superusers
            self.stdout.write('\nCurrent superusers:')
            superusers = User.objects.filter(is_superuser=True)
            for su in superusers:
                self.stdout.write(f'- Username: {su.username}, Email: {su.email}')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error updating admin credentials: {str(e)}'))
