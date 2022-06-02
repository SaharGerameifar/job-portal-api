from rest_framework.viewsets import ModelViewSet
from .models import (City, State, JobCategory, Employee, WorkExperience, SkillCategory, Skill,
                    EducationalBackground, Company, Job, JobRequest)
from rest_framework.response import Response
from rest_framework import status
from .serializers import (CitySerializer, NestedCitySerializer, StateSerializer, JobCategorySerializer,
                            EmployeeSerializer, NestedEmployeeSerializer, WorkExperienceSerializer,
                            NestedWorkExperienceSerializer, SkillCategorySerializer, SkillEmployeeSerializer,
                             NestedSkillEmployeeSerializer,  EducationalBackgroundEmployeeSerializer,
                             NestedEducationalBackgroundEmployeeSerializer, CompanySerializer,
                             NestedCompanySerializer, JobSerializer, NestedJobSerializer,
                             JobRequestByEmployeeSerializer, NestedJobRequestByEmployeeSerializer,
                             JobRequestForCompanySerializer, NestedJobRequestForCompanySerializer)
from .permissions import (IsOwnerOrReadOnly, IsEmployeeOwnerOrReadOnly, IsCompanyOwnerOrReadOnly,
                         IsJobCompanyOwnerOrReadOnly, IsCompanyOrReadOnly, IsEmployeeOrReadOnly)
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class NestedSerializerMixin(ModelViewSet):
    read_serializer_class = None

    def get_serializer_class(self):
        if self.request.method.lower() == "get":
            return self.read_serializer_class
        return self.serializer_class


class CityViewSet(NestedSerializerMixin):
    serializer_class = CitySerializer
    queryset = City.objects.all()
    read_serializer_class = NestedCitySerializer
    
    
class StateViewSet(ModelViewSet):
    serializer_class = StateSerializer
    queryset = State.objects.all()


class SkillCategoryViewSet(ModelViewSet):
    serializer_class = SkillCategorySerializer
    queryset = SkillCategory.objects.all()


class JobCategoryViewSet(ModelViewSet):
    serializer_class = JobCategorySerializer
    queryset = JobCategory.objects.all()


class EmployeeViewSet(NestedSerializerMixin):
    serializer_class = EmployeeSerializer
    read_serializer_class = NestedEmployeeSerializer
    queryset = Employee.objects.all()   
      

    def update(self, request, pk= None, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        
        data ={
            "phone_number": request.POST.get("phone_number", None),
            "gender": request.POST.get("gender", None),
            "date_of_birth": request.POST.get("date_of_birth", None),
            "preferred_job_category": request.POST.get("preferred_job_category", None),
            "expected_salary": request.POST.get("expected_salary", None),
            "state": request.POST.get("state", None),
            "city": request.POST.get("city", None),
            "address": request.POST.get("address", None),
            "linkedin" : request.POST.get("linkedin", None),
            
        }
        _serializer = self.serializer_class(instance=instance, data=data, context={'user': user}, partial=True)
        if _serializer.is_valid():
            _serializer.save()
            return Response(data=_serializer.data, status=status.HTTP_201_CREATED)
        else:    
            return Response(data=_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsOwnerOrReadOnly] 
        else:
            permission_classes = [IsAdminUser]   
        return [permission() for permission in permission_classes]      


class WorkExperienceViewSet(NestedSerializerMixin):
    serializer_class = WorkExperienceSerializer
    read_serializer_class = NestedWorkExperienceSerializer
    
    def get_queryset(self):
        user = self.request.user
        queryset = WorkExperience.objects.all()
        queryset = queryset.filter(employee__user=user)    
        return queryset

    def create(self, request, *args, **kwargs):
        user = request.user
        _serializer = self.serializer_class(data=request.data, context={'user': user})
        if _serializer.is_valid():
            _serializer.save()
            return Response(data=_serializer.data, status=status.HTTP_201_CREATED)
        else:    
            return Response(data=_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    def update(self, request, pk= None, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        data ={
            "job_title" : request.POST.get("job_title", None),
            "company_name" : request.POST.get("company_name", None),
            "from_month": request.POST.get("from_month", None),
            "from_year" : request.POST.get("from_year", None),
            "to_month" : request.POST.get("to_month", None),
            "to_year" : request.POST.get("to_year", None),
            "state" : request.POST.get("state", None),
            "city" : request.POST.get("city", None),
            "current_job" : request.POST.get("current_job", None),
            "description" : request.POST.get("description", None),
        }
        _serializer = self.serializer_class(instance=instance, data=data, context={'user': user}, partial=True)
        if _serializer.is_valid():
            _serializer.save()
            return Response(data=_serializer.data, status=status.HTTP_201_CREATED)
        else:    
            return Response(data=_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsEmployeeOwnerOrReadOnly]    
        else:
            permission_classes = [IsEmployeeOrReadOnly]    
        return [permission() for permission in permission_classes]  


class SkillOfEmployeeViewSet(NestedSerializerMixin):
    serializer_class = SkillEmployeeSerializer
    read_serializer_class = NestedSkillEmployeeSerializer
        
    def get_queryset(self):
        user = self.request.user
        queryset = Skill.objects.all() 
        queryset = queryset.filter(employee__user=user)    
        return queryset
        
    def create(self, request, *args, **kwargs):
        user = request.user
        _serializer = self.serializer_class(data=request.data, context={'user': user})
        if _serializer.is_valid():
            _serializer.save()
            return Response(data=_serializer.data, status=status.HTTP_201_CREATED)
        else:    
            return Response(data=_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    def update(self, request, pk= None, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        data ={
            "title" : request.POST.get("title", None),
            "skill_category" : request.POST.get("skill_category", None),
            "skill_level": request.POST.get("skill_level", None),
            
        }
        _serializer = self.serializer_class(instance=instance, data=data, context={'user': user}, partial=True)
        if _serializer.is_valid():
            _serializer.save()
            return Response(data=_serializer.data, status=status.HTTP_201_CREATED)
        else:    
            return Response(data=_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'update', 'partial_update','destroy']:
            permission_classes = [IsEmployeeOwnerOrReadOnly]
        else:
            permission_classes = [IsEmployeeOrReadOnly]    
        return [permission() for permission in permission_classes]   


class EducationalBackgroundOfEmployeeViewSet(NestedSerializerMixin):
    serializer_class = EducationalBackgroundEmployeeSerializer
    read_serializer_class = NestedEducationalBackgroundEmployeeSerializer
    
    def get_queryset(self):
        user = self.request.user
        queryset = EducationalBackground.objects.all()  
        queryset = queryset.filter(employee__user=user)    
        return queryset
        
    def create(self, request, *args, **kwargs):
        user = request.user
        _serializer = self.serializer_class(data=request.data, context={'user': user})
        if _serializer.is_valid():
            _serializer.save()
            return Response(data=_serializer.data, status=status.HTTP_201_CREATED)
        else:    
            return Response(data=_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    def update(self, request, pk= None, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        data ={
            "university" : request.POST.get("university", None),
            "degree_level" : request.POST.get("degree_level", None),
            "from_year": request.POST.get("from_year", None),
            "from_month": request.POST.get("from_month", None),
            "to_year": request.POST.get("to_year", None),
            "to_month": request.POST.get("to_month", None),
            "gpa": request.POST.get("gpa", None),
            "studying": request.POST.get("studying", None),
        }
        _serializer = self.serializer_class(instance=instance, data=data, context={'user': user}, partial=True)
        if _serializer.is_valid():
            _serializer.save()
            return Response(data=_serializer.data, status=status.HTTP_201_CREATED)
        else:    
            return Response(data=_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'update', 'partial_update','destroy']:
            permission_classes = [IsEmployeeOwnerOrReadOnly]
        else:
            permission_classes = [IsEmployeeOrReadOnly]    
        return [permission() for permission in permission_classes]     


class CompanyViewSet(NestedSerializerMixin):
    serializer_class = CompanySerializer
    read_serializer_class = NestedCompanySerializer
    queryset = Company.objects.all()   
  
    def update(self, request, pk= None, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        
        data ={
            "name_of_company": request.POST.get("name_of_company", None),
            "website_url": request.POST.get("website_url", None),
            "co_phone_number": request.POST.get("co_phone_number", None),
            "co_size": request.POST.get("co_size", None),
            "state": request.POST.get("state", None),
            "city": request.POST.get("city", None),
            "co_introduction": request.POST.get("co_introduction", None),
                        
        }
        _serializer = self.serializer_class(instance=instance, data=data, context={'user': user}, partial=True)
        if _serializer.is_valid():
            _serializer.save()
            return Response(data=_serializer.data, status=status.HTTP_201_CREATED)
        else:    
            return Response(data=_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsOwnerOrReadOnly]     
        else:
            permission_classes = [IsAdminUser]     
        return [permission() for permission in permission_classes]      


class JobViewSet(NestedSerializerMixin):
    serializer_class = JobSerializer
    read_serializer_class = NestedJobSerializer
    queryset = Job.objects.all()   
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update','destroy']:
            permission_classes = [IsCompanyOwnerOrReadOnly] 
        else:  
            permission_classes = [IsCompanyOrReadOnly]         
        return [permission() for permission in permission_classes]
        
    def create(self, request, *args, **kwargs):
        user = request.user
        _serializer = self.serializer_class(data=request.data, context={'user': user})
        if _serializer.is_valid():
            _serializer.save()
            return Response(data=_serializer.data, status=status.HTTP_201_CREATED)
        else:    
            return Response(data=_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    def update(self, request, pk= None, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        data ={
            "job_title" : request.POST.get("job_title", None),
            "working_hoursand_days" : request.POST.get("working_hoursand_days", None),
            "created_date": request.POST.get("created_date", None),
            "gender" : request.POST.get("gender", None),
            "work_experience" : request.POST.get("work_experience", None),
            "degree_level" : request.POST.get("degree_level", None),
            "salary" : request.POST.get("salary", None),
            "cooperation_type" : request.POST.get("cooperation_type", None),
            "facilities_and_benefits" : request.POST.get("facilities_and_benefits", None),
            "description" : request.POST.get("description", None),
           
        }
        _serializer = self.serializer_class(instance=instance, data=data, context={'user': user}, partial=True)
        if _serializer.is_valid():
            _serializer.save()
            return Response(data=_serializer.data, status=status.HTTP_201_CREATED)
        else:    
            return Response(data=_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


class JobRequestByEmployeeViewSet(NestedSerializerMixin):
    serializer_class = JobRequestByEmployeeSerializer
    read_serializer_class = NestedJobRequestByEmployeeSerializer
    
    def get_queryset(self):
        user = self.request.user
        queryset = JobRequest.objects.all()  
        queryset = queryset.filter(employee__user=user)    
        return queryset

    def create(self, request, *args, **kwargs):
        user = request.user
        
        _serializer = self.serializer_class(data=request.data, context={'user': user })
        if _serializer.is_valid():
            _serializer.save()
            return Response(data=_serializer.data, status=status.HTTP_201_CREATED)
        else:    
            return Response(data=_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        
    def get_permissions(self):
        if self.action in ['list', 'retrieve','update', 'partial_update','destroy']:
            permission_classes = [IsEmployeeOwnerOrReadOnly] 
        else:
            permission_classes = [IsEmployeeOrReadOnly]         
        return [permission() for permission in permission_classes]  


class JobRequestForCompanyViewSet(NestedSerializerMixin):
    serializer_class = JobRequestForCompanySerializer
    read_serializer_class = NestedJobRequestForCompanySerializer
  
    def get_queryset(self):
        user = self.request.user
        queryset = JobRequest.objects.all() 
        queryset = queryset.filter(job__company__user=user)    
        return queryset
  
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsJobCompanyOwnerOrReadOnly]   
        else:
            permission_classes = [IsAdminUser]   
        return [permission() for permission in permission_classes] 

    def update(self, request, pk= None, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        
        data ={
            "job_request_status": request.POST.get("job_request_status", None),
             }
        _serializer = self.serializer_class(instance=instance, data=data, context={'user': user}, partial=True)
        if _serializer.is_valid():
            _serializer.save()
            return Response(data=_serializer.data, status=status.HTTP_201_CREATED)
        else:    
            return Response(data=_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

          

