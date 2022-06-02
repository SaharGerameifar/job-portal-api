from rest_framework import routers
from .api_views import (StateViewSet, CityViewSet, JobCategoryViewSet, EmployeeViewSet,
                        WorkExperienceViewSet, SkillCategoryViewSet, SkillOfEmployeeViewSet,
                        EducationalBackgroundOfEmployeeViewSet, CompanyViewSet, JobViewSet,
                        JobRequestByEmployeeViewSet, JobRequestForCompanyViewSet) 


router = routers.DefaultRouter()
router.register('state', StateViewSet, basename='state')
router.register('city', CityViewSet, basename='city')
router.register('job_cat', JobCategoryViewSet, basename='job_cat')
router.register('employee', EmployeeViewSet, basename='employee')
router.register('work_exp', WorkExperienceViewSet, basename='work_exp')
router.register('skill_cat',SkillCategoryViewSet, basename='skill_cat')
router.register('skill_employee',SkillOfEmployeeViewSet, basename='skill_employee')
router.register('edu_bg_employee',EducationalBackgroundOfEmployeeViewSet, basename='edu_bg_employee')
router.register('company',CompanyViewSet, basename='company')
router.register('job',JobViewSet, basename='job')
router.register('req_job',JobRequestByEmployeeViewSet, basename='req_job')
router.register('co_req_job',JobRequestForCompanyViewSet, basename='co_req_job')