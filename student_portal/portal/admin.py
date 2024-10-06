from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.urls import path
from django.shortcuts import render, redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.contrib import messages
from .models import StudentProfile, Workshop, LabEquipment, Notification, NotificationRecipient
from django import forms
from .admin_views import import_lab_equipment
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.contrib.admin.utils import unquote

class CSVImportForm(forms.Form):
    csv_file = forms.FileField()

class LabEquipmentInline(admin.TabularInline):
    model = LabEquipment
    extra = 1    

class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False
    verbose_name_plural = 'Student Profile'
    # Remove readonly_fields for state to make it editable
    fields = ('student_id', 'lab_equipment', 'state')

class UserAdmin(BaseUserAdmin):
    inlines = (StudentProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'lab_equipment', 'workshop', 'state')
    search_fields = ('user__username', 'student_id', 'lab_equipment__name')
    list_filter = ('lab_equipment__workshop', 'state')
    fields = ('user', 'student_id', 'lab_equipment', 'state')

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

class NotificationForm(forms.ModelForm):
    recipients = forms.ModelMultipleChoiceField(
        queryset=StudentProfile.objects.all(),
        widget=admin.widgets.FilteredSelectMultiple('Recipients', False),
        required=False
    )

    class Meta:
        model = Notification
        fields = ['subject', 'message']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    form = NotificationForm
    list_display = ('subject', 'created_at', 'recipient_count', 'sent_count')
    list_filter = ('created_at',)
    search_fields = ('subject', 'message')
    date_hierarchy = 'created_at'
    actions = ['send_notification']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('add/', self.admin_site.admin_view(self.add_notification), name='portal_notification_add'),
            path('<path:object_id>/change/', self.admin_site.admin_view(self.change_notification), name='portal_notification_change'),
        ]
        return custom_urls + urls

    def add_notification(self, request):
        return self._changeform_view(request, None, '')

    def change_notification(self, request, object_id):
        return self._changeform_view(request, object_id, '')

    def _changeform_view(self, request, object_id, form_url, extra_context=None):
        add = object_id is None
        if add:
            obj = None
        else:
            obj = self.get_object(request, unquote(object_id))

        if request.method == 'POST':
            form = self.get_form(request, obj)(request.POST, instance=obj)
            if form.is_valid():
                notification = form.save()
                recipients = form.cleaned_data['recipients']
                NotificationRecipient.objects.filter(notification=notification).exclude(student__in=recipients).delete()
                for recipient in recipients:
                    NotificationRecipient.objects.get_or_create(notification=notification, student=recipient)
                msg = _('The notification was added successfully.') if add else _('The notification was changed successfully.')
                self.message_user(request, msg, messages.SUCCESS)
                return self.response_post_save_change(request, notification)
        else:
            form = self.get_form(request, obj)(instance=obj)
            if obj:
                form.initial['recipients'] = StudentProfile.objects.filter(received_notifications__notification=obj)

        fieldsets = self.get_fieldsets(request, obj)
        adminForm = admin.helpers.AdminForm(
            form,
            list(fieldsets),
            self.get_prepopulated_fields(request, obj),
            self.get_readonly_fields(request, obj),
            model_admin=self)
        media = self.media + adminForm.media

        context = {
            **self.admin_site.each_context(request),
            'title': (_('Add %s') if add else _('Change %s')) % self.model._meta.verbose_name,
            'adminform': adminForm,
            'object_id': object_id,
            'original': obj,
            'is_popup': False,
            'to_field': None,
            'media': media,
            'inline_admin_formsets': [],
            'errors': admin.helpers.AdminErrorList(form, []),
            'preserved_filters': self.get_preserved_filters(request),
        }

        context.update(extra_context or {})

        return self.render_change_form(request, context, add=add, change=not add, obj=obj, form_url=form_url)

    def recipient_count(self, obj):
        return obj.recipients.count()
    recipient_count.short_description = 'Total Recipients'

    def sent_count(self, obj):
        return obj.recipients.filter(is_sent=True).count()
    sent_count.short_description = 'Sent Count'

    def send_notification(self, request, queryset):
        for notification in queryset:
            recipients = NotificationRecipient.objects.filter(notification=notification, is_sent=False)
            sent_count = 0
            for recipient in recipients:
                try:
                    send_mail(
                        subject=notification.subject,
                        message=notification.message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[recipient.student.user.email],
                        fail_silently=False,
                    )
                    recipient.is_sent = True
                    recipient.sent_at = timezone.now()
                    recipient.save()
                    sent_count += 1
                except Exception as e:
                    self.message_user(request, f"Failed to send email to {recipient.student.user.email}: {str(e)}", level=messages.ERROR)
            
            if sent_count > 0:
                self.message_user(request, f"Sent notification '{notification.subject}' to {sent_count} recipient(s).", level=messages.SUCCESS)
            else:
                self.message_user(request, f"No new recipients for notification '{notification.subject}'.", level=messages.WARNING)

    send_notification.short_description = "Send selected notifications"
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['recipients'].queryset = StudentProfile.objects.all()
        return form

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:  # Only for new notifications
            recipients = form.cleaned_data.get('recipients')
            if recipients:
                for recipient in recipients:
                    NotificationRecipient.objects.create(notification=obj, student=recipient)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        recipients = form.cleaned_data.get('recipients')
        if recipients is not None:
            current_recipients = set(NotificationRecipient.objects.filter(notification=form.instance).values_list('student_id', flat=True))
            new_recipients = set(recipients.values_list('id', flat=True))
            
            # Remove recipients that are no longer selected
            NotificationRecipient.objects.filter(notification=form.instance, student_id__in=current_recipients - new_recipients).delete()
            
            # Add new recipients
            for recipient_id in new_recipients - current_recipients:
                NotificationRecipient.objects.create(notification=form.instance, student_id=recipient_id)