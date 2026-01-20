from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Teacher, Student, Class
from datetime import date


class Command(BaseCommand):
    help = "Create demo admin/teacher/student accounts for screenshots"

    def handle(self, *args, **options):
        # Admin
        admin_username = "admin_manual"
        admin_password = "AdminPass123!"
        admin_email = "admin_manual@example.com"

        user, created = User.objects.get_or_create(
            username=admin_username,
            defaults={
                "email": admin_email,
                "first_name": "Admin",
                "last_name": "Manual",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if created:
            user.set_password(admin_password)
            user.save()
            self.stdout.write(self.style.SUCCESS("Created admin user 'admin_manual'"))
        else:
            self.stdout.write("Admin user already exists")

        # Ensure a class exists for student linkage
        class_obj, _ = Class.objects.get_or_create(
            name="Demo Class", section="A", academic_year="2025-26"
        )

        # Teacher
        if not Teacher.objects.filter(teacher_id="TCH_MANUAL").exists():
            teacher_user = User.objects.create_user(
                username="teacher_manual",
                password="TeacherPass123!",
                email="teacher_manual@example.com",
                first_name="Teacher",
                last_name="Manual",
            )
            Teacher.objects.create(
                user=teacher_user,
                teacher_id="TCH_MANUAL",
                first_name="Teacher",
                last_name="Manual",
                email="teacher_manual@example.com",
                department="Mathematics",
                subjects="Algebra, Geometry",
                joining_date=date.today(),
            )
            self.stdout.write(self.style.SUCCESS("Created demo teacher 'TCH_MANUAL'"))
        else:
            self.stdout.write("Demo teacher already exists")

        # Student
        if not Student.objects.filter(student_id="STD_MANUAL").exists():
            student_user = User.objects.create_user(
                username="student_manual",
                password="StudentPass123!",
                email="student_manual@example.com",
                first_name="Student",
                last_name="Manual",
            )
            Student.objects.create(
                user=student_user,
                student_id="STD_MANUAL",
                first_name="Student",
                last_name="Manual",
                date_of_birth=date(2010, 1, 1),
                gender="M",
                email="student_manual@example.com",
                phone_number="+12345678901",
                address="123 Demo St",
                grade_level="10",
                admission_date=date.today(),
                guardian_name="Guardian Manual",
                guardian_relation="Parent",
                guardian_phone="+12345678901",
                class_section=class_obj,
            )
            self.stdout.write(self.style.SUCCESS("Created demo student 'STD_MANUAL'"))
        else:
            self.stdout.write("Demo student already exists")

        self.stdout.write(self.style.SUCCESS("Demo accounts are ready."))


