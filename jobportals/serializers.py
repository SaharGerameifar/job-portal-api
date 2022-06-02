from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import (Employee, WorkExperience, Skill, EducationalBackground, JobCategory,
                     State, City, SkillCategory, Company, Job, JobRequest)
from accounts.serializers import UserDetailsSerializer


class StateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = State
        fields = ['name']
                

class CitySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = City
        fields = ['name', 'state']


class NestedCitySerializer(serializers.ModelSerializer):
    state = StateSerializer()

    class Meta:
        model = City
        fields = ['name', 'state']        


class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = ['title']


class SkillCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillCategory
        fields = ['category']


class EmployeeWorkExpSerializer(serializers.ModelSerializer):
    state = StateSerializer()
    city = CitySerializer()

    class Meta:
        model = WorkExperience
        fields = ['job_title', 'company_name', 'state', 'city', 'from_month',
                    'from_year', 'to_month', 'to_year', 'current_job', 'description' ] 


class SkillSerializer(serializers.ModelSerializer):
    skill_category = SkillCategorySerializer()
    class Meta:
        model = Skill
        fields = ['title', 'skill_category', 'skill_level'] 


class EducationalBackgroundSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = EducationalBackground
        fields = ['university', 'degree_level', 'from_year', 'from_month', 'to_year', 'to_month',   
                'gpa', 'studying'] 


class EmployeeSerializer(serializers.ModelSerializer):
    user = UserDetailsSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = ['user', 'gender', 'phone_number', 'date_of_birth', 'preferred_job_category',
                    'expected_salary', 'state', 'city', 'address', 'linkedin' ]   
        

class NestedEmployeeSerializer(serializers.ModelSerializer):
    state = StateSerializer()
    city = CitySerializer()
    preferred_job_category = JobCategorySerializer()
    employee_workexperience = serializers.SerializerMethodField("get_work_exp", read_only=True)
    employee_skill = serializers.SerializerMethodField("get_skill", read_only=True)
    employee_educationalbackground = serializers.SerializerMethodField("get_edu", read_only=True)
    user = serializers.SerializerMethodField("get_user", read_only=True)

    def get_user(self, obj):
        return {"email": obj.user.email,
                "first_name": obj.user.first_name,
                "last_name": obj.user.last_name }

    def get_work_exp(self, obj):
        works_exp = obj.employee_workexperience.all()
        return EmployeeWorkExpSerializer(works_exp, many=True).data

    def get_skill(self, obj):
        skill = obj.employee_skill.all()
        return SkillSerializer(skill, many=True).data

    def get_edu(self, obj):
        edu = obj.employee_educationalbackground.all()
        return EducationalBackgroundSerializer(edu, many=True).data

    # def create(self, validated_data):
    #     user_username = validated_data.get('user').username
    #     employee = Employee.objects.create(**validated_data)
    #     return employee

    def update(self, instance, validated_data):
        instance.phone_number = validated_data.get("phone_number", instance.phone_number),
        instance.gender = validated_data.get("gender", instance.gender),
        instance.date_of_birth = validated_data.get("date_of_birth", instance.date_of_birth),
        instance.preferred_job_category = validated_data.get("preferred_job_category", instance.preferred_job_category),
        instance.expected_salary = validated_data.get("expected_salary", instance.expected_salary),
        instance.state = validated_data.get("state", instance.state),
        instance.city = validated_data.get("city", instance.city),
        instance.address = validated_data.get("address", instance.address),
        instance.linkedin = validated_data.get("linkedin", instance.linkedin),
        instance.user = self.context['user']
        instance.save()
        return instance

    class Meta:
        model = Employee
        fields = ['user', 'gender', 'phone_number', 'date_of_birth', 'preferred_job_category',
                    'expected_salary', 'state', 'city', 'address', 'linkedin', 'employee_workexperience',
                     'employee_skill', 'employee_educationalbackground' ]   


class WorkExperienceSerializer(serializers.ModelSerializer):
    
    def create(self, validated_data):
        if self.context['user']:
            user = self.context['user']
            employee = Employee.objects.get(user=user)
            validated_data['employee'] = employee
        work_exp = WorkExperience.objects.create(**validated_data)
        return work_exp  

    class Meta:
        model = WorkExperience
        fields = ['job_title', 'company_name', 'state', 'city', 'from_month',
                    'from_year', 'to_month', 'to_year', 'current_job', 'description' ] 


class NestedWorkExperienceSerializer(serializers.ModelSerializer):
    state = StateSerializer()
    city = CitySerializer()
    employee = serializers.SerializerMethodField("get_employee", read_only=True)

    def get_employee(self, obj):
        return {"email": obj.employee.user.email,
                "first_name": obj.employee.user.first_name,
                "last_name": obj.employee.user.last_name }

    def update(self, instance, validated_data):
        instance.job_title = validated_data.get("job_title", instance.job_title),
        instance.company_name = validated_data.get("company_name", instance.company_name),
        instance.from_month = validated_data.get("from_month", instance.from_month),
        instance.from_year = validated_data.get("from_year", instance.from_year),
        instance.to_month = validated_data.get("to_month", instance.to_month),
        instance.to_year = validated_data.get("to_year", instance.to_year),
        instance.state = validated_data.get("state", instance.state),
        instance.city = validated_data.get("city", instance.city),
        instance.current_job = validated_data.get("current_job", instance.current_job),
        instance.description = validated_data.get("description", instance.description),
        user = self.context['user']
        employee = Employee.objects.get(user=user)
        instance.employee = employee
        instance.save()
        return instance

    class Meta:
        model = WorkExperience
        fields = ['employee', 'job_title', 'company_name', 'state', 'city', 'from_month',
                    'from_year', 'to_month', 'to_year', 'current_job', 'description' ]   


class SkillEmployeeSerializer(serializers.ModelSerializer):
    
    def create(self, validated_data):
        if self.context['user']:
            user = self.context['user']
            employee = Employee.objects.get(user=user)
            validated_data['employee'] = employee
        skill = Skill.objects.create(**validated_data)
        return skill  

    class Meta:
        model = Skill
        fields = ['title', 'skill_category', 'skill_level' ] 


class NestedSkillEmployeeSerializer(serializers.ModelSerializer):
    skill_category = SkillCategorySerializer()
    employee = serializers.SerializerMethodField("get_employee", read_only=True)

    def get_employee(self, obj):
        return {"email": obj.employee.user.email,
                "first_name": obj.employee.user.first_name,
                "last_name": obj.employee.user.last_name }

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title),
        instance.skill_category = validated_data.get("skill_category", instance.skill_category),
        instance.skill_level = validated_data.get("skill_level", instance.skill_level),
        user = self.context['user']
        employee = Employee.objects.get(user=user)
        instance.employee = employee
        instance.save()
        return instance

    class Meta:
        model = Skill
        fields = ['title', 'skill_category', 'employee', 'skill_level' ]   


class EducationalBackgroundEmployeeSerializer(serializers.ModelSerializer):
    
    def create(self, validated_data):
        if self.context['user']:
            user = self.context['user']
            employee = Employee.objects.get(user=user)
            validated_data['employee'] = employee
        edu_bg =EducationalBackground.objects.create(**validated_data)
        return edu_bg  

    class Meta:
        model = EducationalBackground
        fields = ['university', 'degree_level', 'from_year', 'from_month', 'to_year', 'to_month',   
                'gpa', 'studying'] 


class NestedEducationalBackgroundEmployeeSerializer(serializers.ModelSerializer):
    employee = serializers.SerializerMethodField("get_employee", read_only=True)

    def get_employee(self, obj):
        return {"email": obj.employee.user.email,
                "first_name": obj.employee.user.first_name,
                "last_name": obj.employee.user.last_name }

    def update(self, instance, validated_data):
        instance.university = validated_data.get("university", instance.university),
        instance.degree_level = validated_data.get("degree_level", instance.degree_level),
        instance.from_year = validated_data.get("from_year", instance.from_year),
        instance.from_month = validated_data.get("from_month", instance.from_month),
        instance.to_year = validated_data.get("to_year", instance.to_year),
        instance.to_month = validated_data.get("to_month", instance.to_month),
        instance.gpa = validated_data.get("gpa", instance.gpa),
        instance.studying = validated_data.get("studying", instance.studying),
        user = self.context['user']
        employee = Employee.objects.get(user=user)
        instance.employee = employee
        instance.save()
        return instance

    class Meta:
        model = EducationalBackground
        fields = ['employee', 'university', 'degree_level', 'from_year', 'from_month', 'to_year', 'to_month',   
                'gpa', 'studying'] 


class CompanySerializer(serializers.ModelSerializer):
    user = UserDetailsSerializer(read_only=True)
    class Meta:
        model = Company
        fields = ['user', 'name_of_company', 'website_url', 'co_phone_number', 'co_size',
                    'state', 'city', 'co_introduction' ]   
        

class NestedCompanySerializer(serializers.ModelSerializer):
    state = StateSerializer()
    city = CitySerializer()
    user = serializers.SerializerMethodField("get_user", read_only=True)

    def get_user(self, obj):
        return {"email": obj.user.email}

    def update(self, instance, validated_data):
        instance.name_of_company = validated_data.get("name_of_company", instance.name_of_company),
        instance.website_url = validated_data.get("website_url", instance.website_url),
        instance.co_phone_number = validated_data.get("co_phone_number", instance.co_phone_number),
        instance.co_size = validated_data.get("co_size", instance.co_size),
        instance.state = validated_data.get("state", instance.state),
        instance.city = validated_data.get("city", instance.city),
        instance.co_introduction = validated_data.get("co_introduction", instance.co_introduction),
        instance.user = self.context['user']
        instance.save()
        return instance

    class Meta:
        model = Company
        fields = ['user', 'name_of_company', 'website_url', 'co_phone_number', 'co_size',
                    'state', 'city', 'co_introduction' ] 


class SkillCompanySerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Skill
        fields = ['title', 'skill_level' ] 


class JobSerializer(serializers.ModelSerializer):
    job_skill= SkillCompanySerializer(many=True)
    
    def create(self, validated_data):
        skills_data = validated_data.pop('job_skill')
        if self.context['user']:
            user = self.context['user']
            company = Company.objects.get(user=user)
            validated_data['company'] = company
        job = Job.objects.create(**validated_data)
        for i in range(len(skills_data)):
            Skill.objects.create(job=job, **skills_data[i])
        return job  
   
    class Meta:
        model = Job
        fields = ['job_title', 'working_hoursand_days', 'created_date', 'gender', 'work_experience',
                    'degree_level', 'salary', 'cooperation_type', 'facilities_and_benefits', 'description',
                    'job_skill'] 


class NestedJobSerializer(serializers.ModelSerializer):
    company = NestedCompanySerializer(read_only=True)
    job_skill= SkillCompanySerializer(many=True)

    def update(self, instance, validated_data):
        instance.job_title = validated_data.get("job_title", instance.job_title),
        instance.working_hoursand_days = validated_data.get("working_hoursand_days", instance.working_hoursand_days),
        instance.created_date = validated_data.get("created_date", instance.created_date),
        instance.gender = validated_data.get("gender", instance.gender),
        instance.work_experience = validated_data.get("work_experience", instance.work_experience),
        instance.degree_level = validated_data.get("degree_level", instance.degree_level),
        instance.salary = validated_data.get("salary", instance.salary),
        instance.cooperation_type = validated_data.get("cooperation_type", instance.cooperation_type),
        instance.facilities_and_benefits = validated_data.get("facilities_and_benefits", instance.facilities_and_benefits),
        instance.description = validated_data.get("description", instance.description),
        user = self.context['user']
        company = Company.objects.get(user=user)
        instance.company = company
        instance.save()
        return instance  

    class Meta:
        model = Job
        fields = ['company', 'job_title', 'working_hoursand_days', 'created_date', 'gender', 'work_experience',
                    'degree_level', 'salary', 'cooperation_type', 'facilities_and_benefits', 'description',
                    'job_skill' ] 
   

class JobRequestByEmployeeSerializer(serializers.ModelSerializer):
    
    def create(self, validated_data):
        if self.context['user']:
            user = self.context['user']
            employee = Employee.objects.get(user=user)
            validated_data['employee'] = employee
        job_req =JobRequest.objects.create(**validated_data)
        return job_req  

    class Meta:
        model = JobRequest
        fields = ['cover_letter', 'created', 'job'] 


class NestedJobRequestByEmployeeSerializer(serializers.ModelSerializer):
    employee = serializers.SerializerMethodField("get_employee", read_only=True)
    job = NestedJobSerializer(read_only=True)

    def get_employee(self, obj):
        return {"email": obj.employee.user.email,
                "first_name": obj.employee.user.first_name,
                "last_name": obj.employee.user.last_name }

    class Meta:
        model = JobRequest
        fields = ['employee', 'job', 'cover_letter', 'created', 'job_request_status']  


class JobRequestForCompanySerializer(serializers.ModelSerializer):
           
    class Meta:
        model = JobRequest
        fields = ['job_request_status'] 


class NestedJobRequestForCompanySerializer(serializers.ModelSerializer):
    employee = serializers.HyperlinkedIdentityField(view_name='employee-detail')
    job = NestedJobSerializer(read_only=True)
    
    def update(self, instance, validated_data):
        instance.job_request_status = validated_data.get("job_request_status", instance.job_request_status),
        instance.user = self.context['user']
        instance.save()
        return instance

    class Meta:
        model = JobRequest
        fields = ['employee', 'job', 'cover_letter', 'created', 'job_request_status']  

