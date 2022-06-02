from django.db import transaction
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import ROLE_SELECTION 
from .models import User
from jobportals.models import Employee, Company


class UserRegisterSerializer(RegisterSerializer):
    role = serializers.ChoiceField(choices=ROLE_SELECTION)
   
    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.role = self.data.get('role')
        user.save()
        if user.role == 'E':
            Employee.objects.create(user=user)
        elif user.role == 'C':
            Company.objects.create(user=user)
        return user
        

class UserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'first_name', 'last_name']
        read_only_fields = ['id', 'email', 'role']


