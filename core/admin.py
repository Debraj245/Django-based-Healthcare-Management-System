from django.contrib import admin
from .models import Hospital, Department, Doctor, Patient, Bed, Slot, Appointment, Bloodbank


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'phone']
    search_fields = ['name', 'address']


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'hospital']
    list_filter = ['hospital', 'name']


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'department', 'qualification', 'experience_years', 'opd_duration']
    list_filter = ['department__hospital', 'department']
    search_fields = ['user__first_name', 'user__last_name', 'user__username']


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'phone', 'blood_group', 'date_of_birth']
    search_fields = ['user__first_name', 'user__last_name', 'user__username']


@admin.register(Bed)
class BedAdmin(admin.ModelAdmin):
    list_display = ['bed_type', 'department', 'allocated_to', 'under', 'is_available']
    list_filter = ['bed_type', 'department__hospital', 'department']


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'days', 'start_time', 'end_time']
    list_filter = ['doctor', 'days']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'slot', 'status', 'created_at']
    list_filter = ['status', 'doctor__department__hospital']
    search_fields = ['patient__user__username', 'doctor__user__username']


@admin.register(Bloodbank)
class BloodbankAdmin(admin.ModelAdmin):
    list_display = ['hospital', 'bld_grps', 'units_available']
    list_filter = ['bld_grps', 'hospital']
