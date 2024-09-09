from django.contrib import admin
from django.urls import path
from home.views import *
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     # path('',home,name='home' ),
#     path('', login_user, name='dashboard'),

#     path('diagnostic/', diagnostic_view, name='diagnostic'),
#     path('doctors/', doctor_view, name='doctors'),
#     path('login/', login_user, name='login'),
#     path('logout/', custom_logout, name='logout'),
#     path('dashboard/', dashboard_view, name='dashboard'),

# ]
urlpatterns = [
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    path('login/', login_user, name='login'),  # Assuming this is the login page
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
   
   
    path('diagnostic/',login_required( diagnostic_view), name='diagnostic'),
    path('dashboard/', login_required(dashboard_view), name='dashboard'),
    path('doctors/', login_required(doctor_view), name='doctors'),
 
    path('logout/', custom_logout, name='logout'),
    path('adddoctor/',login_required(add_doctor_view),name='adddoctor'),
     path('deletedoctor/<int:doctor_id>/',login_required(delete_doctor_view),name='deletedoctor'),
    path('adddiagnostic/', login_required(add_diagnostic_view),name='adddiagnostic'),
    path('viewallpatients/', login_required(view_all_patients),name='viewallpatients'),
    path('patientlist/',login_required(patient_list_view),name='patientlist'),
    path('testfungus/<int:diagnostic_id>/', login_required(test_fungus_view), name='testfungus'),
    path('diagnosefungus/<int:diagnostic_id>/',login_required(diagnose_fungus_view), name='diagnosefungus'),
    path('pdfreport/<int:diagnostic_id>/', login_required(pdf_generate_view), name='pdfreport'),
    path('generate_pdf/<int:diagnostic_id>/', login_required(generate_pdf), name='generate_pdf'),

   
]