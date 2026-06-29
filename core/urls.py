from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('hospitals/', views.hospitals, name='hospitals'),
    path('hospitals/<int:pk>/', views.hospital_detail, name='hospital_detail'),
    path('beds/', views.bed_availability, name='bed_availability'),
    path('blood/', views.blood_search, name='blood_search'),
    path('appointments/book/', views.book_appointment, name='book_appointment'),
    path('appointments/my/', views.my_appointments, name='my_appointments'),
    path('appointments/manage/', views.manage_appointments, name='manage_appointments'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
