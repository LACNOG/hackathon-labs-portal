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

from allauth.account.views import LoginView, LogoutView # type: ignore
from django.urls import reverse_lazy

import logging

logger = logging.getLogger(__name__)

class CustomLogoutView(LogoutView):
    template_name = 'account/logout2.html'  # Use logout2.html instead of logout.html
    success_url = reverse_lazy('landing_page')  # or whatever your home page URL name is

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Log Out'
        return context

class CustomLoginView(LoginView):
    template_name = 'account/login2.html'
    # success_url = reverse_lazy('student_dashboard')  # or whatever your dashboard URL name is

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['page_title'] = 'Log In'  # Add any additional context you need
    #     return context

from django.shortcuts import render, redirect
from django.contrib import messages
from allauth.account.views import ConfirmEmailView
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from django.http import HttpResponseBadRequest
import logging

logger = logging.getLogger(__name__)

class CustomConfirmEmailView(ConfirmEmailView):
    template_name = 'account/email_confirmation.html'

    def get_object(self, *args, **kwargs) -> EmailConfirmation | None:
        key = kwargs.get('key')
        if not key:
            return None

        try:
            emailconfirmation = EmailConfirmationHMAC.from_key(key)
            if emailconfirmation:
                return emailconfirmation
        except Exception as e:
            logger.error(f"Error in HMAC confirmation: {str(e)}")

        try:
            queryset = EmailConfirmation.objects.all_valid()
            emailconfirmation = queryset.get(key=key)
            return emailconfirmation
        except EmailConfirmation.DoesNotExist:
            logger.warning(f"No valid confirmation found for key: {key}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in email confirmation: {str(e)}")
            return None

    def get(self, *args, **kwargs):
        self.object = self.get_object(**kwargs)
        if self.object is None:
            return HttpResponseBadRequest("Invalid or expired confirmation link.")
        context = self.get_context_data()
        return self.render_to_response(context)

    def post(self, *args, **kwargs):
        self.object = self.get_object(**kwargs)
        if self.object is None:
            return HttpResponseBadRequest("Invalid or expired confirmation link.")
        
        try:
            self.object.confirm(self.request)
        except Exception as e:
            logger.error(f"Error confirming email: {str(e)}")
            messages.error(self.request, "An error occurred while confirming your email. Please try again.")
            return redirect('account_email')

        messages.success(self.request, "Your email has been confirmed.")
        return redirect('account_email')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['confirmation'] = self.object
        return context

# class CustomConfirmEmailView(ConfirmEmailView):
#      # template_name = 'account/email_confirmation.html'
#      template_name = 'account/email_confirmation.html'


class StudentSignupView(SignupView):
    template_name = 'registration/register.html'
    form_class = StudentRegistrationForm

student_signup = StudentSignupView.as_view()

def student_dashboard(request):
    student_profile = StudentProfile.objects.get(user=request.user)
    context = {
        'student_profile': student_profile,
        'show_lab_info': student_profile.state == StudentProfile.State.ASSIGNED,
    }
    return render(request, "portal/student_dashboard.html", context)

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

