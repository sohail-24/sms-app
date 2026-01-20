from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import Student, Course, Grade, Examination
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Populate sample grade data for realistic report statistics'

    def handle(self, *args, **options):
        self.stdout.write('Populating sample grade data...')
        
        # Get students and courses
        students = Student.objects.all()
        courses = Course.objects.all()
        
        if not students.exists() or not courses.exists():
            self.stdout.write(self.style.ERROR('Need students and courses to create grades. Please create them first.'))
            return
        
        # Clear existing grades for clean test
        Grade.objects.all().delete()
        
        grades_created = 0
        
        # Create grades for each student in each course they're enrolled in
        for student in students:
            enrolled_courses = student.enrolled_courses.all()
            
            # If no enrolled courses, use all courses for demo
            if not enrolled_courses.exists():
                enrolled_courses = courses[:3]  # Limit to first 3 courses
            
            for course in enrolled_courses:
                # Create 2-4 grades per student per course (multiple assessments)
                num_grades = random.randint(2, 4)
                
                for i in range(num_grades):
                    # Generate realistic grade distributions
                    # 70% of grades between 70-90, 20% between 90-100, 10% below 70
                    rand = random.random()
                    if rand < 0.1:  # 10% below 70
                        score = random.uniform(40, 69)
                        grade_letter = 'F' if score < 60 else 'D'
                    elif rand < 0.8:  # 70% between 70-90
                        score = random.uniform(70, 89)
                        if score >= 80:
                            grade_letter = 'B'
                        else:
                            grade_letter = 'C'
                    else:  # 20% between 90-100
                        score = random.uniform(90, 100)
                        grade_letter = 'A+' if score >= 95 else 'A'
                    
                    # Create grade with a date in the past 3 months
                    grade_date = timezone.now().date() - timedelta(days=random.randint(1, 90))
                    
                    Grade.objects.create(
                        student=student,
                        subject=course,
                        score=round(score, 1),
                        grade=grade_letter,
                        date=grade_date,
                        remarks=f'Assessment {i+1} for {course.title}'
                    )
                    grades_created += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {grades_created} grade records')
        ) 