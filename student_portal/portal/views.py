from django.shortcuts import render
from .forms import StudentRegistrationForm
from allauth.account.views import SignupView
from .models import StudentProfile, Workshop

class StudentSignupView(SignupView):
    template_name = 'registration/register.html'
    form_class = StudentRegistrationForm

student_signup = StudentSignupView.as_view()

def student_dashboard(request):
    return render(request, "portal/student_dashboard.html")

def landing_page(request):
    open_workshops = Workshop.objects.filter(is_open=True)
    context = {
        'open_workshops': open_workshops
    }
    return render(request, "portal/landing_page.html", context)