from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Course, registered_students, booking_students, register_3freeday, user_profile, Page, PageLock
from django.contrib import messages
from datetime import timedelta
from django.utils import timezone
from django.template.loader import render_to_string
from xhtml2pdf import pisa

def home1(request):
    course = Course.objects.all()
    contact_info = {
        'email1': 'milumathew7779@gmail.com',
        'email2': 'alansha71011@gmail.com',
        'offices': [
            'EduApp 2nd floor Technoark phase I: Trivandrum, Kerala',
            'EduApp 4th floor Infoark phase III: Ernakulam, Kerala',
            'EduApp 10th floor Prince Info City II: Chennai, Tamil Nadu'
        ]
    }
    context = {
        'contact_info': contact_info,
        'course': course
    }
    return render(request, 'main/home1.html', context)

def signup(request, id):
    if request.method == 'POST':
        # Retrieve form data
        username = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        # Check if user exists in User
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username Exists! Try another Username...')
            return redirect('signup', id=id)

        # Check if email exists in User
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email Is Already Taken! Try Another One...')
            return redirect('signup', id=id)
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            reg = user_profile(user=user, username=username, email=email, password=password)
            reg.save()
            messages.success(request, 'You have successfully created an Account')
            return redirect('login', id=id)

    else:
        return render(request, 'main/signup.html', {'id':id})

def signin(request, id):
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('password')

        # Check if user is authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            if not user.is_staff:
                login(request, user)
                return redirect('view_course_description', id=id)
            else:
                messages.error(request, 'You do not have permission to access this dashboard.')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'main/login.html', {'id': id})

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        messages.success(request, "Logged out Successfully")
    return redirect('home1')

def base(request):
    return render(request, 'main/base.html')

def view_course_description(request, id):
    course = Course.objects.get(id=id)
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        course_name = request.POST['course']
        duration = request.POST['duration']
        price = request.POST['price']
        reg_date = request.POST['date']
        reg = registered_students(user=request.user, email=email, course=course_name, duration=duration, amount=price, registered_at=reg_date)
        reg.save()

        messages.success(request, 'You have successfully enrolled for the course')
        return redirect('booking', id=course.id)
    return render(request, 'main/course_description.html', {'course': course})

def booking_base(request, id):
    course2 = Course.objects.get(id=id)
    user = request.user
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        course1 = request.POST['course']
        duration1 = request.POST['duration']
        price = request.POST['price']
        payment_id = request.POST['payment_id']
        reg_date = timezone.now()

        reg = booking_students(user=user, email=email, course=course1, duration=duration1, price=price, payment_id=payment_id, start_date=reg_date)
        reg.save()

        messages.success(request, 'You have successfully completed the payment')
        return redirect('dashboard')
    return render(request, 'main/booking.html', {'course': course2})

def free_3days(request, id):
    course = Course.objects.get(id=id)
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        course_name = request.POST['course']
        duration = request.POST['duration']
        price = request.POST['price']
        payment_id = request.POST['payment_id']
        reg_date = request.POST['date1']
        reg = register_3freeday(user=request.user, email=email, course=course_name, duration=duration, amount=price, payment_id=payment_id, registered_at=reg_date)
        reg.save()

        messages.success(request, 'You have successfully enrolled for the 3-day free demo class')
        return redirect('dashboard')

    return render(request, 'main/free_reg.html', {'course': course})

@login_required
def success(request):
    user = request.user
    reg_user = registered_students.objects.get(user=user)
    reg_course = reg_user.course
    get_course = Course.objects.get(title=reg_course)
    get_id = get_course.id
    return render(request, 'main/success.html', {'id': get_id})

@login_required
def booking_success(request):
    user = request.user
    reg_user = registered_students.objects.get(user=user)
    reg_course = reg_user.course
    get_course = Course.objects.get(title=reg_course)
    get_id = get_course.id
    return render(request, 'main/booking_success.html', {'id': get_id})

def videomeet(request, payment_id):
    course = register_3freeday.objects.get(payment_id=payment_id)
    return render(request, 'main/videomeet_ui.html', {'course': course})

def live(request):
    user = request.user
    reg_student = registered_students.objects.get(user=user)
    course_name = reg_student.course
    course1 = Course.objects.get(title=course_name)
    return render(request, 'main/live.html', {'course': course1})

def login1(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if not user.is_staff:
                login(request, user)
                return redirect('dashboard')
            else:
                return redirect('admin_dashboard')
                #messages.error(request, 'You do not have permission to access this dashboard.')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'main/login1.html')

def signup1(request):
    if request.method == 'POST':
        username = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username Exists! Try another Username...')
            return redirect('signup1')

        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email Is Already Taken! Try Another One...')
            return redirect('signup1')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            reg = user_profile(user=user, username=username, email=email, password=password)
            reg.save()
            messages.success(request, 'You have successfully created an Account')
            return redirect('login1')

    else:
        return render(request, 'main/signup1.html')

@login_required
def dashboard(request):
    course = Course.objects.all()
    contact_info = {
        'email1': 'milumathew7779@gmail.com',
        'email2': 'alansha71011@gmail.com',
        'offices': [
            'EduApp 2nd floor Technoark phase I: Trivandrum, Kerala',
            'EduApp 4th floor Infoark phase III: Ernakulam, Kerala',
            'EduApp 10th floor Prince Info City II: Chennai, Tamil Nadu'
        ]
    }
    context = {
        'contact_info': contact_info,
        'course': course
    }
    return render(request, 'main/dashboard.html', context)

@login_required
def online_class(request):
    user = request.user

    if booking_students.objects.filter(user=user).exists():
        return redirect('videomeet1')

    free_day = register_3freeday.objects.filter(user=user).first()
    if free_day:
        expiry_date = free_day.registered_at + timedelta(days=3)
        if timezone.now() <= expiry_date:
            return redirect('videomeet1')

    return redirect('videomeet1')

@login_required
def videomeet1(request):
    user = request.user
    course = registered_students.objects.get(user=user)
    return render(request, 'main/videomeet_ui.html', {'course': course})

@login_required
def booking1(request):
    user = request.user
    course = registered_students.objects.get(user=user)
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        course_name = request.POST['course']
        price = request.POST['price']
        payment_id = request.POST['payment_id']
        reg_date = request.POST['date1']

        reg = register_3freeday(user=user, email=email, course=course_name, duration=course.duration, amount=price, payment_id=payment_id, registered_at=reg_date)
        reg.save()

        messages.success(request, 'You have successfully completed the payment')
        return redirect('dashboard')

    return render(request, 'main/booking.html', {'course': course})

@login_required
def mocktest(request):
    user = request.user
    if not user_has_access(user, 'mocktest'):
        return redirect('admin_lock')
    return render(request, 'main/interview_prep.html')

@login_required
def certificate(request):
    user = request.user
    if not user_has_access(user, 'certificate'):
        return redirect('admin_lock')
    if request.method == 'POST':
        uploaded_file = request.FILES.get('certificate')

        if uploaded_file:
            save_path = r'C:\Users\\' + uploaded_file.name
            with open(save_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            success_message = 'File uploaded successfully!'
        else:
            success_message = 'No file chosen!'

    return render(request, 'main/certificates_upload.html')

def submit_resume(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        education = request.POST.get('education')
        work_experience = request.POST.get('work_experience')
        skills = request.POST.get('skills')

        if not all([name, email, phone, education, work_experience, skills]):
            return HttpResponse('Some fields are missing.', status=400)

        html_string = render_to_string('main/resume_template.html', {
            'name': name,
            'email': email,
            'phone': phone,
            'education': education,
            'work_experience': work_experience,
            'skills': skills
        })

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="resume.pdf"'

        pisa_status = pisa.CreatePDF(html_string, dest=response)
        if pisa_status.err:
            return HttpResponse('PDF generation error!', status=500)

        return response

    return HttpResponse('Invalid request', status=400)

@login_required
def resume_creation(request):
    user = request.user
    if not user_has_access(user, 'resume_upload'):
        return redirect('admin_lock')
    return render(request, 'main/resume_form.html')

@login_required
def placement(request):
    user = request.user
    if not user_has_access(user, 'placement'):
        return redirect('admin_lock')
    return render(request, 'main/placement.html')

@login_required
def company(request):
    user = request.user
    if not user_has_access(user, 'company'):
        return redirect('admin_lock')
    return render(request, 'main/company.html')

def user_has_access(user, page_name):
    try:
        page = Page.objects.get(name=page_name)
        page_lock = PageLock.objects.get(username=user)
        return page in page_lock.pages.all() and not page_lock.is_locked == False
    except (Page.DoesNotExist, PageLock.DoesNotExist):
        return False


def admin_lock(request):
    return render(request, 'main/admin_lock.html')

def homenew(request):
    course = Course.objects.all()
    contact_info = {
        'email1': 'milumathew7779@gmail.com',
        'email2': 'alansha71011@gmail.com',
        'offices': [
            'EduApp 2nd floor Technoark phase I: Trivandrum, Kerala',
            'EduApp 4th floor Infoark phase III: Ernakulam, Kerala',
            'EduApp 10th floor Prince Info City II: Chennai, Tamil Nadu'
        ]
    }
    context = {
        'contact_info': contact_info,
        'course': course
    }
    return render(request, 'main/home-new.html',context)

@login_required
def dashboard1(request):
    course = Course.objects.all()
    contact_info = {
        'email1': 'milumathew7779@gmail.com',
        'email2': 'alansha71011@gmail.com',
        'offices': [
            'EduApp 2nd floor Technoark phase I: Trivandrum, Kerala',
            'EduApp 4th floor Infoark phase III: Ernakulam, Kerala',
            'EduApp 10th floor Prince Info City II: Chennai, Tamil Nadu'
        ]
    }
    context = {
        'contact_info': contact_info,
        'course': course
    }
    return render(request, 'main/dashboard-new.html', context)
def admin_dashboard(request):
    reg_stud = Course.objects.all()
    reg_stud1 = registered_students.objects.all()
    return render(request, 'main/admin_dashboard.html',{'course1':reg_stud,'reg':reg_stud1})
def admin_status(request):
    status = PageLock.objects.all()
    #page= Page.objects.all()
    return render(request,'main/admin-status.html',{'status':status})
def admin_payment(request):
    reg = registered_students.objects.all()
    actual = booking_students.objects.all()
    free = register_3freeday.objects.all()
    # page= Page.objects.all()
    return render(request, 'main/admin-payment.html', {'reg':reg,'actual': actual,'free':free})
def edit_status(request,id):
    get_user = PageLock.objects.get(id=id)
    pages = Page.objects.all()
    return render(request,'main/edit-status.html',{'get_user':get_user,'pages':pages})