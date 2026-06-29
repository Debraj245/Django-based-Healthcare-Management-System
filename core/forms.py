from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Appointment, Patient

User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    phone = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'slot', 'notes']
        widgets = {
            'slot': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Any notes for the doctor...'}),
        }


class BloodSearchForm(forms.Form):
    BLOOD_GRP_CHOICES = [('', 'Select Blood Group')] + [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ]
    blood_group = forms.ChoiceField(choices=BLOOD_GRP_CHOICES, required=False)
    city = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'City or area...'}))


class BedSearchForm(forms.Form):
    BED_TYPE_CHOICES = [('', 'All Types'),
        ("GENERAL_BED", "General Bed"),
        ("ICU_BED", "ICU Bed"),
        ("CABIN_BED", "Cabin Bed"),
        ("VENTILATOR_BED", "Ventilator Bed"),
    ]
    bed_type = forms.ChoiceField(choices=BED_TYPE_CHOICES, required=False)
    hospital_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Hospital name...'}))
