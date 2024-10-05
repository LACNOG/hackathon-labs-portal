from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('register/', views.student_signup, name='register'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    # path('import-lab-equipment/<int:workshop_id>/', import_lab_equipment, name='import_lab_equipment'),
]