# job-portal-api

This project is an API for the job search site.
Backend uses the Django, DjangoRestFramework, and DjangoRestFramework-Simplejwt frameworks.
It is possible to register (by sending an activation email) and user login (company or job seeker).
The company can create job positions and edit own information and see the profile of job seekers and see the profile of job seekers who have applied for the job position defined by the company and change their request to one of four options Pending, Rejected, Interview and Hire.
Job seekers can see information about companies and other job seekers or edit own information. Job seekers can see the job ads submitted by the companies and submit a job application and see the result.


===========================================================

Installation guide:
create virtualenv and activate

pip install -r requirements.txt

cp .env-sample .env

python manage.py runserver
