from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from .serializers import Job_SeekerSerializer
from rest_framework import status
from django.contrib import messages
from rest_framework.response import Response
#from rest_framework.authtoken.models import Token
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.db import transaction
from .models import Job_Seeker, Company, Recruiter, Category, Job, Apply
from datetime import date
import random

from django.core.mail import send_mail

# Create your views here.
def index(request):
    return render(request, 'index.html')

def Contact(request):
    return render(request, 'Contact.html')

def User_login(request):
    return render(request, 'User_login.html')

def User_signup(request):
    return render(request, 'User_signup.html')

def get_or_create_category(category_name, category_type):
    if not category_name or not category_type:
        return None

    category, created = Category.objects.get_or_create(
        Category_type=category_type,
        defaults={'Category': category_name}
    )

    if category.Category != category_name:
        category.Category = category_name
        category.save()

    return category


def jobs_for_company(company=None, company_name=None):
    company_names = []

    if company and company.company_name:
        company_names.append(company.company_name.strip())

    if company_name:
        company_names.append(company_name.strip())

    company_names = [name for name in set(company_names) if name]

    if not company_names:
        return Job.objects.none()

    query = Q()

    for name in company_names:
        query |= Q(company__company_name__iexact=name)
        query |= Q(recruiter__company__company_name__iexact=name)
        query |= Q(recruiter__cname__iexact=name)

    return Job.objects.filter(query).distinct()


def User_home(request):
    return render(request, 'User_home.html')

def Company_login(request):
    return render(request, 'Company_login.html')

def Company_home(request):
    return render(request, 'Company_home.html')

def Company_Signup(request):
    return render(request,'Company_Signup.html')

def Recruiter_login(request):
    return render(request, 'Recruiter_login.html')

def Recruiter_Signup(request):
    return render(request,'Recruiter_Signup.html')
# ===================== LOGOUT =====================
def Logout(request):

    logout(request)

    return redirect('index')

#def User_logout_api(request):

    logout(request)

    return JsonResponse({
        'status': 'success',
        'message': 'Logout Successful'
    })
    return redirect('/User_login/')
#====================User_login_api==================
@api_view(['POST'])
def User_login_api(request):

    username = request.POST.get('username')
    password = request.POST.get('password')

    print(username, password)

    user = authenticate(
        request,
        username=username,
        password=password
    )

    if user is not None:

        try:

            # Check whether this user is a Job Seeker
            job_seeker = Job_Seeker.objects.get(User=user)

            print("USER LOGIN SUCCESS")

            login(request, user)

            request.session['user_type'] = 'user'
            request.session['job_seeker_id'] = job_seeker.id

            return redirect('/User_home/')

        except Job_Seeker.DoesNotExist:

            print("THIS USER IS NOT A JOB SEEKER")

            return render(
                request,
                'User_login.html',
                {
                    'error': 'not_user'
                }
            )

    else:

        print("LOGIN FAILED")

        return render(
            request,
            'User_login.html',
            {
                'error': 'yes'
            }
        )

    return redirect('User_login')

#def User_login_api(request):

    username = request.data.get('username')
    password = request.data.get('pwd')

    # Empty field validation
    if not username or not password:

        return Response(
            {
                'status': 'error',
                'message': 'Username and Password are required'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Authenticate User
    user = authenticate(request, username=username, password=password)

    if user is not None:

        try:
            user_obj = Job_Seeker.objects.get(User=user)

            # Session Login
            login(request, user)

            return Response(
                {
                    'status': 'success',
                    'message': 'Login Successful',
                    'user_id': user.id,
                    'username': user.username,
                    'type': user_obj.type
                },
                status=status.HTTP_200_OK
            )

        except Job_Seeker.DoesNotExist:

            return Response(
                {
                    'status': 'error',
                    'message': 'Profile not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )

    else:

        return Response(
            {
                'status': 'error',
                'message': 'Invalid Username or Password'
            },
            status=status.HTTP_401_UNAUTHORIZED
        )

#def User_home(request):
    if not request.user.is_authenticated:
        return redirect('User_login')
    User = request.user                            #For the data view code
    Job_seeker = Job_Seeker.objects.get(User=User)
    d = {'Job_Seeker': Job_seeker}
    return render(request, 'User_home.html',d)

def User_home(request):

    if not request.user.is_authenticated:
        return redirect('User_login')

    User = request.user

    try:

        Job_seeker = Job_Seeker.objects.get(User=User)

        # UPDATE PROFILE
        if request.method == "POST":

            fname = request.POST.get('Fname')
            lname = request.POST.get('Lname')
            contact = request.POST.get('Contact')
            email = request.POST.get('Email')
            gender = request.POST.get('Gender')
            category_name = request.POST.get('category')
            category_type = request.POST.get('category_type')

            image = request.FILES.get('Image')

            # Update Django User table
            User.first_name = fname
            User.last_name = lname
            User.username = email
            User.email = email
            User.save()

            # Update Job_Seeker table
            Job_seeker.mobile = contact
            Job_seeker.gender = gender
            Job_seeker.Category = get_or_create_category(category_name, category_type)
            Job_seeker.category_type = category_type

            # Update Image only if new image selected
            if image:
                Job_seeker.image = image

            Job_seeker.save()

            return render(request, 'User_home.html', {
                'Job_Seeker': Job_seeker,
                'error': 'no'
            })

        d = {
            'Job_Seeker': Job_seeker
        }

        return render(request, 'User_home.html', d)

    except Job_Seeker.DoesNotExist:

        return render(request, 'User_home.html', {
            'error': 'yes'
        })
#========================User_signup_api====================================
@api_view(['POST'])
def User_signup_api(request):

    if request.method != "POST":
        return redirect('User_signup')

    try:

        fname = (request.POST.get('Fname') or '').strip()
        lname = (request.POST.get('Lname') or '').strip()
        contact = (request.POST.get('Contact') or '').strip()
        email_username = (request.POST.get('Email') or '').strip()

        if email_username.endswith('@gmail.com'):
            email = email_username
        elif '@' in email_username:
            return render(request, 'User_signup.html', {'error': 'yes'})
        else:
            email = email_username + "@gmail.com"

        password = request.POST.get('pwd')
        gender = request.POST.get('Gender')
        state = request.POST.get('state')
        city = request.POST.get('city')
        image = request.FILES.get('Image')
        category = request.POST.get('category')
        category_type = request.POST.get('category_type')

        # Validation

        if not fname or not lname or not email or not password or not category or not category_type:

            return render(request, 'User_signup.html', {'error': 'yes'})

        # Check Existing User

        if User.objects.filter(username=email).exists():

            return render(request, 'User_signup.html', {'error': 'exist'})

        # Create User

        with transaction.atomic():
            user = User.objects.create_user(
                first_name=fname,
                last_name=lname,
                username=email,
                email=email,
                password=password
            )

            category_obj = get_or_create_category(category, category_type)

            Job_Seeker.objects.create(
                User=user,
                mobile=contact,
                gender=gender,
                image=image,
                state=state,
                city=city,
                Category=category_obj,
                category_type=category_type,
            )

        return render(request, 'User_signup.html', {'error': 'no'})

    except Exception as e:
        print(e)

        return render(request, 'User_signup.html', {'error': 'yes'})
#===========================change_passworduser==============================
def change_passworduser(request):

    if not request.user.is_authenticated:
        return redirect('User_login')

    error = ""

    user = request.user

    # Current User Profile
    try:
        Job_seeker = Job_Seeker.objects.get(User=user)

    except Job_Seeker.DoesNotExist:
        Job_seeker = None

    if request.method == 'POST':

        o = request.POST.get('cpwd')
        n = request.POST.get('npwd')

        if user.check_password(o):

            user.set_password(n)
            user.save()

            error = "no"

        else:

            error = "not"

    d = {
        'error': error,
        'Job_Seeker': Job_seeker
    }

    return render(request, 'change_passworduser.html', d)
#==========================Company login=============================
@api_view(['POST'])
def Company_login_api(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        print(username, password)

        user = authenticate(request, username=username, password=password)

        if user is not None:

            try:
                # Check whether logged in user is company
                company = Company.objects.get(User=user)

                print("COMPANY LOGIN SUCCESS")

                login(request, user)
                request.session['user_type'] = 'company'

                return redirect('/Company_home/')

            except Company.DoesNotExist:

                print("NOT A COMPANY ACCOUNT")

                return render(request, 'Company_login.html', {
                    'error': 'not_company'
                })

        else:

            print("LOGIN FAILED")

            return render(request, 'Company_login.html', {
                'error': 'yes'
            })

    return redirect('Company_login')
#======================Company Home=============================
def Company_home(request):

    if not request.user.is_authenticated:
        return redirect('Company_login')

    error = ""

    user = request.user

    try:
        company = Company.objects.get(User=user)

    except Company.DoesNotExist:
        company = None

    if request.method == "POST" and company:

        d = request.POST.get('description')
        l = request.FILES.get('company_logo')

        # Save Description
        if d is not None:
            company.description = d

        # Save Logo if uploaded
        if l:
            company.company_logo = l

        company.save()

        return redirect('/Company_home/?updated=1')

    d = {
        'company': company,
        'error': error,
        'updated': request.GET.get('updated')
    }

    return render(request, 'Company_home.html', d)
#def Company_home(request):

    if not request.user.is_authenticated:
        return redirect('Company_login')

    company = Company.objects.get(User=request.user)

    d = {'company': company}

    return render(request, 'Company_home.html', d)
#=======================Company_Signup==========================
@api_view(['POST'])
def Company_Signup_api(request):

    try:

        print(request.POST)
        print(request.FILES)

        # Get Form Data

        company_name = request.POST.get('company_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        website = request.POST.get('website')
        address = request.POST.get('address')

        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')

        company_size = request.POST.get('company_size')
        established_year = request.POST.get('established_year')

        description = request.POST.get('description')

        password = request.POST.get('pwd')

        company_logo = request.FILES.get('company_logo')

        print(company_name, email, password)

        # Validation

        if not company_name or not email or not password:

            return render(request, 'Company_Signup.html', {'error': 'yes'})

        # Check Existing Company Email

        if User.objects.filter(username=email).exists():

            return render(request, 'Company_Signup.html', {'error': 'exist'})

        # Create User

        user = User.objects.create_user(

            first_name = company_name,
            username = email,
            email = email,
            password = password

        )

        # Save Company Data

        Company.objects.create(
            User = user,
            company_name = company_name,
            email = email,
            phone_no = phone,
            website = website,
            address = address,
            country = country,
            state = state,
            city = city,
            company_size = company_size,
            established_year = established_year,
            description=description,
            company_logo = company_logo

        )

        # Success

        return render(request, 'Company_Signup.html', {'error': 'no'})

    except Exception as e:

        print(e)

        return render(request, 'Company_Signup.html', {'error': 'yes'})
#============================Change_passwordcompany=================
def change_passwordcompany(request):

    if not request.user.is_authenticated:
        return redirect('Company_login')

    error = ""

    user = request.user

    # Current Company Profile

    try:
        company = Company.objects.get(User=user)

    except Company.DoesNotExist:
        company = None

    if request.method == 'POST':

        o = request.POST.get('cpwd')
        n = request.POST.get('npwd')

        if user.check_password(o):

            user.set_password(n)
            user.save()

            error = "no"

        else:

            error = "not"

    d = {

        'error': error,
        'company': company

    }

    return render(request, 'change_passwordcompany.html', d)
#==============================Recruiter login api================
@api_view(['POST'])
def Recruiter_login_api(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        print(username, password)

        user = authenticate(request, username=username, password=password)

        if user is not None:

            try:
                # Check whether this user is a recruiter
                recruiter = Recruiter.objects.get(User=user)

                print("RECRUITER LOGIN SUCCESS")

                login(request, user)

                request.session['user_type'] = 'recruiter'
                request.session['recruiter_id'] = recruiter.id

                return redirect('/Recruiter_home/')

            except Recruiter.DoesNotExist:

                print("THIS USER IS NOT A RECRUITER")

                return render(
                    request,
                    'Recruiter_login.html',
                    {'error': 'not_recruiter'}
                )

        else:

            print("LOGIN FAILED")

            return render(
                request,
                'Recruiter_login.html',
                {'error': 'yes'}
            )

    return redirect('Recruiter_login')
#====================Recruiter_Signup_api===========================
@api_view(['POST'])
def Recruiter_Signup_api(request):

    try:

        print("POST DATA :", request.POST)
        print("FILES :", request.FILES)

        # Get Form Data

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        contact_no = request.POST.get('contact_no')
        email = request.POST.get('Email')
        gender = request.POST.get('Gender')
        state = request.POST.get('state')
        city = request.POST.get('city')
        cname = request.POST.get('cname')
        password = request.POST.get('pwd')

        recruiter_image = request.FILES.get('recruiter_image')
        clogo = request.FILES.get('clogo')

        print("First Name :", first_name)
        print("Last Name :", last_name)
        print("Email :", email)
        print("Company :", cname)
        print("Password :", password)

        # Validation

        if not first_name or not email or not password:

            print("Validation Failed")

            return render(
                request,
                'Recruiter_Signup.html',
                {'error': 'yes'}
            )

        # Check Existing Email

        if User.objects.filter(username=email).exists():

            print("Email Already Exists")

            return render(
                request,
                'Recruiter_Signup.html',
                {'error': 'exist'}
            )

        # Create User

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=email,
            email=email,
            password=password
        )

        print("User Created Successfully")

        # Company Check

        company = Company.objects.filter(company_name=cname).first()

        if company is None:

            company = Company.objects.create(
                User=user,
                company_name=cname,
                email=email,
                company_logo=clogo
            )

            print("Company Created Successfully")

        # Save Recruiter

        Recruiter.objects.create(
            User=user,
            company=company,
            first_name=first_name,
            last_name=last_name,
            contact_no=contact_no,
            email=email,
            gender=gender,
            state=state,
            city=city,
            cname=cname,
            recruiter_image=recruiter_image,
            clogo=clogo
        )

        print("Recruiter Created Successfully")

        return render(
            request,
            'Recruiter_Signup.html',
            {'error': 'no'}
        )

    except Exception as e:

        print("===================================")
        print("RECRUITER SIGNUP ERROR")
        print(str(e))
        print("===================================")

        return render(
            request,
            'Recruiter_Signup.html',
            {'error': 'yes'}
        )
#=======================change_passwordrecruiter=========================
def change_passwordrecruiter(request):

    if not request.user.is_authenticated:
        return redirect('Recruiter_login')

    error = ""

    user = request.user

    # Current Recruiter Profile

    try:
        recruiter = Recruiter.objects.get(User=user)

    except Recruiter.DoesNotExist:
        recruiter = None

    if request.method == 'POST':

        o = request.POST.get('cpwd')
        n = request.POST.get('npwd')

        if user.check_password(o):

            user.set_password(n)
            user.save()

            error = "no"

        else:

            error = "not"

    d = {

        'error': error,
        'recruiter': recruiter

    }

    return render(request,
                  'change_passwordrecruiter.html',
                  d)
#============================Recruiter_home========================
def Recruiter_home(request):

    if not request.user.is_authenticated:
        return redirect('Recruiter_login')

    error = ""

    user = request.user

    try:
        recruiter = Recruiter.objects.get(User=user)

    except Recruiter.DoesNotExist:
        recruiter = None

    if request.method == "POST":

        # Recruiter Image
        r = request.FILES.get('recruiter_image')

        # Company Logo
        c = request.FILES.get('clogo')

        # Save Recruiter Image
        if r:
            recruiter.recruiter_image = r

        # Save Company Logo
        if c:
            recruiter.clogo = c

        recruiter.save()

        error = "no"

    d = {

        'recruiter': recruiter,
        'error': error

    }

    return render(request,
                  'Recruiter_home.html',
                  d)
#===========================Add Job==================================
def Add_Job(request):

    if not request.user.is_authenticated:
        return redirect('Recruiter_login')

    error = ""

    company = Company.objects.filter(User=request.user).first()
    recruiter = Recruiter.objects.filter(User=request.user).first()
    login_type = request.session.get('user_type')
    is_recruiter_login = login_type == 'recruiter' or (recruiter and not company)
    is_company_login = login_type == 'company' or (company and not recruiter)
    posting_company = recruiter.company if is_recruiter_login and recruiter else company
    template_company = company if is_company_login else None
    template_recruiter = recruiter if is_recruiter_login else None
    posting_company_name = recruiter.cname if is_recruiter_login and recruiter else company.company_name if company else None

    same_company_jobs = jobs_for_company(posting_company, posting_company_name)

    if request.method == 'POST':
        try:
            category = get_or_create_category(
                request.POST.get('category'),
                request.POST.get('category_type')
            )

            Job.objects.create(
                company=posting_company,
                recruiter=recruiter if is_recruiter_login else None,
                job_title=request.POST.get('job_title'),
                category=category,
                experience=request.POST.get('experience'),
                location=request.POST.get('location'),
                min_salary=request.POST.get('min_salary'),
                max_salary=request.POST.get('max_salary'),
                start_date=request.POST.get('start_date'),
                end_date=request.POST.get('end_date'),
                skills=request.POST.get('skills'),
                job_description=request.POST.get('job_description'),
                clogo=request.FILES.get('clogo'),
                creation_date=date.today()
            )

            error = "Done"

        except Exception as e:
            print(e)
            error = "yes"

    return render(request, 'Add_Job.html', {
        'error': error,
        'company': template_company,
        'recruiter': template_recruiter
    })   
#=====================edit_jobdetails===========================
def edit_jobdetails(request, pid):
    if not request.user.is_authenticated:
        return redirect('Recruiter_login')

    recruiter = Recruiter.objects.filter(User=request.user).first()
    job = Job.objects.get(id=pid)
    error = ""

    if request.method == "POST":
        try:
            job.job_title = request.POST.get('job_title')

            job.category = get_or_create_category(
                request.POST.get('category'),
                request.POST.get('category_type')
            )

            job.experience = request.POST.get('experience')
            job.location = request.POST.get('location')

            job.min_salary = request.POST.get('min_salary')
            job.max_salary = request.POST.get('max_salary')

            job.skills = request.POST.get('skills')
            job.job_description = request.POST.get('job_description')

            job.start_date = request.POST.get('start_date')
            job.end_date = request.POST.get('end_date')

            # Company Logo (Optional)
            if request.FILES.get('clogo'):
                job.clogo = request.FILES.get('clogo')

            job.save()

            error = "no"

        except Exception as e:
            print(e)
            error = "yes"

    return render(
        request,
        'edit_jobdetails.html',
        {
            'job': job,
            'recruiter': recruiter,
            'error': error
        }
    )
# ===================== JOB LIST =====================
#def Job_List(request):
    if not request.user.is_authenticated:
        return redirect('Recruiter_login')
    
    #recruiter = Recruiter.objects.get(User=request.user)
    recruiter = Recruiter.objects.filter(User=request.user).first()
    jobs = jobs_for_company(recruiter.company, recruiter.cname) if recruiter else Job.objects.none()

    return render(request, 'Job_List.html', {
        'jobs': jobs,
        'recruiter': recruiter
    })     
def Job_List(request):

    if not request.user.is_authenticated:
        return redirect('Recruiter_login')

    recruiter = Recruiter.objects.filter(User=request.user).first()
    company = Company.objects.filter(User=request.user).first()

    jobs = Job.objects.none()

    # Recruiter Login
    if recruiter:
        jobs = Job.objects.filter(company=recruiter.company)

    # Company Login
    elif company:
        jobs = Job.objects.filter(company=company)

    return render(request, 'Job_List.html', {
        'jobs': jobs,
        'recruiter': recruiter,
        'company': company
    }) 
#===================Delete_Job=============================
def delete_job(request, pid):
    if not request.user.is_authenticated:
        return redirect('Recruiter_login')

    job = Job.objects.get(id=pid)
    job.delete()
    return redirect('Job_List')
#===================Latest Job===============================
def Latest_Job(request):
    today = date.today()
    data = Job.objects.filter(
        start_date__lte=today,
        end_date__gte=today
    ).order_by('-start_date')
    return render(
        request,
        'Latest_Job.html',
        {
            'data': data
        }
    )
#==================Apply_Job=================================
def Apply_job(request, pid):
    if not request.user.is_authenticated:
        return redirect('User_login')
    error = ""
    user = request.user
    job_seeker = Job_Seeker.objects.get(User=user)
    job = Job.objects.get(id=pid)
    today = date.today()
    if job.end_date < today:
        error = "Close"
        return render(request, 'Apply.html', {'error': error})
    
    elif job.start_date > today:
        error = "Not Open"
        return render(request, 'Apply.html', {'error': error})
    
    if request.method == "POST":
        resume = request.FILES['Resume']
        Apply.objects.create(Job_seeker=job_seeker, job=job, Resume=resume, Date=date.today())
        error = "Done"

    return render(request, 'Apply.html', {'error': error, 'Job_Seeker': job_seeker})
#=================== User_latestjob ==========================
#def User_latestjob(request):
    data = Job.objects.all().order_by('-start_date')

    # Get current user
    User = request.user

    # Get Job Seeker object
    job_seeker = Job_Seeker.objects.filter(User=User).first()

    # If job seeker not found, return page safely
    if job_seeker is None:
        return render(request, 'User_latestjob.html', {'data': data, 'list': []})

    # Get all applied jobs
    applied_jobs = Apply_job.objects.all().filter(Job_seeker=job_seeker)
    # Store applied job IDs
    list = []
    for i in applied_jobs:
        list.append(i.job.id)
    return render(request, 'User_latestjobs.html', {'data': data, 'list': list})

#def User_latestjob(request):

    data = Job.objects.all().order_by('-start_date')

    # Current logged-in user
    current_user = request.user

    # Get Job Seeker object
    job_seeker = Job_Seeker.objects.filter(
        User=current_user
    ).first()

    if job_seeker is None:
        return render(
            request,
            'User_latestjob.html',
            {
                'data': data,
                'list': []
            }
        )

    # Applied jobs
    applied_jobs = Apply.objects.filter(
        Job_seeker=job_seeker
    )

    applied_job_ids = []

    for i in applied_jobs:
        applied_job_ids.append(i.job.id)

    return render(
        request,
        'User_latestjob.html',
        {
            'data': data,
            'list': applied_job_ids
        }
    )
    #

#def User_latestjob(request):

    data = Job.objects.all().order_by('-start_date')

    user = request.user

    job_seeker = Job_Seeker.objects.filter(User=user).first()

    if job_seeker is None:
        return render(
            request,
            'User_latestjobs.html',
            {
                'data': data,
                'list': []
            }
        )

    applied_jobs = Apply_job.objects.filter(
        Job_seeker=job_seeker
    )

    applied_list = []

    for i in applied_jobs:
        applied_list.append(i.job.id)

    return render(
        request,
        'User_latestjobs.html',
        {
            'data': data,
            'list': applied_list,
            'job_seeker': job_seeker
        }
    )
    
from datetime import date

def User_latestjob(request):

    if not request.user.is_authenticated:
        return redirect('User_login')

    today = date.today()

    user = request.user

    job_seeker = Job_Seeker.objects.filter(
        User=user
    ).first()

    if not job_seeker:

        return render(
            request,
            'User_latestjob.html',
            {
                'data': [],
                'list': [],
                'user_profile': None,
                'Job_Seeker': None
            }
        )

    applied_jobs = Apply.objects.filter(
        Job_seeker=job_seeker
    )

    applied_list = []

    for i in applied_jobs:
        applied_list.append(i.job.id)

    data = Job.objects.filter(
        Q(start_date__lte=today, end_date__gte=today) |
        Q(id__in=applied_list)
    ).distinct().order_by('-start_date')

    return render(
        request,
        'User_latestjob.html',
        {
            'data': data,
            'list': applied_list,
            'job_seeker': job_seeker,
            'user_profile': job_seeker,
            'Job_Seeker': job_seeker
        }
    )
#=====================job_details===============================
def job_detail(request, pid):
    if not request.user.is_authenticated:
        return redirect('User_login')

    data = Job.objects.filter(id=pid).first()  # safer than get()
    if data is None:
        return redirect('User_latestjob')   # if job not found

    job_seeker = Job_Seeker.objects.filter(User=request.user).first()

    return render(
        request,
        'job_detail.html',
        {
            'data': data,
            'job_seeker': job_seeker,
            'user_profile': job_seeker,
            'Job_Seeker': job_seeker
        }
    )
#=================candidate_list================================
#def candidate_list(request):
    if not request.user.is_authenticated:
        return redirect('Recruiter_login')
    
    recruiter = Recruiter.objects.filter(User=request.user).first()
    company = Company.objects.filter(User=request.user).first()
    if recruiter:
        data = Apply.objects.filter(job__recruiter=recruiter)
    elif company:
        data = Apply.objects.filter(
            Q(job__company=company) | Q(job__recruiter__company=company)
        ).distinct()
    else:
        data = Apply.objects.none()

    return render(request, 'candidate_list.html', {
        'data': data,
        'recruiter': recruiter,
        'company': company
    })


#def candidate_list(request):

    recruiter = Recruiter.objects.get(User=request.user)

    data = Apply.objects.filter(
        job__company=recruiter.company
    )

    return render(
        request,
        'candidate_list.html',
        {
            'data': data
        }
    ) 
 
def candidate_list(request):

    if not request.user.is_authenticated:
        return redirect('Recruiter_login')

    recruiter = Recruiter.objects.filter(
        User=request.user
    ).first()

    company = Company.objects.filter(
        User=request.user
    ).first()

    if recruiter:

        # Show all candidates of this company
        data = Apply.objects.filter(
            Q(job__company=recruiter.company) |
            Q(job__recruiter__company=recruiter.company)
        ).distinct()

    elif company:

        data = Apply.objects.filter(
            Q(job__company=company) |
            Q(job__recruiter__company=company)
        ).distinct()

    else:

        data = Apply.objects.none()

    return render(
        request,
        'candidate_list.html',
        {
            'data': data,
            'recruiter': recruiter,
            'company': company
        }
    )     
#========================Recruiter Manage=================================
def Recruiter_pending(request):
    if not request.user.is_authenticated:
        return redirect('Company_login')

    company = Company.objects.filter(User=request.user).first()
    data = Recruiter.objects.filter(status="Pending")

    if company:
        data = data.filter(company=company)

    return render(request, 'Recruiter_pending.html', {
        'data': data,
        'company': company
    })

def Change_status(request,id):
    if not request.user.is_authenticated:
        return redirect('Company_login')
    error=""
    company = Company.objects.filter(User=request.user).first()
    recruiter = Recruiter.objects.get(id=id)
    if request.method=="POST":
        s = request.POST['status']
        recruiter.status = s
        try:
            recruiter.save()
            error="no"
        except:
            error="yes"
    return render(request, 'Change_status.html', {
        'recruiter': recruiter,
        'company': company,
        'error': error
    })

#def Recruiter_rejected(request):
    if not request.user.is_authenticated:
        return redirect('Company_login')

    data = Recruiter.objects.filter(status="Rejected")
    return render(request, 'Recruiter_rejected.html', {'data': data})

def Recruiter_rejected(request):

    if not request.user.is_authenticated:
        return redirect('Company_login')

    company = Company.objects.filter(User=request.user).first()

    data = Recruiter.objects.filter(
        company=company,
        status="Rejected"
    )

    return render(
        request,
        'Recruiter_rejected.html',
        {
            'data': data,
            'company': company
        }
    )

def Recruiter_accepted(request):
    if not request.user.is_authenticated:
        return redirect('Company_login')
    company = Company.objects.filter(User=request.user).first()
    data = Recruiter.objects.filter(
        company=company,
        status="Accepted"
    )
    return render(
        request,
        'Recruiter_accepted.html',
        {
            'data': data,
            'company': company
        }
    )

def Recruiter_all(request):
    if not request.user.is_authenticated:
        return redirect('Company_login')
    company = Company.objects.filter(User=request.user).first()
    if company:
        data = Recruiter.objects.filter(company=company)
    else:
        data = Recruiter.objects.none()
    return render(
        request,
        'Recruiter_all.html',
        {
            'data': data,
            'company': company
        }
    )
    
def delete_Recruiter(request,id):
    if not request.user.is_authenticated:
        return redirect('Company_login')
    Recruiter = User.objects.get(id=id)
    Recruiter.delete()
    return redirect('Recruiter_all')

def delete_Users(request,id):
    if not request.user.is_authenticated:
        return redirect('Company_login')
        return redirect('Recruiter_login')

    #data = Job_Seeker.objects.get(id=id)
    data = User.objects.get(id=id)
    data.delete()
    return redirect('View_Users')

def View_Users(request):

    if not request.user.is_authenticated:
        return redirect('index')

    company = Company.objects.filter(User=request.user).first()
    recruiter = Recruiter.objects.filter(User=request.user).first()

    data = Job_Seeker.objects.all()

    return render(
        request,
        'View_Users.html',
        {
            'data': data,
            'company': company,
            'recruiter': recruiter
        }
    )

#def View_Users(request):
    if not request.user.is_authenticated:
        return redirect('Company_login')
        return redirect('Recruiter_login')
    data = Job_Seeker.objects.all()
    return render(request, 'View_Users.html', {'data': data})
#=========================forgot Password============================
#def forgot_password(request):
    error = ""
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(username=email)
            return redirect('reset_password', user_id=user.id)
        except User.DoesNotExist:
            error = "notfound"
    return render(
        request,
        'forgot_password.html',
        {
            'error': error
        }
    )
    
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)

            otp = str(random.randint(100000, 999999))

            request.session['otp'] = otp
            request.session['user_id'] = user.id

            print("OTP Saved:", otp)
            print("User ID Saved:", user.id)

            # send email here

            return redirect('verify_otp')

        except User.DoesNotExist:
            return render(request, 'forgot_password.html', {
                'error': 'Email not found'
            })

    return render(request, 'forgot_password.html')



#def reset_password(request):
    email = request.session.get('reset_email')
    if not email:
        return redirect('forgot_password')
    if request.method == "POST":
        pwd = request.POST.get("pwd")
        cpwd = request.POST.get("cpwd")
        if pwd != cpwd:
            return render(
                request,
                'reset_password.html',
                {'error': 'nomatch'}
            )
        user = User.objects.get(username=email)
        user.set_password(pwd)
        user.save()
        request.session.flush()
        return render(
            request,
            'reset_password.html',
            {'error': 'done'}
        )

    return render(request, 'reset_password.html')

#def reset_password(request, user_id):
    error = ""
    try:
        user = User.objects.get(id=user_id)
        if request.method == "POST":
            pwd = request.POST.get("pwd")
            cpwd = request.POST.get("cpwd")
            if pwd != cpwd:
                error = "nomatch"
            else:
                user.set_password(pwd)
                user.save()
                error = "done"
        return render(
            request,
            'reset_password.html',
            {
                'error': error
            }
        )
    except User.DoesNotExist:
        return redirect('forgot_password')
    
#def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        session_otp = request.session.get('reset_otp')
        if entered_otp == session_otp:
            return redirect('reset_password')
        else:
            return render(
                request,
                'verify_otp.html',
                {'error': 'invalid'}
            )
    return render(request, 'verify_otp.html')

def reset_password(request, user_id):
    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        password = request.POST.get('password')

        user.set_password(password)
        user.save()

        return redirect('User_login')

    return render(request, 'reset_password.html')

#def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')

        if otp == request.session.get('otp'):
            user_id = request.session.get('user_id')

            return redirect('reset_password', user_id=user_id)

    return render(request, 'verify_otp.html')

def verify_otp(request):
    print("Session Data:", dict(request.session))
    if request.method == "POST":
        entered_otp = request.POST.get('otp')

        stored_otp = request.session.get('otp')
        user_id = request.session.get('user_id')

        print("Entered OTP:", entered_otp)
        print("Stored OTP:", stored_otp)
        print("User ID:", user_id)

        if str(entered_otp).strip() == str(stored_otp).strip():

            if user_id:
                return redirect('reset_password', user_id=user_id)

        return render(request, 'verify_otp.html', {
            'error': 'Invalid OTP'
        })

    print(request.session.items())
    return render(request, 'verify_otp.html')