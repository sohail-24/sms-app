from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .models import Student, Teacher, Course, Activity, Payment, Invoice, Grade, Behavior, Fee, Class, Attendance, Event, Schedule, Examination, ExamSchedule

class StudentRegistrationForm(UserCreationForm):
    student_id = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    gender = forms.ChoiceField(choices=Student.GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    photo = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(max_length=17, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}))
    grade_level = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    admission_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    guardian_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    guardian_relation = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    guardian_phone = forms.CharField(max_length=17, widget=forms.TextInput(attrs={'class': 'form-control'}))
    guardian_email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            student = Student.objects.create(
                user=user,
                student_id=self.cleaned_data['student_id'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                date_of_birth=self.cleaned_data['date_of_birth'],
                gender=self.cleaned_data['gender'],
                photo=self.cleaned_data['photo'],
                email=self.cleaned_data['email'],
                phone_number=self.cleaned_data['phone_number'],
                address=self.cleaned_data['address'],
                grade_level=self.cleaned_data['grade_level'],
                admission_date=self.cleaned_data['admission_date'],
                guardian_name=self.cleaned_data['guardian_name'],
                guardian_relation=self.cleaned_data['guardian_relation'],
                guardian_phone=self.cleaned_data['guardian_phone'],
                guardian_email=self.cleaned_data['guardian_email']
            )
        return user

class TeacherRegistrationForm(UserCreationForm):
    teacher_id = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    gender = forms.ChoiceField(choices=Teacher.GENDER_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    photo = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(max_length=17, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}))
    department = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    subjects = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}))
    qualification = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    joining_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Add user to teacher group
            teacher_group = Group.objects.get_or_create(name='Teacher')[0]
            user.groups.add(teacher_group)
            
            teacher = Teacher.objects.create(
                user=user,
                teacher_id=self.cleaned_data['teacher_id'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                date_of_birth=self.cleaned_data.get('date_of_birth'),
                gender=self.cleaned_data.get('gender'),
                photo=self.cleaned_data.get('photo'),
                email=self.cleaned_data['email'],
                phone_number=self.cleaned_data.get('phone_number', ''),
                address=self.cleaned_data.get('address', ''),
                department=self.cleaned_data['department'],
                subjects=self.cleaned_data['subjects'],
                qualification=self.cleaned_data.get('qualification', ''),
                joining_date=self.cleaned_data['joining_date']
            )
        return user

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'student_id', 'first_name', 'last_name', 'date_of_birth', 
            'gender', 'photo', 'email', 'phone_number', 'address', 
            'grade_level', 'admission_date', 'status', 'guardian_name', 
            'guardian_relation', 'guardian_phone', 'guardian_email'
        ]
        widgets = {
            'student_id': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'grade_level': forms.TextInput(attrs={'class': 'form-control'}),
            'admission_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'guardian_name': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_relation': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_email': forms.EmailInput(attrs={'class': 'form-control'})
        }

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['teacher_id', 'first_name', 'last_name', 'email', 'phone_number',
                 'department', 'date_of_birth', 'gender', 'qualification', 'address', 'photo']
        widgets = {
            'teacher_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Teacher ID'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email Address'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Department'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Qualification'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Enter Address'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'})
        }

    def clean_teacher_id(self):
        teacher_id = self.cleaned_data.get('teacher_id')
        if teacher_id:
            # Check if another teacher with this ID exists (excluding current instance)
            existing_teacher = Teacher.objects.filter(teacher_id=teacher_id).exclude(pk=self.instance.pk if self.instance else None)
            if existing_teacher.exists():
                raise forms.ValidationError('A teacher with this ID already exists.')
        return teacher_id

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_code', 'title', 'description', 'teacher', 'credits']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_code', 'title', 'description', 'teacher', 'credits']

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'photo', 'phone_number', 'address',
            'guardian_name', 'guardian_relation', 'guardian_phone', 'guardian_email'
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'date_of_birth',
            'gender',
            'address',
            'department',
            'qualification',
            'photo'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')]),
        }

class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['title', 'description', 'file']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'file': forms.FileInput(attrs={'class': 'form-control'})
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['student', 'amount', 'payment_method', 'payment_date', 'remarks']
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['student', 'amount', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'student': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = Student.objects.all().order_by('first_name', 'last_name')

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'subject', 'score', 'grade', 'remarks', 'date']

class BehaviorForm(forms.ModelForm):
    class Meta:
        model = Behavior
        fields = ['student', 'incident_type', 'description', 'severity', 'date', 'action_taken']

class FeeForm(forms.ModelForm):
    class Meta:
        model = Fee
        fields = ['student', 'amount', 'due_date', 'paid', 'payment_date', 'description']

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name', 'section', 'academic_year']

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'course', 'date', 'status', 'remarks', 'marked_by'] 

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_date', 'end_date', 'event_type', 'location', 'is_all_day', 'color']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'event_type': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'is_all_day': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'color': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial color based on event type if creating new event
        if not self.instance.pk and self.initial.get('event_type'):
            color_map = {
                'academic': '#3498db',
                'exam': '#e74c3c',
                'holiday': '#2ecc71',
                'meeting': '#f1c40f',
                'sports': '#9b59b6',
                'cultural': '#e67e22',
                'general': '#34495e'
            }
            self.initial['color'] = color_map.get(self.initial['event_type'], '#34495e')
    
    def save(self, commit=True):
        event = super().save(commit=False)
        # Set color based on event type if color is not selected
        if not event.color and event.event_type:
            color_map = {
                'academic': '#3498db',
                'exam': '#e74c3c',
                'holiday': '#2ecc71',
                'meeting': '#f1c40f',
                'sports': '#9b59b6',
                'cultural': '#e67e22',
                'general': '#34495e'
            }
            event.color = color_map.get(event.event_type, '#34495e')
        
        if commit:
            event.save()
        return event

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['course', 'day', 'start_time', 'end_time', 'room']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
            'day': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'room': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Room 101, Lab 201'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes and helpful labels
        self.fields['course'].queryset = Course.objects.all().order_by('title')
        self.fields['course'].empty_label = "Select Course/Subject"
        self.fields['day'].empty_label = "Select Day"
        
        # Add some common room options
        self.fields['room'].widget.attrs['list'] = 'room-suggestions'
    
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        day = cleaned_data.get('day')
        room = cleaned_data.get('room')
        course = cleaned_data.get('course')
        
        if start_time and end_time:
            if start_time >= end_time:
                raise forms.ValidationError('End time must be after start time.')
        
        # Check for schedule conflicts in the same room
        if day and room and start_time and end_time:
            conflicts = Schedule.objects.filter(
                day=day,
                room=room,
                start_time__lt=end_time,
                end_time__gt=start_time
            )
            
            # Exclude current instance if editing
            if self.instance.pk:
                conflicts = conflicts.exclude(pk=self.instance.pk)
            
            if conflicts.exists():
                raise forms.ValidationError(f'There is a scheduling conflict in {room} on {day}.')
        
        # Check for teacher conflicts (same teacher teaching different courses at same time)
        if course and day and start_time and end_time:
            teacher_conflicts = Schedule.objects.filter(
                course__teacher=course.teacher,
                day=day,
                start_time__lt=end_time,
                end_time__gt=start_time
            )
            
            # Exclude current instance if editing
            if self.instance.pk:
                teacher_conflicts = teacher_conflicts.exclude(pk=self.instance.pk)
            
            if teacher_conflicts.exists():
                raise forms.ValidationError(f'{course.teacher} is already scheduled to teach another class at this time.')
        
        return cleaned_data

class ExaminationForm(forms.ModelForm):
    class Meta:
        model = Examination
        fields = ['course', 'title', 'exam_type', 'date', 'duration', 'total_marks', 'instructions']
        widgets = {
            'course': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter exam title (e.g., Mathematics Midterm)',
                'required': True
            }),
            'exam_type': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'required': True
            }),
            'duration': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'HH:MM:SS (e.g., 02:00:00 for 2 hours)',
                'pattern': r'^\d{2}:\d{2}:\d{2}$',
                'title': 'Format: HH:MM:SS',
                'required': True
            }),
            'total_marks': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '1000',
                'placeholder': 'Enter total marks',
                'required': True
            }),
            'instructions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter exam instructions (optional)'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter courses to only show active courses
        self.fields['course'].queryset = Course.objects.filter(
            teacher__is_active=True
        ).order_by('course_code')
        
        # Set empty labels for better UX
        self.fields['course'].empty_label = "Select Course/Subject"
        self.fields['exam_type'].empty_label = "Select Exam Type"

class ExamScheduleForm(forms.ModelForm):
    class Meta:
        model = ExamSchedule
        fields = ['room', 'supervisor', 'start_time', 'end_time']
        widgets = {
            'room': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter room number/name',
                'list': 'room-suggestions',
                'required': True
            }),
            'supervisor': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'start_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'required': True
            }),
            'end_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'required': True
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter supervisors to only show active teachers
        self.fields['supervisor'].queryset = Teacher.objects.filter(
            is_active=True
        ).order_by('first_name', 'last_name')
        self.fields['supervisor'].empty_label = "Select Supervisor"

class StudentPasswordChangeForm(forms.Form):
    password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )
    password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")
        if p1 or p2:
            if p1 != p2:
                raise forms.ValidationError("Passwords do not match.")
            if not p1:
                raise forms.ValidationError("Password cannot be empty if changing.")
        return cleaned_data 