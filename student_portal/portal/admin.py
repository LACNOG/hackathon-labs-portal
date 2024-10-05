from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.urls import path
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.contrib import messages
from .models import StudentProfile, Workshop, LabEquipment
from django import forms
from .admin_views import import_lab_equipment

class CSVImportForm(forms.Form):
    csv_file = forms.FileField()

class LabEquipmentInline(admin.TabularInline):
    model = LabEquipment
    extra = 1    

class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False
    verbose_name_plural = 'Student Profile'

class UserAdmin(BaseUserAdmin):
    inlines = (StudentProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'lab_equipment', 'workshop')
    search_fields = ('user__username', 'student_id', 'lab_equipment__name')
    list_filter = ('lab_equipment__workshop',)

    def workshop(self, obj):
        return obj.workshop
    workshop.short_description = 'Workshop'

@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ('name', 'opening_date', 'is_open', 'is_registration_open')
    search_fields = ('name',)
    list_filter = ('is_open', 'opening_date')
    inlines = [LabEquipmentInline]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/<int:workshop_id>/', self.admin_site.admin_view(import_lab_equipment), name='workshop_import_csv'),
        ]
        return custom_urls + urls

    def import_csv_action(self, request, queryset):
        if len(queryset) != 1:
            self.message_user(request, "Please select one workshop", level=messages.WARNING)
            return
        
        workshop = queryset.first()
        return redirect('admin:workshop_import_csv', workshop_id=workshop.id)
    
    import_csv_action.short_description = "Import Lab Equipment from CSV"

    actions = [import_csv_action]

@admin.register(LabEquipment)
class LabEquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'workshop')
    search_fields = ('name', 'workshop__name')
    list_filter = ('workshop',)