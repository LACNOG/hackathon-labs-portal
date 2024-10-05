from django.shortcuts import render
from .forms import StudentRegistrationForm
from allauth.account.views import SignupView
from .models import StudentProfile, Workshop
from django.urls import reverse
from allauth.account.views import EmailVerificationSentView, ConfirmEmailView
from django.views.generic import TemplateView
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib import messages

from django.views.decorators.debug import sensitive_post_parameters
from django.http import HttpResponseRedirect

from allauth.account.views import LoginView # type: ignore
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    template_name = 'account/login2.html'
    # success_url = reverse_lazy('student_dashboard')  # or whatever your dashboard URL name is

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['page_title'] = 'Log In'  # Add any additional context you need
    #     return context


class CustomConfirmEmailView(ConfirmEmailView):
     # template_name = 'account/email_confirmation.html'
     template_name = 'account/email_confirmation.html'


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

class CustomEmailVerificationSentView(EmailVerificationSentView):
    def get(self, request, *args, **kwargs):
        # Clear any existing messages
        storage = messages.get_messages(request)
        for message in storage:
            # This iteration is necessary to mark the messages as processed
            pass
        storage.used = True

        # Add only the email sent confirmation message
        messages.success(request, f"Confirmation email sent to {request.user.email}.")
        
        return render(request, 'account/email_verification_sent_initial.html', {'messages': messages.get_messages(request)})



class EmailVerificationInstructionsView(TemplateView):
    template_name = 'account/email_verification_instructions.html'

