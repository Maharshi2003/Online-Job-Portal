from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

User = get_user_model()
# Create your models here.
#==========================Category========================================
class Category(models.Model):
    CATEGORY_CHOICES = (
        ('Internship', 'Internship'),
        ('Junior Developer', 'Junior Developer'),
        ('Senior Developer', 'Senior Developer'),
        ('Fresher', 'Fresher'),
        ('AI/ML Intern', 'AI/ML Intern'),
    )
    Category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES
    )
    Category_type = models.CharField(
        max_length=100,
        unique=True
    )
    # created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.Category_type
    
#======================Job_Seeker=====================================  
class Job_Seeker(models.Model):
    User = models.OneToOneField(User,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15, null=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    image = models.FileField(null=True)
    gender = models.CharField(max_length=10,null=True)
    type = models.CharField(max_length=50, default='Fresher')
    Category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    category_type = models.CharField(max_length=200, null=True)
   
    def __str__(self):
        return self.User.username
#==================================Company===============================
class Company(models.Model):

    User = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    email = models.EmailField(null=True, blank=True)
    company_logo = models.ImageField(
        upload_to='company_logo/',
        null=True,
        blank=True
    )
    phone_no = models.CharField(
        max_length=15,
        null=True,
        blank=True
    )
    website = models.URLField(
        max_length=300,
        null=True,
        blank=True
    )
    address = models.TextField(null=True, blank=True)
    country = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    state = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    city = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    company_size = models.CharField(
        max_length=50,
        choices=[
            ('1-10', '1-10 Employees'),
            ('11-50', '11-50 Employees'),
            ('51-200', '51-200 Employees'),
            ('201-500', '201-500 Employees'),
            ('500+', '500+ Employees'),
        ],
        null=True,
        blank=True
    )
    established_year = models.PositiveIntegerField(
        null=True,
        blank=True
    )
    description = models.TextField(
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.company_name
#========================Recruiter==================================
class Recruiter(models.Model):

    User = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=15)
    email = models.EmailField()
    gender = models.CharField(max_length=20)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    recruiter_image = models.FileField(upload_to='recruiterimage/', null=True, blank=True)
    clogo = models.FileField(upload_to='companylogo/', null=True, blank=True)
    cname = models.CharField(max_length=200)
    status = models.CharField(
        max_length=20,
        default='Pending'
    )

    def __str__(self):
        return self.first_name
    #============================post Job=====================================
class Job(models.Model):
    recruiter = models.ForeignKey(
        Recruiter,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    job_title = models.CharField(max_length=200)
    job_description = models.TextField()
    
    #category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    
    category = models.ForeignKey(
    Category,
    on_delete=models.CASCADE,
    null=True,
    blank=True  
    )
    
    clogo = models.ImageField(
        upload_to='job_logo/',
        null=True,
        blank=True
    )

    skills = models.CharField(max_length=300)
    
    EXPERIENCE_CHOICES = (
        ('0-1', '0-1 Year'),
        ('1-1.5', '1-1.5 Years'),
        ('1.5-2', '1.5-2 Years'),
        ('2-3', '2-3 Years'),
        ('3-4', '3-4 Years'),
        ('4-5', '4-5 Years'),
        ('5-6', '5-6 Years'),
        ('6-7', '6-7 Years'),
        ('7-8', '7-8 Years'),
        ('8-9', '8-9 Years'),
        ('9-10', '9-10 Years'),
        ('10-11', '10-11 Years'),
        ('11-12', '11-12 Years'),
        ('12-13', '12-13 Years'),
        ('13-14', '13-14 Years'),
        ('14-15', '14-15 Years'),
        ('15-16', '15-16 Years'),
        ('16-17', '16-17 Years'),
        ('17-18', '17-18 Years'),
        ('18-19', '18-19 Years'),
        ('19-20', '19-20 Years'),
        ('20+', '20+ Years'),
    )

    experience = models.CharField(
        max_length=20,
        choices=EXPERIENCE_CHOICES
    )
    
    #experience = models.CharField(max_length=100)

    location = models.CharField(max_length=200)
    min_salary = models.IntegerField()
    max_salary = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    creation_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.job_title
#=============================Apply==================================
class Apply(models.Model):
   job = models.ForeignKey(Job,on_delete=models.CASCADE)
   Job_seeker = models.ForeignKey(Job_Seeker,on_delete=models.CASCADE)
   Resume = models.FileField(null=True)
   Date = models.DateField() 
   
   def __str__(self):
      return self.job_job.title