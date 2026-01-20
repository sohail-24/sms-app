from .models import Student, Teacher, Course

def dashboard_stats(request):
    """
    Context processor to provide dashboard statistics to all templates
    """
    if request.user.is_authenticated:
        return {
            'sidebar_total_students': Student.objects.filter(status='active').count(),
            'sidebar_total_teachers': Teacher.objects.filter(is_active=True).count(),
            'sidebar_active_courses': Course.objects.count(),
        }
    return {
        'sidebar_total_students': 0,
        'sidebar_total_teachers': 0,
        'sidebar_active_courses': 0,
    } 