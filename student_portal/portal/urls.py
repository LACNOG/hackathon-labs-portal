from django.urls import path, re_path, include
# from .views import CustomConfirmEmailView, CustomEmailVerificationSentView
from . import views
from .views import CustomLoginView, CustomConfirmEmailView, student_dashboard, landing_page, student_signup



urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('register/', views.student_signup, name='register'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    
    path('accounts/login/', CustomLoginView.as_view(), name='account_login'),
    path('accounts/email-verification-instructions/', views.EmailVerificationInstructionsView.as_view(), name='email_verification_instructions'),

    path('accounts/confirm-email/', views.EmailVerificationInstructionsView.as_view(), name='email_verification_instructions'),
    # re_path(r'^accounts/confirm-email/(?P<key>[-:\w]+)/$', views.CustomConfirmEmailView.as_view(), name='account_confirm_email'),
    path('accounts/confirm-email/<str:key>/', views.CustomConfirmEmailView.as_view(), name='account_confirm_email'),
    
    path('accounts/', include('allauth.urls')),    
]       
 