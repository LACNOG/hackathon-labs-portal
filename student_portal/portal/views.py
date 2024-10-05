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


class CustomConfirmEmailView(ConfirmEmailView):
    template_name = 'account/email_confirmation.html'

    def get_object(self, *args, **kwargs):
        key = kwargs.get('key')
        emailconfirmation = EmailConfirmationHMAC.from_key(key)
        if not emailconfirmation:
            if EmailConfirmation.objects.all_valid().filter(key=key).exists():
                emailconfirmation = EmailConfirmation.objects.all_valid().get(key=key)
                emailconfirmation.confirm(self.request)
            else:
                emailconfirmation = None
        return emailconfirmation

    def get(self, *args, **kwargs):
        self.object = self.get_object(**kwargs)
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['confirmation'] = self.object
        return context


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
        return render(request, 'account/email_verification_sent_initial.html', {'messages': messages.get_messages(request)})
    
class CustomConfirmEmailView(ConfirmEmailView):
    template_name = 'account/email_confirmation.html'

class EmailVerificationInstructionsView(TemplateView):
    template_name = 'account/email_verification_instructions.html'
