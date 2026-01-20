from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import Course, Schedule, Teacher
from datetime import time
import random

class Command(BaseCommand):
    help = 'Populate sample schedule data for timetable testing'

    def handle(self, *args, **options):
        self.stdout.write('Populating sample schedule data...')
        
        # Clear existing schedules
        Schedule.objects.all().delete()
        
        # Get available courses and ensure we have some
        courses = Course.objects.all()
        if not courses.exists():
            self.stdout.write(self.style.ERROR('No courses found. Please create courses first.'))
            return
        
        # Define time slots (8 AM to 5 PM, 1-hour slots)
        time_slots = [
            (time(8, 0), time(9, 0)),
            (time(9, 0), time(10, 0)),
            (time(10, 0), time(11, 0)),
            (time(11, 0), time(12, 0)),
            (time(12, 0), time(13, 0)),  # Lunch
            (time(13, 0), time(14, 0)),
            (time(14, 0), time(15, 0)),
            (time(15, 0), time(16, 0)),
            (time(16, 0), time(17, 0)),
        ]
        
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        rooms = ['Room 101', 'Room 102', 'Room 103', 'Lab 201', 'Lab 202', 'Computer Lab']
        
        schedules_created = 0
        
        # Create schedules for each course
        for course in courses[:6]:  # Limit to first 6 courses
            # Random number of classes per week (2-4)
            classes_per_week = random.randint(2, 4)
            
            # Pick random days for this course
            course_days = random.sample(days, classes_per_week)
            
            for day in course_days:
                # Pick a random time slot
                start_time, end_time = random.choice(time_slots)
                room = random.choice(rooms)
                
                # Check if this slot is already taken
                existing_schedule = Schedule.objects.filter(
                    day=day,
                    start_time=start_time,
                    room=room
                ).first()
                
                if not existing_schedule:
                    Schedule.objects.create(
                        course=course,
                        day=day,
                        start_time=start_time,
                        end_time=end_time,
                        room=room
                    )
                    schedules_created += 1
                    self.stdout.write(f'Created schedule: {course.title} on {day} at {start_time}-{end_time} in {room}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {schedules_created} schedule entries')
        ) 