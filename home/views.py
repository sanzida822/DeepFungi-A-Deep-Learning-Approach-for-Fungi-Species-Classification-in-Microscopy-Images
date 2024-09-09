from django.shortcuts import render,redirect
from django.http  import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth import logout
from .models import *
from datetime import datetime,timedelta
from django.db import IntegrityError
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import tensorflow as tf
import io

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO




import numpy as np
# Create your views her


def dashboard_view(request):
    total_report = Diagnostic.objects.count()
    total_doctor=Doctor.objects.count()
    context={
        'total_report':total_report,
        'total_doctor':total_doctor
    }

    return render(request, 'dashboard.html',context)

def  test_fungus_view(request, diagnostic_id):
    patient_diagnostic=Diagnostic.objects.get(id=diagnostic_id)
    doctor_name=patient_diagnostic.doctor.name
    
    # if request.method=='POST':



    context={
        'patient_diagnostic':patient_diagnostic,
        'doctor_name':doctor_name,
    }
    return render(request, 'test_fungus.html', context)
    



# Load the model once to avoid loading it every time a request is made
model = load_model('../mblnet_ef_inc6.h5')

class_info = {
    0: {'name': 'BASH', 'description': 'Description for class 1'},
    1: {'name': 'BBH', 'description': 'Description for class 2'},
    2: {'name': 'GMA', 'description': 'Description for class 3'},
    3: {'name': 'SHC', 'description': 'Description for class 4'},
    4: {'name': 'TSH', 'description': 'Description for class 5'},
}

def diagnose_fungus_view(request, diagnostic_id):
    patient_diagnostic = Diagnostic.objects.get(id=diagnostic_id)
    doctor_name = patient_diagnostic.doctor.name

    if request.method == 'POST' and request.FILES.get('fungus_image'):
        try:
            # Read and preprocess the image file
            image_file = request.FILES['fungus_image']
            image = Image.open(image_file)
            image = image.resize((224, 224))  
            image_array = np.array(image) 
            image_array = np.expand_dims(image_array, axis=0)
            # Make prediction
            predictions = model.predict(image_array)
            predicted_class = np.argmax(predictions, axis=1)[0]
            result = class_info.get(predicted_class, {'name': 'Unknown', 'description': 'No description available'})
        except Exception as e:
            print(f"Error: {e}")
            result = {'name': 'Error', 'description': str(e)}
            
        Report.objects.create(
            diagnostic_id=diagnostic_id,
            status='Complete',
            species=result.get('name', 'Unknown'),
            description=result.get('description', 'No description available'),

        )
        context = {
            'patient_diagnostic': patient_diagnostic,
            'doctor_name': doctor_name,
            'result': result
        }
    else:
        context = {
            'patient_diagnostic': patient_diagnostic,
            'doctor_name': doctor_name,
        }

    return render(request, 'report_generation.html', context)



def pdf_generate_view(request,diagnostic_id):
    patient_diagnostic=Diagnostic.objects.get(id=diagnostic_id)
    doctor_name=patient_diagnostic.doctor.name
    context={
        'patient_diagnostic':patient_diagnostic,
        'doctor_name':doctor_name,
    }
    return render(request, 'pdf_template.html',context)

# pdf

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.CreatePDF(BytesIO(html.encode('utf-8')), dest=result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def generate_pdf(request, diagnostic_id):
    # Fetch diagnostic object (assuming you have a model named Diagnostic)
    patient_diagnostic = get_object_or_404(Diagnostic, id=diagnostic_id)
    patient_report = Report.objects.filter(diagnostic_id=diagnostic_id).first()

    context = {
        'patient_diagnostic': patient_diagnostic,
        'patient_report': patient_report,

    }
    
    diagnostic = get_object_or_404(Diagnostic, id=diagnostic_id)   
    diagnostic.status = "Complete"
    diagnostic.total_cost = diagnostic.total_cost
    diagnostic.payment=diagnostic.total_cost
    diagnostic.due='0'

    diagnostic.save()
    return render_to_pdf('pdf_template.html', context)

def view_all_patients(request):
    all_patients = Diagnostic.objects.all()
    context={
        'all_patients':all_patients,
    }
    return render(request, 'view_patients.html', context)

def diagnostic_view(request): 
    doctors=Doctor.objects.all()
    latest_diagnostic = Diagnostic.objects.latest('id')

    latest_diagnostic_id = latest_diagnostic.id
    today_date = datetime.today()
    current_date_upper = today_date.strftime('%d %b %Y')  # e.g., '08 Aug 2024'
    current_time = datetime.now().strftime("%H:%M:%S")  # e.g., '14:30:45'

    today_date = datetime.today()
    current_date_lower = today_date.strftime('%Y-%m-%d')
  

 # future date
    future_date = today_date + timedelta(days=2)
    
    # Format the future date as 'YYYY-MM-DD'
    future_date_format = future_date.strftime('%Y-%m-%d')
   
    context={
          'current_date_upper':current_date_upper,
          'current_date_lower':current_date_lower,
          'future_date_format':future_date_format,
          'current_time':current_time,
          'doctors':doctors,
          'latest_id': latest_diagnostic_id+1

    }
    return render(request, 'diagnostic.html',context)
   


def doctor_view(request):
    doctors=Doctor.objects.all()
    return render(request, 'doctor.html',{'doctors': doctors})

def add_doctor_view(request):
    if request.method == "POST":
        data = request.POST
        try:
            Doctor.objects.create(
                name=data.get('name'),
                gender=data.get('gender'),
                hospital=data.get('hospital'),
                department=data.get('department'),
                mobile=data.get('mobile'),
                email=data.get('email'),
            )
            messages.success(request, 'Doctor added successfully!')
        except IntegrityError:
            messages.error(request, 'A doctor with this email already exists.')
        return redirect('doctors')

def delete_doctor_view(request, doctor_id):
    if request.method == 'POST':
        doctor = get_object_or_404(Doctor, id=doctor_id)
        doctor.delete()
        messages.success(request, 'Doctor record deleted successfully!')
        return redirect('doctors')




def login_user(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(f"Email: {email}, Password: {password}")  # Debugging print
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid email or password")
            return redirect('login')
    return render(request, 'login.html')



def custom_logout(request):
    logout(request)
    return redirect('login')


def add_diagnostic_view(request):
    if request.method=="POST":


        try:
            total_cost = Decimal(request.POST.get('total_cost', '0'))
            payment = Decimal(request.POST.get('payment', '0'))
            net_balance = Decimal(request.POST.get('net_balance', '0'))
            print(request.POST.get('name'),
             request.POST.get('mobile'),
               request.POST.get('gender'),
              request.POST.get('doctor_id'),
              request.POST.get('sample_date'),
               request.POST.get('sample_time'),
              request.POST.get('report_date'),
              request.POST.get('report_time'),
               request.POST.get('total'),
               request.POST.get('payment'),
            request.POST.get('net_balance'),)
            Diagnostic.objects.create(
                patient_name=request.POST.get('name'),
                mobile=request.POST.get('mobile'),
                gender= request.POST.get('gender'),
                age=request.POST.get('age'),
                doctor_id= request.POST.get('doctor_id'),
                sample_date= request.POST.get('sample_date'),
                sample_time= request.POST.get('sample_time'),
                report_date= request.POST.get('report_date'),
                report_time= request.POST.get('report_time'),
                total_cost= request.POST.get('total_cost'),
                payment= request.POST.get('payment'),
                due= request.POST.get('net_balance'),
                status='Pending',
            )
            messages.success(request, 'Record added successfully!')
        except Exception as e:
            print(f'Error: {e}')  # Print the exception message for debugging
            messages.error(request, 'Record not added')
        return redirect('diagnostic')
    


def patient_list_view(request):
    selected_date = request.GET.get('date')  # Get the date from the request

    # Initialize empty lists
    pending_patients = []
    complete_patients = []

    if selected_date:
        try:
            date = datetime.strptime(selected_date, '%Y-%m-%d').date()  # Parse the selected date
            pending_patients = Diagnostic.objects.filter(status='Pending', sample_date=date)
            complete_patients = Diagnostic.objects.filter(status='Complete', sample_date=date)
        except ValueError:
            messages.error(request, 'Please provide a correct date format.')
    else:

        pending_patients = Diagnostic.objects.filter(status='Pending')
        complete_patients = Diagnostic.objects.filter(status='Complete')

    context = {
        'pending_patients': pending_patients,
        'complete_patients': complete_patients,
        'selected_date': selected_date,
        'initial_view': True if not selected_date else False,  # Determine if this is the initial view
    }

    return render(request, 'view_patients.html', context)






