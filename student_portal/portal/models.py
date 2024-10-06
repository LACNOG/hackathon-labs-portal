from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import csv
from io import StringIO
from django.core.exceptions import ValidationError

class Workshop(models.Model):
    name: models.CharField = models.CharField(max_length=100)
    description: models.TextField = models.TextField()
    opening_date: models.DateTimeField = models.DateTimeField()
    is_open: models.BooleanField = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name

    @property
    def is_registration_open(self) -> bool:
        return self.is_open and self.opening_date <= timezone.now()

    def import_lab_equipment(self, csv_file: StringIO) -> int:
        reader = csv.DictReader(csv_file)
        count = 0
        for row in reader:
            if 'name' in row and 'password' in row:
                LabEquipment.objects.create(
                    workshop=self,
                    name=row['name'],
                    password=row['password']
                )
                count += 1
        return count

class LabEquipment(models.Model):
    workshop: models.ForeignKey = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name='lab_equipments')
    name: models.CharField = models.CharField(max_length=100)
    password: models.CharField = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.name} - {self.workshop.name}"

class StudentProfile(models.Model):
    class State(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        ASSIGNED = 'Assigned', 'Assigned'
        REJECTED = 'Rejected', 'Rejected'

    user: models.OneToOneField = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id: models.CharField = models.CharField(max_length=20, unique=True)
    lab_equipment: models.ForeignKey = models.ForeignKey(LabEquipment, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    state: models.CharField = models.CharField(
        max_length=10,
        choices=State.choices,
        default=State.PENDING,
    )

    def __str__(self) -> str:
        return f"{self.user.username} - {self.student_id} - {self.state}"

    @property
    def workshop(self) -> Workshop:
        return self.lab_equipment.workshop if self.lab_equipment else None

    def clean(self):
        if self.state not in [choice[0] for choice in self.State.choices]:
            raise ValidationError({'state': 'Invalid state value'})