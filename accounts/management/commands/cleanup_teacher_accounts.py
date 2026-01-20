from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Teacher

class Command(BaseCommand):
    help = 'Delete specific teacher accounts while keeping teacher1'

    def handle(self, *args, **kwargs):
        try:
            # List of usernames to delete
            usernames_to_delete = ['default_teacher', 'teacher001']
            
            # Delete users and their associated teacher profiles
            for username in usernames_to_delete:
                try:
                    user = User.objects.get(username=username)
                    # Delete the teacher profile first
                    if hasattr(user, 'teacher_profile'):
                        user.teacher_profile.delete()
                    # Then delete the user
                    user.delete()
                    self.stdout.write(self.style.SUCCESS(f'Successfully deleted account: {username}'))
                except User.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'User {username} does not exist'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error deleting {username}: {str(e)}'))
            
            # Verify teacher1 exists
            if User.objects.filter(username='teacher1').exists():
                self.stdout.write(self.style.SUCCESS('teacher1 account is preserved'))
            else:
                self.stdout.write(self.style.WARNING('teacher1 account not found'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error during cleanup: {str(e)}')) 