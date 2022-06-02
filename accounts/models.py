from django.db import models
from django.contrib.auth.models import AbstractUser


ROLE_SELECTION = [
    ('E', 'employee'),
    ('C', 'company')
]


class User(AbstractUser):
    role = models.CharField(max_length=1, choices=ROLE_SELECTION)
   
    def __str__(self):
        return f'{self.email} - {self.role}'