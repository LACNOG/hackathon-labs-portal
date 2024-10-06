# Generated by Django 4.2.7 on 2024-10-06 00:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0006_notification'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='sent_at',
            new_name='created_at',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='is_sent',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='student',
        ),
        migrations.CreateModel(
            name='NotificationRecipient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent_at', models.DateTimeField(blank=True, null=True)),
                ('is_sent', models.BooleanField(default=False)),
                ('notification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipients', to='portal.notification')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_notifications', to='portal.studentprofile')),
            ],
            options={
                'unique_together': {('notification', 'student')},
            },
        ),
    ]
