from django.contrib import admin
from .models import (Employee, State, City, EducationalBackground, SkillCategory, 
                     WorkExperience, Company, Job, Skill, JobRequest, JobCategory)


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_per_page = 10
    

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'state_name']
    list_per_page = 10

    def state_name(self, city):
        return city.state.name    


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['user']
    list_per_page = 10



@admin.register(EducationalBackground)
class EducationalBackgroundAdmin(admin.ModelAdmin):
    list_display = ['employee']


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ['category',]
    list_per_page = 10


@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'job_title']
    list_per_page = 10   


@admin.register(Company)
class Company(admin.ModelAdmin):
    list_display = ['user', 'name_of_company', 'website_url']
    list_per_page = 10   


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['company', 'job_title']
    list_per_page = 10  


@admin.register(Skill)
class SkillsAdmin(admin.ModelAdmin):
    list_display = ['title','job', 'employee']
    list_per_page = 10  


@admin.register(JobRequest)
class JobRequestAdmin(admin.ModelAdmin):
    list_display = ['employee', 'created', 'job_request_status']
    list_per_page = 10   


@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_per_page = 10   