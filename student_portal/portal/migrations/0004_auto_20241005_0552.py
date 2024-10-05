
from django.db import migrations
from django.conf import settings

def update_default_site(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    Site.objects.update_or_create(
        id=settings.SITE_ID,
        defaults={
            'domain': 'localhost:8000',
            'name': 'localhost'
        }
    )

class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('portal', '0003_remove_studentprofile_lab_group_and_more'),  # replace 'previous_migration' with the name of your last migration
    ]

    operations = [
        migrations.RunPython(update_default_site),
    ]