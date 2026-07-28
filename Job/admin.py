from django.contrib import admin
from .models import Job_Seeker
from .models import Category,Company,Recruiter,Job,Apply


# Register your models here.
admin.site.register(Job_Seeker)
admin.site.register(Category)
admin.site.register(Company)
admin.site.register(Recruiter)
admin.site.register(Job)
admin.site.register(Apply)