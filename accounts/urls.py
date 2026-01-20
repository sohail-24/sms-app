from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('', views.index_view, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard URLs
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # Student Management
    path('students/', views.students_view, name='students'),
    path('students/add/', views.add_student_view, name='add_student'),
    path('students/<int:id>/', views.student_detail_view, name='student_detail'),
    path('students/<int:id>/edit/', views.edit_student_view, name='edit_student'),
    path('students/<int:id>/delete/', views.delete_student_view, name='delete_student'),
    
    # Teacher Management
    path('teachers/', views.teachers_view, name='teachers'),
    path('teachers/add/', views.add_teacher_view, name='add_teacher'),
    path('teachers/<int:id>/', views.teacher_detail_view, name='teacher_detail'),
    path('teachers/<int:id>/edit/', views.edit_teacher_view, name='edit_teacher'),
    path('teachers/<int:id>/delete/', views.delete_teacher_view, name='delete_teacher'),
    
    # Course Management
    path('courses/', views.courses_view, name='courses'),
    path('courses/add/', views.add_course_view, name='add_course'),
    path('courses/<int:id>/', views.course_detail_view, name='course_detail'),
    path('courses/<int:id>/edit/', views.edit_course_view, name='edit_course'),
    path('courses/<int:id>/delete/', views.delete_course_view, name='delete_course'),
    
    # Finance Management
    path('finance/fees/', views.fee_payment_view, name='fee_payment'),
    path('finance/invoices/', views.invoices_view, name='invoices'),
    path('fee-payment/', views.fee_payment_view, name='fee_payment'),
    path('fee-payment/<int:payment_id>/view/', views.view_payment_details, name='view_payment_details'),
    path('fee-payment/<int:payment_id>/print/', views.print_payment_receipt, name='print_payment_receipt'),
    path('invoices/', views.invoices_view, name='invoices'),
    path('invoices/<int:invoice_id>/view/', views.view_invoice_details, name='view_invoice_details'),
    path('invoices/<int:invoice_id>/print/', views.print_invoice, name='print_invoice'),
    path('invoices/<int:invoice_id>/delete/', views.delete_invoice, name='delete_invoice'),
    
    # Schedule Management
    path('calendar/', views.calendar_view, name='calendar'),
    path('calendar/events/', views.calendar_events_api, name='calendar_events_api'),
    path('calendar/events/<int:event_id>/', views.event_detail_api, name='event_detail_api'),
    path('timetable/', views.timetable_view, name='timetable'),
    path('timetable/print/', views.timetable_print, name='timetable_print'),
    path('timetable/export/pdf/', views.export_timetable_pdf, name='export_timetable_pdf'),
    path('timetable/export/excel/', views.export_timetable_excel, name='export_timetable_excel'),
    
    # Academic Management
    path('reports/', views.reports_view, name='reports'),
    path('examinations/', views.examinations_view, name='examinations'),
    path('exams/schedule/', views.exam_schedule_view, name='exam_schedule'),
    path('examinations/<int:exam_id>/', views.exam_detail_view, name='exam_detail'),
    path('examinations/<int:exam_id>/edit/', views.exam_edit_view, name='exam_edit'),
    path('examinations/<int:exam_id>/delete/', views.exam_delete_view, name='exam_delete'),
    
    # Settings and Profile
    path('settings/', views.settings_view, name='settings'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('profile/picture/update/', views.update_profile_picture, name='update_profile_picture'),
    
    # Password Reset URLs
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-code/', views.verify_code, name='verify_code'),
    path('reset-password/', views.reset_password, name='reset_password'),
    
    # Student Dashboard URLs
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('student/profile/', views.student_profile, name='student_profile'),
    path('student/profile/update/', views.student_profile_update, name='student_profile_update'),
    path('student/profile/picture/update/', views.student_profile_picture_update, name='student_profile_picture_update'),
    path('student/academic/update/', views.student_academic_update, name='student_academic_update'),
    path('student/courses/', views.student_courses, name='student_courses'),
    path('student/courses/enroll/<int:course_id>/', views.student_enroll_course, name='student_enroll_course'),
    path('student/courses/<int:course_id>/', views.student_course_detail, name='student_course_detail'),
    path('student/timetable/', views.student_timetable, name='student_timetable'),
    path('student/timetable/data/', views.student_timetable_data, name='student_timetable_data'),
    path('student/assignments/', views.student_assignments, name='student_assignments'),
    path('student/assignments/<int:assignment_id>/', views.student_assignment_detail, name='student_assignment_detail'),
    path('student/assignments/<int:assignment_id>/submit/', views.student_submit_assignment, name='student_submit_assignment'),
    path('student/exams/', views.student_exams, name='student_exams'),
    path('student/attendance/', views.student_attendance, name='student_attendance'),
    path('student/fees/', views.student_fees, name='student_fees'),
    path('student/fees/make-payment/', views.student_make_payment, name='student_make_payment'),
    path('student/fees/download-receipt/', views.student_download_receipt, name='student_download_receipt'),
    path('student/notices/', views.student_notices, name='student_notices'),
    
    # Teacher Dashboard URLs
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/profile/', views.teacher_profile, name='teacher_profile'),
    path('teacher/profile/edit/', views.teacher_profile_edit, name='teacher_profile_edit'),
    path('teacher/profile/update/', views.teacher_profile_update, name='teacher_profile_update'),
    path('teacher/profile/picture/update/', views.teacher_profile_picture_update, name='teacher_profile_picture_update'),
    path('teacher/courses/', views.teacher_courses, name='teacher_courses'),
    path('teacher/courses/create/', views.teacher_create_course, name='teacher_create_course'),
    path('teacher/schedule/add-class/', views.teacher_add_schedule_class, name='teacher_add_schedule_class'),
    path('teacher/classes/create/', views.teacher_create_class, name='teacher_create_class'),
    path('teacher/course/<int:id>/', views.teacher_course_detail_view, name='teacher_course_detail'),
    path('teacher/course/<int:course_id>/edit/', views.teacher_edit_course, name='teacher_edit_course'),
    path('teacher/course/<int:course_id>/delete/', views.teacher_delete_course, name='teacher_delete_course'),
    path('teacher/students/', views.teacher_students, name='teacher_students'),
    path('teacher/students/<int:student_id>/', views.teacher_student_detail, name='teacher_student_detail'),
    path('teacher/students/<int:student_id>/attendance/', views.teacher_student_attendance, name='teacher_student_attendance'),
    path('teacher/students/<int:student_id>/grades/', views.teacher_student_grades, name='teacher_student_grades'),
    path('teacher/students/export/', views.teacher_export_students, name='teacher_export_students'),
    path('teacher/timetable/', views.teacher_timetable, name='teacher_timetable'),
    path('teacher/attendance/', views.teacher_attendance_index, name='teacher_attendance'),
    path('teacher/attendance/history/', views.teacher_attendance, name='teacher_attendance_history'),
    path('teacher/attendance/select/', views.teacher_attendance_select, name='teacher_attendance_select'),
    path('teacher/attendance/take/<int:course_id>/', views.teacher_take_attendance, name='teacher_take_attendance'),
    path('teacher/assignments/', views.teacher_assignments, name='teacher_assignments'),
    path('teacher/assignments/create/', views.teacher_create_assignment, name='teacher_create_assignment'),
    path('teacher/assignments/<int:assignment_id>/edit/', views.teacher_edit_assignment, name='teacher_edit_assignment'),
    path('teacher/exams/', views.teacher_exams, name='teacher_exams'),
    path('teacher/exams/create/', views.teacher_create_exam, name='teacher_create_exam'),
    path('teacher/exams/<int:exam_id>/', views.teacher_exam_detail, name='teacher_exam_detail'),
    path('teacher/exams/<int:exam_id>/edit/', views.teacher_exam_edit, name='teacher_exam_edit'),
    path('teacher/exams/<int:exam_id>/delete/', views.teacher_exam_delete, name='teacher_exam_delete'),
    path('teacher/grades/', views.teacher_grades, name='teacher_grades'),
    path('teacher/course/<int:course_id>/students/', views.teacher_course_students, name='teacher_course_students'),
    path('teacher/course/<int:course_id>/assignments/', views.teacher_course_assignments, name='teacher_course_assignments'),
    path('teacher/course/<int:course_id>/grades/', views.teacher_course_grades, name='teacher_course_grades'),
    path('teacher/course/<int:course_id>/grades/<int:student_id>/update/', views.teacher_update_grades, name='teacher_update_grades'),
    path('teacher/grades/<int:grade_id>/student/<int:student_id>/edit/', views.teacher_edit_grade, name='teacher_edit_grade'),
    path('teacher/grades/<int:grade_id>/student/<int:student_id>/delete/', views.teacher_delete_grade, name='teacher_delete_grade'),
    path('teacher/student/<int:student_id>/grades-data/', views.teacher_student_grades_data, name='teacher_student_grades_data'),
    
    # Teacher Communication URLs
    path('teacher/messages/', views.teacher_messages, name='teacher_messages'),
    path('teacher/messages/compose/', views.teacher_compose_message, name='teacher_compose_message'),
    path('teacher/messages/send/', views.teacher_send_message, name='teacher_send_message'),
    path('teacher/announcements/', views.teacher_announcements, name='teacher_announcements'),
    path('teacher/announcements/create/', views.teacher_create_announcement, name='teacher_create_announcement'),
    path('teacher/announcements/<int:announcement_id>/edit/', views.teacher_edit_announcement, name='teacher_edit_announcement'),
    path('teacher/announcements/<int:announcement_id>/delete/', views.teacher_delete_announcement, name='teacher_delete_announcement'),
    
    # Report Generation URLs
    path('reports/student/', views.generate_student_report, name='generate_student_report'),
    path('reports/teacher/', views.generate_teacher_report, name='generate_teacher_report'),
    path('reports/academic/', views.generate_academic_report, name='generate_academic_report'),
    path('reports/financial/', views.generate_financial_report, name='generate_financial_report'),
    path('teacher/assignments/<int:assignment_id>/', views.teacher_assignment_detail, name='teacher_assignment_detail'),
    path('teacher/assignments/<int:assignment_id>/delete/', views.teacher_delete_assignment, name='teacher_delete_assignment'),
    path('teacher/assignments/<int:assignment_id>/submissions/', views.teacher_assignment_submissions, name='teacher_assignment_submissions'),
    path('teacher/assignments/<int:assignment_id>/submissions/<int:submission_id>/view/', views.teacher_view_submission, name='teacher_view_submission'),
    path('teacher/assignments/<int:assignment_id>/submissions/<int:submission_id>/grade/', views.teacher_grade_submission, name='teacher_grade_submission'),
    
    # Course Materials URLs
    path('teacher/course-materials/', views.teacher_course_materials, name='teacher_course_materials'),
    path('teacher/course-materials/upload/', views.teacher_upload_material, name='teacher_upload_material'),
    path('teacher/course-materials/<int:material_id>/delete/', views.teacher_delete_material, name='teacher_delete_material'),
    
    # Student Course Materials
    path('student/course-materials/', views.student_course_materials, name='student_course_materials'),
    
    # User Manual (print/PDF)
    path('manual/', views.user_manual, name='user_manual'),
] 