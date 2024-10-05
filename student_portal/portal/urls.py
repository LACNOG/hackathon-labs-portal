from django.urls import path, re_path, include
from .views import CustomConfirmEmailView, CustomEmailVerificationSentView
from . import views


urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('register/', views.student_signup, name='register'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    # path('import-lab-equipment/<int:workshop_id>/', import_lab_equipment, name='import_lab_equipment'),

    path('accounts/email-verification-sent/', views.CustomEmailVerificationSentView.as_view(), name='account_email_verification_sent'),
    path('accounts/email-verification-instructions/', views.EmailVerificationInstructionsView.as_view(), name='email_verification_instructions'),
    re_path(r'^accounts/confirm-email/(?P<key>[-:\w]+)/$', views.CustomConfirmEmailView.as_view(), name='account_confirm_email'),
    path('accounts/', include('allauth.urls')),    
]       
 