from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count
from .models import Hospital, Department, Doctor, Patient, Bed, Slot, Appointment, Bloodbank
from .forms import RegisterForm, AppointmentForm, BloodSearchForm, BedSearchForm



def get_user_role(user):
    if user.is_staff or user.is_superuser:
        return 'admin'
    try:
        Doctor.objects.get(user=user)
        return 'doctor'
    except Doctor.DoesNotExist:
        pass
    try:
        Patient.objects.get(user=user)
        return 'patient'
    except Patient.DoesNotExist:
        pass
    return 'unknown'


def home(request):
    total_hospitals = Hospital.objects.count()
    available_beds = Bed.objects.filter(allocated_to__isnull=True).count()
    total_doctors = Doctor.objects.count()
    is_doctor = False
    is_patient = False
    if request.user.is_authenticated:
        is_doctor = Doctor.objects.filter(user=request.user).exists()
        is_patient = Patient.objects.filter(user=request.user).exists()

    return render(request, 'core/home.html', {
        'total_hospitals': total_hospitals,
        'available_beds': available_beds,
        'total_doctors': total_doctors,
        'is_doctor': is_doctor,
        'is_patient': is_patient,
    })


def hospitals(request):
    q = request.GET.get('q', '').strip()
    hospitals_qs = Hospital.objects.all()
    if q:
        hospitals_qs = hospitals_qs.filter(name__icontains=q)

    hospitals_data = []
    for h in hospitals_qs:
        total_beds = Bed.objects.filter(department__hospital=h).count()
        available_beds = Bed.objects.filter(department__hospital=h, allocated_to__isnull=True).count()
        hospitals_data.append({
            'obj': h,
            'total_beds': total_beds,
            'available_beds': available_beds,
        })

    return render(request, 'core/hospitals.html', {
        'hospitals_data': hospitals_data,
        'query': q,
    })

def hospital_detail(request, pk):
    hospital = get_object_or_404(Hospital, pk=pk)
    departments = Department.objects.filter(hospital=hospital)
    doctors = Doctor.objects.filter(department__hospital=hospital).select_related('user', 'department')

    beds_by_dept = []
    for dept in departments:
        beds = Bed.objects.filter(department=dept)
        beds_by_dept.append({
            'dept': dept,
            'total': beds.count(),
            'available': beds.filter(allocated_to__isnull=True).count(),
            'beds': beds,
        })

    bloodbank = Bloodbank.objects.filter(hospital=hospital)

    return render(request, 'core/hospital_detail.html', {
        'hospital': hospital,
        'departments': departments,
        'doctors': doctors,
        'beds_by_dept': beds_by_dept,
        'bloodbank': bloodbank,
    })

def bed_availability(request):
    form = BedSearchForm(request.GET or None)
    beds_qs = Bed.objects.filter(allocated_to__isnull=True).select_related('department__hospital', 'under')

    bed_type = request.GET.get('bed_type', '').strip()
    hospital_name = request.GET.get('hospital_name', '').strip()

    if bed_type:
        beds_qs = beds_qs.filter(bed_type=bed_type)
    if hospital_name:
        beds_qs = beds_qs.filter(department__hospital__name__icontains=hospital_name)

    summary = {}
    for bed in Bed.objects.select_related('department__hospital'):
        h = bed.department.hospital
        if h.id not in summary:
            summary[h.id] = {'hospital': h, 'total': 0, 'available': 0}
        summary[h.id]['total'] += 1
        if bed.allocated_to is None:
            summary[h.id]['available'] += 1

    return render(request, 'core/bed_availability.html', {
        'form': form,
        'beds': beds_qs,
        'summary': summary.values(),
        'bed_type': bed_type,
        'hospital_name': hospital_name,
    })

def blood_search(request):
    form = BloodSearchForm(request.GET or None)
    results = None
    blood_group = request.GET.get('blood_group', '').strip()
    city = request.GET.get('city', '').strip()

    if blood_group or city:
        results = Bloodbank.objects.filter(units_available__gt=0).select_related('hospital')
        if blood_group:
            results = results.filter(bld_grps=blood_group)
        if city:
            results = results.filter(hospital__address__icontains=city)

    return render(request, 'core/blood_search.html', {
        'form': form,
        'results': results,
        'blood_group': blood_group,
    })


@login_required(login_url='/login/')
def book_appointment(request):
    try:
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        messages.error(request, 'Patient profile not found. Please contact admin.')
        return redirect('home')

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appt = form.save(commit=False)
            appt.patient = patient
            appt.status = 'PENDING'
            appt.save()
            messages.success(request, f'Appointment booked with Dr. {appt.doctor}! Status: Pending confirmation.')
            return redirect('my_appointments')
    else:
        form = AppointmentForm()

    doctors = Doctor.objects.all().select_related('user', 'department__hospital')
    return render(request, 'core/book_appointment.html', {
        'form': form,
        'doctors': doctors,
    })


@login_required(login_url='/login/')
def my_appointments(request):
    try:
        patient = Patient.objects.get(user=request.user)
        appointments = Appointment.objects.filter(patient=patient).select_related(
            'doctor__user', 'doctor__department__hospital'
        ).order_by('-slot')
    except Patient.DoesNotExist:
        appointments = []
    return render(request, 'core/my_appointments.html', {'appointments': appointments})


@login_required(login_url='/login/')
def dashboard(request):
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Staff only.')
        return redirect('home')

    total_hospitals = Hospital.objects.count()
    total_patients = Patient.objects.count()
    total_doctors = Doctor.objects.count()
    total_beds = Bed.objects.count()
    available_beds = Bed.objects.filter(allocated_to__isnull=True).count()
    pending_appointments = Appointment.objects.filter(status='PENDING').count()
    recent_appointments = Appointment.objects.select_related(
        'patient__user', 'doctor__user'
    ).order_by('-created_at')[:10]

    blood_summary = Bloodbank.objects.values('bld_grps').annotate(
        total_units=Sum('units_available')
    ).order_by('bld_grps')

    return render(request, 'core/dashboard.html', {
        'total_hospitals': total_hospitals,
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'total_beds': total_beds,
        'available_beds': available_beds,
        'pending_appointments': pending_appointments,
        'recent_appointments': recent_appointments,
        'blood_summary': blood_summary,
    })

@login_required(login_url='/login/')
def manage_appointments(request):
    if not request.user.is_staff:
        return redirect('home')

    appointments = Appointment.objects.all().select_related(
        'patient__user', 'doctor__user', 'doctor__department__hospital'
    ).order_by('-created_at')

    if request.method == 'POST':
        appt_id = request.POST.get('appt_id')
        action = request.POST.get('action')
        appt = get_object_or_404(Appointment, pk=appt_id)
        if action == 'confirm':
            appt.status = 'CONFIRMED'
            messages.success(request, f'Appointment #{appt_id} confirmed.')
        elif action == 'cancel':
            appt.status = 'CANCELLED'
            messages.warning(request, f'Appointment #{appt_id} cancelled.')
        elif action == 'complete':
            appt.status = 'COMPLETED'
            messages.success(request, f'Appointment #{appt_id} marked complete.')
        appt.save()
        return redirect('manage_appointments')

    return render(request, 'core/manage_appointments.html', {'appointments': appointments})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            phone = form.cleaned_data.get('phone', '')
            Patient.objects.create(user=user, phone=phone)
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name}! Account created.')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            role = get_user_role(user)
            if role == 'admin':
                return redirect('dashboard')
            elif role == 'doctor':
                return redirect('home')   
            else:
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')