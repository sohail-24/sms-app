from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.utils import timezone
from datetime import datetime, timedelta
import random
from accounts.models import (
    Student, Teacher, Course, Activity, Payment, Invoice, 
    Event, Attendance, Grade, Notice, Class
)

class Command(BaseCommand):
    help = 'Populate database with sample data for dashboard testing'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to populate sample data...'))
        
        # Create sample classes
        self.create_classes()
        
        # Create sample teachers
        self.create_teachers()
        
        # Create sample students
        self.create_students()
        
        # Create sample courses
        self.create_courses()
        
        # Create sample activities
        self.create_activities()
        
        # Create sample attendance records
        self.create_attendance()
        
        # Create sample grades
        self.create_grades()
        
        # Create sample payments and invoices
        self.create_payments_invoices()
        
        # Create sample events
        self.create_events()
        
        self.stdout.write(self.style.SUCCESS('Sample data populated successfully!'))

    def create_classes(self):
        classes_data = [
            {'name': 'Grade 9', 'section': 'A', 'academic_year': '2024-25'},
            {'name': 'Grade 9', 'section': 'B', 'academic_year': '2024-25'},
            {'name': 'Grade 10', 'section': 'A', 'academic_year': '2024-25'},
            {'name': 'Grade 10', 'section': 'B', 'academic_year': '2024-25'},
            {'name': 'Grade 11', 'section': 'Science', 'academic_year': '2024-25'},
            {'name': 'Grade 12', 'section': 'Science', 'academic_year': '2024-25'},
        ]
        
        for class_data in classes_data:
            Class.objects.get_or_create(**class_data)
        
        self.stdout.write('Created sample classes')

    def create_teachers(self):
        # Create teacher group if it doesn't exist
        teacher_group, created = Group.objects.get_or_create(name='Teacher')
        
        teachers_data = [
            {
                'username': 'john_doe',
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john.doe@school.edu',
                'department': 'Mathematics',
                'subjects': 'Algebra, Geometry, Calculus',
                'qualification': 'M.Sc Mathematics',
            },
            {
                'username': 'jane_smith',
                'first_name': 'Jane',
                'last_name': 'Smith', 
                'email': 'jane.smith@school.edu',
                'department': 'Science',
                'subjects': 'Physics, Chemistry',
                'qualification': 'M.Sc Physics',
            },
            {
                'username': 'mike_wilson',
                'first_name': 'Michael',
                'last_name': 'Wilson',
                'email': 'mike.wilson@school.edu',
                'department': 'English',
                'subjects': 'English Literature, Grammar',
                'qualification': 'M.A English',
            },
            {
                'username': 'sarah_brown',
                'first_name': 'Sarah',
                'last_name': 'Brown',
                'email': 'sarah.brown@school.edu',
                'department': 'History',
                'subjects': 'World History, Geography',
                'qualification': 'M.A History',
            },
            {
                'username': 'david_lee',
                'first_name': 'David',
                'last_name': 'Lee',
                'email': 'david.lee@school.edu',
                'department': 'Computer Science',
                'subjects': 'Programming, Data Structures',
                'qualification': 'M.Tech Computer Science',
            }
        ]
        
        for teacher_data in teachers_data:
            # Create user account
            user, created = User.objects.get_or_create(
                username=teacher_data['username'],
                defaults={
                    'first_name': teacher_data['first_name'],
                    'last_name': teacher_data['last_name'],
                    'email': teacher_data['email'],
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                user.groups.add(teacher_group)
            
            # Create teacher profile
            teacher, created = Teacher.objects.get_or_create(
                user=user,
                defaults={
                    'teacher_id': f'T{random.randint(1000, 9999)}',
                    'first_name': teacher_data['first_name'],
                    'last_name': teacher_data['last_name'],
                    'email': teacher_data['email'],
                    'department': teacher_data['department'],
                    'subjects': teacher_data['subjects'],
                    'qualification': teacher_data['qualification'],
                    'joining_date': timezone.now().date() - timedelta(days=random.randint(30, 365)),
                    'is_active': True,
                }
            )
        
        self.stdout.write('Created sample teachers')

    def create_students(self):
        # Create student group if it doesn't exist
        student_group, created = Group.objects.get_or_create(name='Student')
        
        classes = Class.objects.all()
        
        students_data = [
            {'first_name': 'Alex', 'last_name': 'Johnson', 'grade_level': 'Grade 9'},
            {'first_name': 'Emma', 'last_name': 'Davis', 'grade_level': 'Grade 9'},
            {'first_name': 'Liam', 'last_name': 'Miller', 'grade_level': 'Grade 10'},
            {'first_name': 'Olivia', 'last_name': 'Wilson', 'grade_level': 'Grade 10'},
            {'first_name': 'Noah', 'last_name': 'Taylor', 'grade_level': 'Grade 11'},
            {'first_name': 'Ava', 'last_name': 'Anderson', 'grade_level': 'Grade 11'},
            {'first_name': 'Ethan', 'last_name': 'Thomas', 'grade_level': 'Grade 12'},
            {'first_name': 'Sophia', 'last_name': 'Jackson', 'grade_level': 'Grade 12'},
            {'first_name': 'Mason', 'last_name': 'White', 'grade_level': 'Grade 9'},
            {'first_name': 'Isabella', 'last_name': 'Harris', 'grade_level': 'Grade 10'},
            {'first_name': 'Lucas', 'last_name': 'Martin', 'grade_level': 'Grade 11'},
            {'first_name': 'Mia', 'last_name': 'Garcia', 'grade_level': 'Grade 12'},
            {'first_name': 'Logan', 'last_name': 'Rodriguez', 'grade_level': 'Grade 9'},
            {'first_name': 'Charlotte', 'last_name': 'Lewis', 'grade_level': 'Grade 10'},
            {'first_name': 'Benjamin', 'last_name': 'Walker', 'grade_level': 'Grade 11'},
        ]
        
        for i, student_data in enumerate(students_data):
            # Create user account
            username = f"{student_data['first_name'].lower()}_{student_data['last_name'].lower()}"
            email = f"{username}@student.school.edu"
            
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': student_data['first_name'],
                    'last_name': student_data['last_name'],
                    'email': email,
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                user.groups.add(student_group)
            
            # Create student profile
            student, created = Student.objects.get_or_create(
                user=user,
                defaults={
                    'student_id': f'S{2024}{str(i+1).zfill(3)}',
                    'first_name': student_data['first_name'],
                    'last_name': student_data['last_name'],
                    'email': email,
                    'date_of_birth': datetime(2005 + random.randint(0, 4), random.randint(1, 12), random.randint(1, 28)).date(),
                    'gender': random.choice(['M', 'F']),
                    'grade_level': student_data['grade_level'],
                    'phone_number': f'+1{random.randint(2000000000, 9999999999)}',
                    'address': f'{random.randint(100, 999)} Main St, City, State',
                    'admission_date': timezone.now().date() - timedelta(days=random.randint(30, 365)),
                    'status': 'active',
                    'guardian_name': f'{student_data["first_name"]} Parent',
                    'guardian_relation': 'Parent',
                    'guardian_phone': f'+1{random.randint(2000000000, 9999999999)}',
                    'guardian_email': f'parent.{username}@email.com',
                    'class_section': random.choice(classes) if classes else None,
                }
            )
        
        self.stdout.write('Created sample students')

    def create_courses(self):
        teachers = Teacher.objects.all()
        classes = Class.objects.all()
        
        courses_data = [
            {'code': 'MATH101', 'title': 'Algebra I', 'credits': 3},
            {'code': 'MATH102', 'title': 'Geometry', 'credits': 3},
            {'code': 'SCI101', 'title': 'Physics', 'credits': 4},
            {'code': 'SCI102', 'title': 'Chemistry', 'credits': 4},
            {'code': 'ENG101', 'title': 'English Literature', 'credits': 3},
            {'code': 'ENG102', 'title': 'Grammar & Composition', 'credits': 2},
            {'code': 'HIST101', 'title': 'World History', 'credits': 3},
            {'code': 'CS101', 'title': 'Introduction to Programming', 'credits': 4},
            {'code': 'MATH201', 'title': 'Calculus', 'credits': 4},
            {'code': 'SCI201', 'title': 'Advanced Physics', 'credits': 4},
        ]
        
        for course_data in courses_data:
            course, created = Course.objects.get_or_create(
                course_code=course_data['code'],
                defaults={
                    'title': course_data['title'],
                    'description': f'This is a comprehensive course in {course_data["title"]}.',
                    'teacher': random.choice(teachers) if teachers else None,
                    'credits': course_data['credits'],
                    'class_section': random.choice(classes) if classes else None,
                }
            )
            
            # Enroll random students
            students = Student.objects.all()
            if students:
                enrolled_students = random.sample(list(students), min(random.randint(5, 12), len(students)))
                course.students.set(enrolled_students)
        
        self.stdout.write('Created sample courses')

    def create_activities(self):
        courses = Course.objects.all()
        
        activity_types = ['assignment', 'quiz', 'exam', 'project']
        
        for course in courses:
            for i in range(random.randint(2, 5)):
                Activity.objects.get_or_create(
                    title=f'{course.title} {random.choice(activity_types).title()} {i+1}',
                    course=course,
                    defaults={
                        'activity_type': random.choice(activity_types),
                        'due_date': timezone.now() + timedelta(days=random.randint(1, 30)),
                    }
                )
        
        self.stdout.write('Created sample activities')

    def create_attendance(self):
        students = Student.objects.all()
        courses = Course.objects.all()
        
        # Create attendance for the last 30 days
        for days_ago in range(30):
            date = timezone.now().date() - timedelta(days=days_ago)
            
            for student in students:
                for course in student.enrolled_courses.all()[:2]:  # Limit to 2 courses per student
                    status_weights = [('present', 0.85), ('absent', 0.10), ('late', 0.05)]
                    status = random.choices(
                        [s[0] for s in status_weights],
                        weights=[s[1] for s in status_weights]
                    )[0]
                    
                    Attendance.objects.get_or_create(
                        student=student,
                        course=course,
                        date=date,
                        defaults={
                            'status': status,
                            'remarks': 'Auto-generated sample data',
                        }
                    )
        
        self.stdout.write('Created sample attendance records')

    def create_grades(self):
        students = Student.objects.all()
        courses = Course.objects.all()
        
        # Create grades for the last 6 months
        for months_ago in range(6):
            for student in students:
                for course in student.enrolled_courses.all():
                    # Generate realistic grade (70-95)
                    score = random.uniform(70, 95)
                    
                    if score >= 90:
                        grade = 'A'
                    elif score >= 80:
                        grade = 'B'
                    elif score >= 70:
                        grade = 'C'
                    else:
                        grade = 'D'
                    
                    date = timezone.now().date() - timedelta(days=months_ago * 30)
                    
                    Grade.objects.get_or_create(
                        student=student,
                        subject=course,
                        date=date,
                        defaults={
                            'score': round(score, 2),
                            'grade': grade,
                            'remarks': 'Sample grade data',
                        }
                    )
        
        self.stdout.write('Created sample grades')

    def create_payments_invoices(self):
        students = Student.objects.all()
        
        for student in students:
            # Create some invoices
            for i in range(random.randint(1, 3)):
                amount = random.uniform(500, 2000)
                due_date = timezone.now().date() + timedelta(days=random.randint(10, 90))
                
                invoice = Invoice.objects.create(
                    student=student,
                    amount=amount,
                    due_date=due_date,
                    paid=random.choice([True, False]),
                )
                
                # Create payment if invoice is paid
                if invoice.paid:
                    payment = Payment.objects.create(
                        student=student,
                        amount=amount,
                        payment_date=timezone.now() - timedelta(days=random.randint(1, 30)),
                        payment_method=random.choice(['Credit Card', 'Bank Transfer', 'Cash']),
                        status='completed',
                        transaction_id=f'TXN{random.randint(100000, 999999)}',
                    )
                    invoice.payment = payment
                    invoice.save()
        
        self.stdout.write('Created sample payments and invoices')

    def create_events(self):
        event_data = [
            {
                'title': 'Parent-Teacher Meeting',
                'description': 'Monthly parent-teacher conference',
                'event_type': 'meeting',
                'color': '#f1c40f',
                'days_ahead': 15,
            },
            {
                'title': 'Science Fair',
                'description': 'Annual science exhibition',
                'event_type': 'academic',
                'color': '#3498db',
                'days_ahead': 25,
            },
            {
                'title': 'Sports Day',
                'description': 'Inter-school sports competition',
                'event_type': 'sports',
                'color': '#9b59b6',
                'days_ahead': 30,
            },
            {
                'title': 'Cultural Festival',
                'description': 'Annual cultural celebration',
                'event_type': 'cultural',
                'color': '#e67e22',
                'days_ahead': 45,
            },
            {
                'title': 'Mid-term Examinations',
                'description': 'Mid-semester examinations',
                'event_type': 'exam',
                'color': '#e74c3c',
                'days_ahead': 20,
            },
        ]
        
        for event in event_data:
            start_date = timezone.now() + timedelta(days=event['days_ahead'])
            
            Event.objects.get_or_create(
                title=event['title'],
                defaults={
                    'description': event['description'],
                    'start_date': start_date,
                    'end_date': start_date + timedelta(hours=random.randint(2, 8)),
                    'event_type': event['event_type'],
                    'color': event['color'],
                    'location': 'School Campus',
                }
            )
        
        self.stdout.write('Created sample events') 