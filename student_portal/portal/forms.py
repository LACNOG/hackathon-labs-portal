from django import forms
from allauth.account.forms import SignupForm
from .models import Workshop, StudentProfile

class StudentRegistrationForm(SignupForm):
    name = forms.CharField(max_length=100)
    student_id = forms.CharField(max_length=20)
    workshop = forms.ModelChoiceField(queryset=Workshop.objects.filter(is_open=True))

    def save(self, request):
        user = super(StudentRegistrationForm, self).save(request)
        user.first_name = self.cleaned_data['name']
        user.save()
        StudentProfile.objects.create(
            user=user,
            student_id=self.cleaned_data['student_id'],
            lab_equipment=self.cleaned_data['workshop'].lab_equipments.first()
        )
        return user