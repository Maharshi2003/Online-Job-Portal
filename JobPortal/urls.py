"""
URL configuration for JobPortal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django import views
from Job import views
from django.urls import path, include
from Job.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('api/', include('api.urls')),
    path('',index, name="index"),
    path('Contact',Contact, name="Contact"),
    path('FAQ', FAQ, name="FAQ"),
    path('Ratings/', Ratings, name="Ratings"),
    path('User_login/',User_login, name="User_login"),
    path('User_home/', User_home, name="User_home"),
    path('User_login_api/', User_login_api, name='User_login_api'),
    path('User_signup/',User_signup, name="User_signup"),
    path('User_signup_api/', User_signup_api, name='User_signup_api'),
    path('change_passworduser/',change_passworduser,name="change_passworduser"),
    path('Logout/', Logout, name="Logout"),
    
    path('Company_login/', views.Company_login, name='Company_login'),
    path('Company_login_api/',Company_login_api, name='Company_login_api'),
    path('Company_home/',Company_home, name='Company_home'),
    path('Company_Signup/',Company_Signup, name="Company_Signup"),
    path('Company_Signup_api/',Company_Signup_api, name="Company_Signup_api"),
    path('change_passwordcompany/', change_passwordcompany, name='change_passwordcompany'),
    #path('logout_api/', views.User_logout_api, name='logout_api'),
    
    path('Recruiter_login/', Recruiter_login, name="Recruiter_login"),
    path('Recruiter_login_api/',Recruiter_login_api, name='Recruiter_login_api'),
    path('Recruiter_Signup/', Recruiter_Signup, name="Recruiter_Signup"),
    path('Recruiter_Signup_api/',Recruiter_Signup_api, name="Recruiter_Signup_api"),
    path('change_passwordrecruiter/', change_passwordrecruiter, name='change_passwordrecruiter'),
    path('Recruiter_home/',Recruiter_home, name='Recruiter_home'),
    
    path('Add_Job',Add_Job,name="Add_Job"),
    path('Job_List/', Job_List, name="Job_List"),
    path('edit_jobdetails/<int:pid>/', edit_jobdetails, name="edit_jobdetails"),
    path('delete_job/<int:pid>/', delete_job, name="delete_job"),
    
    path('Latest_Job',Latest_Job,name="Latest_Job"),
    path('Apply/<int:pid>/',Apply_job, name='Apply'),
    path('User_latestjob',User_latestjob,name="User_latestjob"),
    path('job_detail/<int:pid>/', job_detail, name='job_detail'),
    path('candidate_list',candidate_list, name='candidate_list'),
    path('Recruiter_pending',Recruiter_pending,name="Recruiter_pending"),
    path('Change_status/<int:id>/',Change_status,name="Change_status"),
    path('Recruiter_rejected',Recruiter_rejected,name="Recruiter_rejected"),
    path('Recruiter_accepted',Recruiter_accepted,name="Recruiter_accepted"),
    path('Recruiter_all/',views.Recruiter_all,name="Recruiter_all"),
    #path('Recruiter_accepted',Recruiter_accepted,name="Recruiter_accepted"),
    path('delete_Users/<int:id>/', delete_Users, name='delete_Users'),
    path('delete_Recruiter/<int:id>/', delete_Recruiter, name='delete_Recruiter'),
    path('View_Users',View_Users,name="View_Users"),
    
    path('My_Applications/', My_Applications, name='My_Applications'),
    path('Saved_Jobs/', Saved_Jobs, name='Saved_Jobs'),
    path('toggle_save_job/<int:pid>/', toggle_save_job, name='toggle_save_job'),
    path('update_application_status/<int:id>/', update_application_status, name='update_application_status'),

    path('forgot_password/', forgot_password, name='forgot_password'),
    path('reset_password/<int:user_id>/', reset_password, name='reset_password'),
    path('verify_otp/', verify_otp, name='verify_otp'),
]
#urlpatterns += static(
    # settings.MEDIA_URL,
    # document_root=settings.MEDIA_ROOT
 # ) 
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
