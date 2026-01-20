from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import Student, Course, Attendance
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Populate sample attendance data for realistic report statistics'

    def handle(self, *args, **options):
        self.stdout.write('Populating sample attendance data...')
        
        # Get students and courses
        students = Student.objects.all()
        courses = Course.objects.all()
        
        if not students.exists() or not courses.exists():
            self.stdout.write(self.style.ERROR('Need students and courses to create attendance. Please create them first.'))
            return
        
        # Clear existing attendance for clean test
        Attendance.objects.all().delete()
        
        attendance_created = 0
        
        # Create attendance records for the past 30 days
        start_date = timezone.now().date() - timedelta(days=30)
        end_date = timezone.now().date()
        
        # Generate attendance for each day in the range
        current_date = start_date
        while current_date <= end_date:
            # Skip weekends for school attendance
            if current_date.weekday() < 5:  # Monday = 0, Friday = 4
                
                for student in students:
                    enrolled_courses = student.enrolled_courses.all()
                    
                    # If no enrolled courses, use some courses for demo
                    if not enrolled_courses.exists():
                        enrolled_courses = courses[:2]  # Limit to first 2 courses
                    
                    for course in enrolled_courses:
                        # 85% chance of being present (realistic attendance rate)
                        attendance_chance = random.random()
                        
                        if attendance_chance < 0.85:  # 85% present
                            status = 'present'
                        elif attendance_chance < 0.92:  # 7% late
                            status = 'late'
                        elif attendance_chance < 0.97:  # 5% excused
                            status = 'excused'
                        else:  # 3% absent
                            status = 'absent'
                        
                        Attendance.objects.create(
                            student=student,
                            course=course,
                            date=current_date,
                            status=status,
                            remarks=f'Auto-generated attendance for {current_date}'
                        )
                        attendance_created += 1
            
            current_date += timedelta(days=1)
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {attendance_created} attendance records')
        ) 