"""
Run with: python manage.py shell < seed_data.py
Seeds the database with demo hospitals, departments, blood bank, beds, doctors.
"""
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import Hospital, Department, Doctor, Patient, Bed, Slot, Bloodbank

User = get_user_model()

print("🌱 Seeding demo data...")

# ── Superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@medicare.com', 'admin123')
    print("✅ Superuser: admin / admin123")

# ── Hospitals
h1, _ = Hospital.objects.get_or_create(name='City General Hospital',  defaults={'address': 'Salt Lake, Kolkata', 'phone': '033-2222-1111'})
h2, _ = Hospital.objects.get_or_create(name='Apollo Multi-Specialty',  defaults={'address': 'EM Bypass, Kolkata', 'phone': '033-3333-2222'})
h3, _ = Hospital.objects.get_or_create(name='SSKM Government Hospital', defaults={'address': 'AJC Bose Road, Kolkata', 'phone': '033-4444-3333'})
print("✅ 3 hospitals created")

# ── Departments
depts_data = [
    (h1, 'EMERGENCY'), (h1, 'HEART'), (h1, 'ORTHO'), (h1, 'GENERAL'),
    (h2, 'CHEST'), (h2, 'HEART'), (h2, 'NEURO'), (h2, 'PEDIATRIC'),
    (h3, 'EMERGENCY'), (h3, 'GENERAL'), (h3, 'ORTHO'),
]
depts = []
for hosp, name in depts_data:
    d, _ = Department.objects.get_or_create(hospital=hosp, name=name)
    depts.append(d)
print(f"✅ {len(depts)} departments created")

# ── Doctors
doctors_data = [
    ('dr_sharma',   'Rajesh',   'Sharma',   depts[1],  'MBBS, MD Cardiology', 12, 20),
    ('dr_gupta',    'Priya',    'Gupta',    depts[2],  'MBBS, MS Ortho',      8,  15),
    ('dr_das',      'Subrata',  'Das',      depts[3],  'MBBS, MD General',    5,  10),
    ('dr_mukherjee','Tanmoy',   'Mukherjee',depts[5],  'MBBS, DM Cardiology', 15, 25),
    ('dr_banerjee', 'Rina',     'Banerjee', depts[6],  'MBBS, DM Neurology',  10, 20),
    ('dr_roy',      'Sanjay',   'Roy',      depts[7],  'MBBS, DCH Pediatrics',7,  15),
    ('dr_khan',     'Imran',    'Khan',     depts[0],  'MBBS, Emergency Med', 6,  10),
]
for uname, first, last, dept, qual, exp, dur in doctors_data:
    if not User.objects.filter(username=uname).exists():
        u = User.objects.create_user(uname, f'{uname}@medicare.com', 'doc123', first_name=first, last_name=last)
        Doctor.objects.get_or_create(user=u, department=dept, defaults={'qualification': qual, 'experience_years': exp, 'opd_duration': dur})
print("✅ 7 doctors created (password: doc123)")

# ── Beds
bed_types = ['GENERAL_BED', 'ICU_BED', 'CABIN_BED', 'VENTILATOR_BED']
for dept in depts:
    for bt in bed_types[:2]:
        for _ in range(3):
            Bed.objects.get_or_create(department=dept, bed_type=bt, allocated_to=None, under=None)
print("✅ Beds added")

# ── Blood Bank
blood_groups = ['A+','A-','B+','B-','O+','O-','AB+','AB-']
for hospital in [h1, h2, h3]:
    for bg in blood_groups:
        import random
        Bloodbank.objects.get_or_create(hospital=hospital, bld_grps=bg, defaults={'units_available': random.randint(0, 15)})
print("✅ Blood bank seeded")

# ── Demo Patient
if not User.objects.filter(username='patient1').exists():
    pu = User.objects.create_user('patient1', 'patient@medicare.com', 'patient123', first_name='Debraj', last_name='Demo')
    Patient.objects.create(user=pu, phone='9876543210', blood_group='O+')
    print("✅ Demo patient: patient1 / patient123")

print("\n🎉 Done! Run: python manage.py runserver")
print("   Admin:   http://127.0.0.1:8000/admin/   → admin / admin123")
print("   Patient: http://127.0.0.1:8000/login/   → patient1 / patient123")
