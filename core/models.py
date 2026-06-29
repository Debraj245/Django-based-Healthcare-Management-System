from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

User = get_user_model()


class Hospital(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    display = models.ImageField(upload_to='hospitals/', blank=True, null=True)

    def __str__(self):
        return self.name

    def available_beds_count(self):
        return Bed.objects.filter(department__hospital=self, allocated_to__isnull=True).count()

    def total_beds_count(self):
        return Bed.objects.filter(department__hospital=self).count()


class Department(models.Model):
    DEPARTMENT_CHOICES = [
        ('EMERGENCY', 'Emergency'),
        ('CHEST', 'Chest'),
        ('HEART', 'Heart'),
        ('ORTHO', 'Orthopedic'),
        ('GENERAL', 'General'),
        ('NEURO', 'Neurology'),
        ('PEDIATRIC', 'Pediatric'),
    ]
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)

    def __str__(self):
        return f"{self.get_name_display()} - {self.hospital.name}"


class Doctor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    opd_duration = models.PositiveIntegerField(help_text="OPD duration in minutes")
    qualification = models.CharField(max_length=100, blank=True, null=True)
    experience_years = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Dr. {self.user.get_full_name() or self.user.username}"

    def hospital(self):
        return self.department.hospital


class Patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    blood_group = models.CharField(max_length=5, blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Bed(models.Model):
    BED_TYPE_CHOICES = [
        ("GENERAL_BED", "General Bed"),
        ("ICU_BED", "ICU Bed"),
        ("CABIN_BED", "Cabin Bed"),
        ("VENTILATOR_BED", "Ventilator Bed"),
    ]
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    bed_type = models.CharField(choices=BED_TYPE_CHOICES, max_length=20)
    allocated_to = models.ForeignKey(Patient, on_delete=models.SET_NULL, blank=True, null=True)
    under = models.ForeignKey(Doctor, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.get_bed_type_display()} - {self.department}"

    def is_available(self):
        return self.allocated_to is None


class Slot(models.Model):
    DAYS_CHOICES = [
        ('MONDAY', 'Monday'),
        ('TUESDAY', 'Tuesday'),
        ('WEDNESDAY', 'Wednesday'),
        ('THURSDAY', 'Thursday'),
        ('FRIDAY', 'Friday'),
        ('SATURDAY', 'Saturday'),
        ('SUNDAY', 'Sunday'),
    ]
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    days = models.CharField(max_length=10, choices=DAYS_CHOICES, blank=True, null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"Dr. {self.doctor} - {self.days} {self.start_time}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed'),
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=True, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, blank=True, null=True)
    slot = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.patient} -> Dr. {self.doctor} on {self.slot.strftime('%d %b %Y %H:%M')}"


class Bloodbank(models.Model):
    BLOOD_GRP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ]
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    bld_grps = models.CharField(max_length=5, choices=BLOOD_GRP_CHOICES)
    units_available = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.bld_grps} at {self.hospital.name} - {self.units_available} units"
