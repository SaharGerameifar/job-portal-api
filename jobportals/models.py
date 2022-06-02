from django.db import models
from accounts.models import User
from datetime import datetime


GENDER_CHOICES = [
    ('N', 'Does not matter'),
    ('F', 'Female'),
    ('M', 'Male'),
]

DEGREE_LEVEL = [
    ('DI', 'Diploma'),
    ('BA', 'Bachelor'),
    ('MA', 'Master'),
    ('DO', 'Doctoral'),
    ('N', 'Does not matter'),
]

WORK_EXPERIENCE_CHOICES = [
    ('1-3', '1-3 years'),
    ('3-6', '3-6 years'),
    ('+6', '+6 years'),
    ('N', 'Does not matter'),
]

SALARY_CHOICES = [
    ('agreement', 'agreement'),
    ('3', 'from 3'),
    ('5', 'from 5'),
    ('8', 'from 8'),
    ('10', 'from 10'),
    ('12', 'from 12'),
    ('15', 'from 15'),
]

COOPERATION_CHOICES = [
    ('full', 'full-time'),
    ('part', 'part-time'),
    ('remote', 'remote'),
    ('internship', 'internship'),
]

JOB_REQUEST_STATUS = [
    ('P', 'Pending'),
    ('R', 'Rejected'),
    ('I', 'Interview'),
    ('H', 'Hire'),
    ]

YEAR_CHOICES = [(y,y) for y in range(1900, datetime.now().year)]
MONTH_CHOICES = [(m,m) for m in range(1,13)]
SKILL_LEVEL = [(n,n) for n in range(1,4)]


class State(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
 

class JobCategory(models.Model):
    title = models.CharField(max_length=255)
    
    def __str__(self):
        return self.title


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='N')
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    preferred_job_category = models.ForeignKey(JobCategory, on_delete=models.CASCADE, null=True, blank=True)
    expected_salary = models.IntegerField(null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    linkedin = models.CharField(max_length=255, null=True, blank=True, help_text='for example linkedin.com/in/username')


    def __str__(self):
        return f"{self.user.first_name}  {self.user.last_name}"


class EducationalBackground(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee_educationalbackground', null=True, blank=True)
    degree_level = models.CharField(max_length=2, choices=DEGREE_LEVEL)
    university = models.CharField(max_length=255)
    gpa = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    from_year = models.IntegerField(choices=YEAR_CHOICES, null=True, blank=True)
    from_month = models.IntegerField(choices=MONTH_CHOICES, null=True, blank=True)
    to_year = models.IntegerField(choices=YEAR_CHOICES, null=True, blank=True)
    to_month = models.IntegerField(choices=MONTH_CHOICES, null=True, blank=True)
    studying =  models.BooleanField(default=False, null=True, blank=True)        


class SkillCategory(models.Model):
    category = models.CharField(max_length=255)
    
    def __str__(self):
        return self.category


class WorkExperience(models.Model):
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE, related_name='employee_workexperience')
    job_title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    from_month = models.IntegerField(choices=MONTH_CHOICES, null=True, blank=True)
    from_year = models.IntegerField(choices=YEAR_CHOICES, null=True, blank=True)
    to_year = models.IntegerField(choices=YEAR_CHOICES, null=True, blank=True)
    to_month = models.IntegerField(choices=MONTH_CHOICES, null=True, blank=True)
    current_job = models.BooleanField()
    description = models.TextField(max_length=1000)


class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name_of_company = models.CharField(max_length=255, null=True, blank=True)
    website_url = models.CharField(max_length=255, null=True, blank=True, help_text='for example https://example.com')
    co_phone_number = models.CharField(max_length=20, null=True, blank=True)
    co_size = models.PositiveIntegerField(null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    co_introduction = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.name_of_company}"


class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255, null=True, blank=True)
    working_hoursand_days = models.CharField(max_length=255, help_text='for example: 9 AM-5 PM all day of week', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='N', null=True, blank=True)
    work_experience = models.CharField(max_length=10, choices=WORK_EXPERIENCE_CHOICES, null=True, blank=True)
    degree_level = models.CharField(max_length=2, choices=DEGREE_LEVEL, default='N', null=True, blank=True)
    salary = models.CharField(max_length=10, choices=SALARY_CHOICES, default='agreement', null=True, blank=True)
    cooperation_type = models.CharField(max_length=20, choices=COOPERATION_CHOICES, default='full', null=True, blank=True)
    facilities_and_benefits = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.job_title}"
    

class Skill(models.Model):
    title = models.CharField(max_length=255)
    skill_category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, null=True, blank=True)
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE, related_name='employee_skill', null=True, blank=True)
    job = models.ForeignKey(Job,on_delete=models.CASCADE, related_name='job_skill', null=True, blank=True)
    skill_level = models.IntegerField(choices=SKILL_LEVEL)


class JobRequest(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    cover_letter = models.TextField()
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    job_request_status = models.CharField(max_length=1, choices=JOB_REQUEST_STATUS, default='P')
    
    def __str__(self):
        return f"{self.employee.user.first_name} applied to {self.job.job_title}"

     