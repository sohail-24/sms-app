from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

# Add name validator
name_validator = RegexValidator(
    regex=r'^[a-zA-Z\s]*$',
    message="Name must contain only letters and spaces."
)

class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('graduated', 'Graduated'),
        ('suspended', 'Suspended')
    ]

    # Personal Information
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile', null=True, blank=True)
    student_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50, validators=[name_validator])
    last_name = models.CharField(max_length=50, validators=[name_validator])
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    photo = models.ImageField(upload_to='student_photos/', null=True, blank=True)

    # Contact Information
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    address = models.TextField()

    # Academic Information
    grade_level = models.CharField(max_length=20)
    batch = models.CharField(max_length=20, blank=True, null=True)
    roll_number = models.CharField(max_length=20, blank=True, null=True)
    admission_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Guardian Information
    guardian_name = models.CharField(max_length=100)
    guardian_relation = models.CharField(max_length=50)
    guardian_phone = models.CharField(validators=[phone_regex], max_length=17)
    guardian_email = models.EmailField(blank=True)

    # System Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # New fields
    class_section = models.ForeignKey('Class', on_delete=models.SET_NULL, null=True, related_name='students')
    enrolled_courses = models.ManyToManyField('Course', related_name='enrolled_students')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def is_active(self):
        return self.status == 'active'

    def get_email(self):
        return self.email  # Use the student's email field directly

    def get_attendance_percentage(self):
        total_classes = Attendance.objects.filter(student=self).count()
        present_classes = Attendance.objects.filter(student=self, status='present').count()
        return (present_classes / total_classes * 100) if total_classes > 0 else 0

    def get_performance(self):
        # Calculate performance based on grades
        grades = Grade.objects.filter(student=self)
        
        if grades.exists():
            total_score = sum(grade.score for grade in grades)
            total_possible = grades.count() * 100  # Assuming grades are out of 100
            return (total_score / total_possible * 100) if total_possible > 0 else 0
        
        return 0

class Teacher(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]

    # Personal Information
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile', null=True, blank=True)
    teacher_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50, validators=[name_validator])
    last_name = models.CharField(max_length=50, validators=[name_validator])
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    photo = models.ImageField(upload_to='teacher_photos/', null=True, blank=True)

    # Contact Information
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    # phone_number = models.CharField(validators=[phone_regex], max_length=17)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.CharField(max_length=17, blank=True, null=True)

    # Professional Information
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100, blank=True, null=True)
    subjects = models.TextField()  # Comma-separated list of subjects
    qualification = models.CharField(max_length=200, blank=True)
    specialization = models.CharField(max_length=200, blank=True, null=True)
    experience = models.IntegerField(null=True, blank=True)
    joining_date = models.DateField()
    is_active = models.BooleanField(default=True)

    # System Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.teacher_id})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

class Course(models.Model):
    course_code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='courses')
    credits = models.IntegerField()
    students = models.ManyToManyField(Student, related_name='courses_enrolled', blank=True)
    class_section = models.ForeignKey('Class', on_delete=models.SET_NULL, null=True, related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['course_code']

    def __str__(self):
        return f"{self.course_code} - {self.title}"

    def get_student_count(self):
        return self.students.count()

    def get_activity_count(self):
        return self.activities.count()

    def get_exam_count(self):
        return self.exams.count()

    def is_available_for_enrollment(self):
        """Check if course is available for enrollment"""
        return self.teacher and self.teacher.is_active

    def can_student_enroll(self, student):
        """Check if a specific student can enroll in this course"""
        # Check if student is already enrolled
        if student.enrolled_courses.filter(id=self.id).exists():
            return False
        
        # Check if course is available for enrollment
        if not self.is_available_for_enrollment():
            return False
        
        # Check if course is for student's class section (if specified)
        if self.class_section and student.class_section:
            return self.class_section == student.class_section
        
        return True

    def get_enrolled_student_count(self):
        """Get count of students enrolled in this course"""
        return self.enrolled_students.count()

    def get_progress_for_student(self, student):
        """Calculate progress percentage for a specific student"""
        # This is a placeholder - you can implement actual progress calculation
        # based on completed assignments, attendance, etc.
        return 50  # Default progress for now

class CourseMaterial(models.Model):
    MATERIAL_TYPES = [
        ('lecture_note', 'Lecture Note'),
        ('presentation', 'Presentation'),
        ('worksheet', 'Worksheet'),
        ('textbook', 'Textbook'),
        ('reference', 'Reference Material'),
        ('video', 'Video'),
        ('other', 'Other')
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    material_type = models.CharField(max_length=20, choices=MATERIAL_TYPES)
    file = models.FileField(upload_to='course_materials/%Y/%m/')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Course Material'
        verbose_name_plural = 'Course Materials'

    def __str__(self):
        return f"{self.title} - {self.course.title}"

    def get_file_size(self):
        """Return human-readable file size"""
        size = self.file.size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

    def get_file_extension(self):
        """Return the file extension"""
        return self.file.name.split('.')[-1].lower() if '.' in self.file.name else ''

class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('assignment', 'Assignment'),
        ('quiz', 'Quiz'),
        ('exam', 'Exam'),
        ('project', 'Project')
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    due_date = models.DateTimeField()
    file = models.FileField(upload_to='activities/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.activity_type})"

class Payment(models.Model):
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded')
    ]
    
    PAYMENT_METHODS = [
        ('CASH', 'Cash'),
        ('CREDIT_CARD', 'Credit Card'),
        ('DEBIT_CARD', 'Debit Card'),
        ('NET_BANKING', 'Net Banking'),
        ('UPI', 'UPI'),
        ('CHEQUE', 'Cheque'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField()
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS)
    transaction_id = models.CharField(max_length=100, unique=True)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-payment_date', '-created_at']  # Order by payment date (newest first), then by creation date
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def __str__(self):
        return f"Payment {self.transaction_id} - {self.student.get_full_name()}"

class Invoice(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    paid = models.BooleanField(default=False)
    payment = models.OneToOneField(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Invoice for {self.student.get_full_name()} - {self.amount}"

class Event(models.Model):
    EVENT_TYPES = [
        ('academic', 'Academic'),
        ('exam', 'Examination'),
        ('holiday', 'Holiday'),
        ('meeting', 'Meeting'),
        ('sports', 'Sports'),
        ('cultural', 'Cultural'),
        ('general', 'General'),
    ]

    EVENT_COLORS = [
        ('#3498db', 'Blue - Academic'),
        ('#e74c3c', 'Red - Examinations'),
        ('#2ecc71', 'Green - Holidays'),
        ('#f1c40f', 'Yellow - Meetings'),
        ('#9b59b6', 'Purple - Sports'),
        ('#e67e22', 'Orange - Cultural'),
        ('#34495e', 'Dark Gray - General'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default='general')
    color = models.CharField(max_length=7, choices=EVENT_COLORS, default='#34495e')
    is_all_day = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return self.title

    def get_css_class(self):
        """Return CSS class based on event type"""
        return f"event-type-{self.event_type}"

    def get_color_name(self):
        """Return human-readable color name"""
        color_dict = dict(self.EVENT_COLORS)
        return color_dict.get(self.color, 'Unknown')

class Timetable(models.Model):
    DAY_CHOICES = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday')
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.course.title} - {self.day} ({self.start_time} to {self.end_time})"

class Report(models.Model):
    REPORT_TYPES = [
        ('academic', 'Academic'),
        ('attendance', 'Attendance'),
        ('behavior', 'Behavior')
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    content = models.TextField()
    generated_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.report_type} Report - {self.student.get_full_name()}"

class Examination(models.Model):
    EXAM_TYPES = [
        ('midterm', 'Midterm'),
        ('final', 'Final'),
        ('quiz', 'Quiz'),
        ('assignment', 'Assignment')
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True, blank=True)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPES)
    date = models.DateTimeField()
    duration = models.DurationField()
    total_marks = models.IntegerField()
    instructions = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title or self.exam_type} - {self.course.title}"

class ExamSchedule(models.Model):
    examination = models.ForeignKey(Examination, on_delete=models.CASCADE)
    room = models.CharField(max_length=50)
    supervisor = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Schedule for {self.examination}"

class Settings(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.key

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile for {self.user.username}"

class Notice(models.Model):
    NOTICE_TYPES = [
        ('general', 'General'),
        ('academic', 'Academic'),
        ('event', 'Event'),
        ('holiday', 'Holiday'),
        ('exam', 'Examination'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    notice_type = models.CharField(max_length=20, choices=NOTICE_TYPES, default='general')
    target_audience = models.CharField(max_length=20, choices=[
        ('all', 'All'),
        ('students', 'Students'),
        ('teachers', 'Teachers'),
        ('parents', 'Parents'),
    ], default='all')
    attachment = models.FileField(upload_to='notices/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ])
    remarks = models.TextField(blank=True)
    marked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', 'course']
        unique_together = ['student', 'course', 'date']

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.course.title} - {self.date}"

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username}"

    class Meta:
        ordering = ['-created_at']

class MessageAttachment(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='message_attachments/')
    filename = models.CharField(max_length=255)
    file_size = models.IntegerField()  # Size in bytes
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment: {self.filename} ({self.message})"

    def get_file_size_display(self):
        """Return human-readable file size"""
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

class Announcement(models.Model):
    CATEGORY_CHOICES = [
        ('academic', 'Academic'),
        ('general', 'General'),
        ('events', 'Events'),
    ]
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='announcements')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='academic')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    expiry_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.course.title}"

    class Meta:
        ordering = ['-created_at']

class AnnouncementAttachment(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='announcement_attachments/')
    filename = models.CharField(max_length=255)
    file_size = models.IntegerField()  # Size in bytes
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for {self.announcement.title}"

    def save(self, *args, **kwargs):
        if not self.filename and self.file:
            self.filename = self.file.name
        if not self.file_size and self.file:
            self.file_size = self.file.size
        super().save(*args, **kwargs)

class Class(models.Model):
    name = models.CharField(max_length=100)
    section = models.CharField(max_length=10)
    academic_year = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Classes"
        ordering = ['-academic_year', 'name', 'section']

    def __str__(self):
        return f"{self.name} - Section {self.section} ({self.academic_year})"

    @property
    def full_name(self):
        return f"{self.name} - Section {self.section}"

    def get_student_count(self):
        return self.students.count()

    def get_teacher_count(self):
        return self.teachers.count()

    def get_course_count(self):
        return self.courses.count()

class Schedule(models.Model):
    DAY_CHOICES = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday')
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='schedules')
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['day', 'start_time']
        # Ensure no scheduling conflicts for the same room
        constraints = [
            models.UniqueConstraint(
                fields=['room', 'day', 'start_time', 'end_time'],
                name='unique_room_schedule'
            )
        ]
    
    def __str__(self):
        return f"{self.course.title} - {self.get_day_display()} ({self.start_time.strftime('%I:%M %p')} - {self.end_time.strftime('%I:%M %p')})"
    
    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError('End time must be after start time.')
            
        # Check for schedule conflicts
        conflicts = Schedule.objects.filter(
            day=self.day,
            room=self.room
        ).exclude(id=self.id)
        
        for schedule in conflicts:
            if (self.start_time < schedule.end_time and 
                self.end_time > schedule.start_time):
                raise ValidationError('There is a scheduling conflict with another class in this room.')

class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        ordering = ['name']

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    subject = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='grades')
    examination = models.ForeignKey('Examination', on_delete=models.CASCADE, related_name='grades', null=True, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=2)
    remarks = models.TextField(blank=True, null=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', 'subject']
        verbose_name = 'Grade'
        verbose_name_plural = 'Grades'

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.subject.title} - {self.grade}"

class Behavior(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='behaviors')
    incident_type = models.CharField(max_length=100)
    description = models.TextField()
    severity = models.CharField(max_length=20)
    date = models.DateField()
    action_taken = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Behavior'
        verbose_name_plural = 'Behaviors'

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.incident_type} ({self.date})"

class Fee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fees')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    paid = models.BooleanField(default=False)
    payment_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-due_date']
        verbose_name = 'Fee'
        verbose_name_plural = 'Fees'

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.amount} (Due: {self.due_date})"

class AssignmentSubmission(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='assignment_submissions')
    assignment = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='submissions')
    file = models.FileField(upload_to='assignment_submissions/')
    comments = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'assignment')
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.assignment.title}"

class Evaluation(models.Model):
    RATING_CHOICES = [
        (1, 'Poor'),
        (2, 'Fair'),
        (3, 'Good'),
        (4, 'Very Good'),
        (5, 'Excellent')
    ]
    
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comments = models.TextField(blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Evaluation for {self.teacher.get_full_name()} by {self.student.get_full_name()}"

class Expense(models.Model):
    EXPENSE_TYPES = [
        ('salary', 'Salary'),
        ('maintenance', 'Maintenance'),
        ('supplies', 'Supplies'),
        ('utilities', 'Utilities'),
        ('other', 'Other')
    ]
    
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_type = models.CharField(max_length=20, choices=EXPENSE_TYPES)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)
    date = models.DateField()
    receipt = models.FileField(upload_to='expenses/receipts/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.title} - {self.amount}"
