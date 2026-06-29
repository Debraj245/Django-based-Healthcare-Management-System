# 🏥 MediCare — Setup & Run Guide

## Quick Start

```bash
# 1. Install dependencies
pip install django pillow

# 2. Apply migrations
python manage.py migrate

# 3. Run the server
python manage.py runserver
```

## Login Credentials

| Role    | Username   | Password     | URL                          |
|---------|------------|--------------|------------------------------|
| Admin   | `admin`    | `admin123`   | http://127.0.0.1:8000/admin/ |
| Patient | `patient1` | `patient123` | http://127.0.0.1:8000/login/ |

## Pages

| Page               | URL                          | Access   |
|--------------------|------------------------------|----------|
| Home               | `/`                          | Public   |
| Hospitals List     | `/hospitals/`                | Public   |
| Hospital Detail    | `/hospitals/<id>/`           | Public   |
| Bed Availability   | `/beds/`                     | Public   |
| Blood Search       | `/blood/`                    | Public   |
| Book Appointment   | `/appointments/book/`        | Login    |
| My Appointments    | `/appointments/my/`          | Login    |
| Admin Dashboard    | `/dashboard/`                | Staff    |
| Manage Appointments| `/appointments/manage/`      | Staff    |
| Django Admin       | `/admin/`                    | Superuser|

## Project Structure

```
healthcare/
├── core/
│   ├── models.py          # Hospital, Department, Doctor, Patient, Bed, Slot, Appointment, Bloodbank
│   ├── views.py           # All views (home, hospitals, beds, blood, appointments, auth, dashboard)
│   ├── urls.py            # All URL routes
│   ├── forms.py           # RegisterForm, AppointmentForm, BloodSearchForm, BedSearchForm
│   ├── admin.py           # Full admin configuration
│   ├── templates/core/
│   │   ├── base.html              # Navbar, footer, messages
│   │   ├── home.html              # Landing page with stats
│   │   ├── hospitals.html         # Hospital list with search
│   │   ├── hospital_detail.html   # Beds, blood bank, doctors per hospital
│   │   ├── bed_availability.html  # Filter + available beds table
│   │   ├── blood_search.html      # Blood group search + quick-select pills
│   │   ├── book_appointment.html  # OPD booking form
│   │   ├── my_appointments.html   # Patient's appointment history
│   │   ├── dashboard.html         # Staff dashboard with stats + charts
│   │   ├── manage_appointments.html # Confirm/Cancel/Complete appointments
│   │   ├── login.html             # Login page
│   │   └── register.html          # Registration page
│   └── templatetags/
│       └── custom_filters.py      # subtract, split filters
├── static/styles/
│   ├── style.css          # Original homepage CSS
│   └── extra.css          # All additional component CSS
└── seed_data.py           # Demo data seeder

# 🏥 MediCare — Healthcare Management System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.x-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/Django_REST_Framework-3.x-ff1709?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**A full-stack healthcare management web application built with Django.**  
Manage hospitals, doctors, OPD appointments, bed availability, and blood bank — all in one platform.

[Features](#-features) · [Tech Stack](#-tech-stack) · [Installation](#-installation) · [API Docs](#-rest-api) · [Screenshots](#-project-structure)

</div>

---

## 📌 Overview

MediCare is a role-based healthcare management system that allows **patients** to book OPD appointments, search for blood availability, and check real-time bed status across multiple hospitals. **Staff/Admin** can manage appointments, view dashboards, and control hospital data.

Built as a portfolio project targeting campus placements, it demonstrates full-stack Django development, REST API design, role-based authentication, and production deployment practices.

---

## ✨ Features

### 🔐 Authentication & Roles
- Register / Login / Logout with Django's built-in auth
- **3 role types** — Admin, Doctor, Patient — automatically detected from linked profiles
- Role-based redirects after login (Admin → Dashboard, Patient → Home)
- Protected views with `@login_required`

### 🏥 Hospital Management
- Browse all hospitals with real-time bed counts
- Search hospitals by name
- View hospital detail — departments, doctors, beds, blood bank

### 🛏️ Bed Availability
- Real-time available bed count per hospital
- Filter by bed type: General, ICU, Cabin, Ventilator
- Filter by hospital name
- Summary table per hospital

### 🩸 Blood Bank
- Search blood group availability across all hospitals
- Quick-select blood group pills (A+, A-, B+, B-, O+, O-, AB+, AB-)
- Filter by hospital and city
- Shows units available per hospital

### 🩺 OPD Appointments
- Patients can book appointments with any doctor
- Select doctor, slot, and add notes
- Real-time status tracking: Pending → Confirmed → Completed / Cancelled
- Staff can manage all appointments from a dedicated panel

### 📊 Admin Dashboard
- Total stats — hospitals, doctors, patients, beds
- Pending appointment count
- Blood summary across all groups
- Recent appointments table

### 🌐 REST API
- Full CRUD API using Django REST Framework
- Token-free Session + Basic auth
- Paginated responses
- Browsable API UI built-in

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11, Django 5.x |
| API | Django REST Framework 3.x |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Frontend | HTML5, CSS3, Vanilla JS |
| Static Files | WhiteNoise |
| Deployment | Railway / Render |
| Config | python-decouple, dj-database-url |
| Server | Gunicorn |

---

## 📁 Project Structure

```

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Debraj245/HealthCare.git
cd HealthCare/healthcare
```

### 2. Create & Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the `healthcare/` folder:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

> Generate a secret key:
> ```bash
> python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
> ```

### 5. Apply Migrations

```bash
python manage.py migrate
```

### 6. Seed Demo Data

```bash
python seed_data.py
```

This creates:
- 3 hospitals (City General, Apollo, SSKM)
- 11 departments
- 7 doctors
- Blood bank data for all 8 blood groups
- Beds across all departments
- Demo admin and patient accounts

### 7. Run the Server

```bash
python manage.py runserver
```

Open → [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🔑 Demo Credentials

| Role | Username | Password | Access |
|------|----------|----------|--------|
| Admin | `admin` | `admin123` | Full dashboard + Django admin |
| Patient | `patient1` | `patient123` | Book appointments, search |
| Doctor | `dr_sharma` | `doc123` | View appointments |
| Doctor | `dr_gupta` | `doc123` | View appointments |

Django Admin Panel → [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🌐 REST API

Base URL: `/api/`

### Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/hospitals/` | List all hospitals with bed counts | No |
| GET | `/api/hospitals/<id>/` | Hospital detail with departments | No |
| GET | `/api/doctors/` | List all doctors | No |
| GET | `/api/doctors/?hospital=1` | Filter doctors by hospital | No |
| GET | `/api/beds/` | Available beds only | No |
| GET | `/api/beds/?type=ICU_BED` | Filter by bed type | No |
| GET | `/api/blood/` | Blood availability | No |
| GET | `/api/blood/?group=O%2B` | Filter by blood group | No |
| GET | `/api/appointments/` | Patient's own appointments | ✅ Yes |
| POST | `/api/appointments/` | Book a new appointment | ✅ Yes |
| GET | `/api/appointments/<id>/` | Appointment detail | ✅ Yes |
| GET | `/api/stats/` | Admin dashboard stats | ✅ Admin only |

### Sample Response — `/api/hospitals/`

```json
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "City General Hospital",
            "address": "Salt Lake, Kolkata",
            "phone": "033-2222-1111",
            "total_beds": 24,
            "available_beds": 18,
            "departments": [
                { "id": 1, "name": "EMERGENCY" },
                { "id": 2, "name": "HEART" }
            ]
        }
    ]
}
```

### Browsable API

DRF provides a built-in browser UI. Just open any `/api/` URL in your browser after logging in — no extra tools needed.

---

## 🚀 Deployment (Railway)

### 1. Push to GitHub

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### 2. Deploy on Railway

1. Go to [railway.app](https://railway.app) → Sign up with GitHub
2. Click **New Project** → **Deploy from GitHub repo**
3. Select this repository
4. Add a **PostgreSQL** database plugin

### 3. Set Environment Variables on Railway

```env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourapp.railway.app
DATABASE_URL=<auto-set by Railway PostgreSQL plugin>
```

### 4. Run Migrations on Railway

In Railway terminal:
```bash
python manage.py migrate
python seed_data.py
```

---

## 🗄️ Data Models

```
Hospital ──< Department ──< Doctor
    │              │
    │              └──< Bed
    │
    └──< Bloodbank

Patient ──< Appointment >── Doctor
                │
               Slot
```

| Model | Key Fields |
|-------|-----------|
| `Hospital` | name, address, phone, display |
| `Department` | hospital, name (choices) |
| `Doctor` | user, department, qualification, experience_years, opd_duration |
| `Patient` | user, phone, blood_group, date_of_birth |
| `Bed` | department, bed_type, allocated_to, under |
| `Slot` | doctor, date_time |
| `Appointment` | patient, doctor, slot, status, notes |
| `Bloodbank` | hospital, bld_grps, units_available |

---

## 📄 Pages

| Page | URL | Access |
|------|-----|--------|
| Home | `/` | Public |
| Hospitals | `/hospitals/` | Public |
| Hospital Detail | `/hospitals/<id>/` | Public |
| Bed Availability | `/beds/` | Public |
| Blood Search | `/blood/` | Public |
| Book Appointment | `/appointments/book/` | Login |
| My Appointments | `/appointments/my/` | Login |
| Dashboard | `/dashboard/` | Staff |
| Manage Appointments | `/appointments/manage/` | Staff |
| Login | `/login/` | Public |
| Register | `/register/` | Public |
| Django Admin | `/admin/` | Superuser |

---

## 👨‍💻 Author

**Debraj Ganguly**  
B.Tech Computer Science & Engineering (AI/ML)  
Kolkata, India

[![GitHub](https://img.shields.io/badge/GitHub-Debraj245-181717?style=flat&logo=github)](https://github.com/Debraj245)

---

## 📝 License

This project is licensed under the MIT License.
