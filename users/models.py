from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class User(models.Model):
    userId = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=15)
    roleId = models.ForeignKey('Role', on_delete=models.CASCADE)
    teamID = models.ForeignKey('health.Team', on_delete=models.CASCADE)

    def __str__(self):
        return self.username


class Role(models.Model):
    roleID = models.AutoField(primary_key=True)
    roleName = models.CharField(max_length=50)
    votePermission = models.BooleanField(default=False)
    viewTeamSummary = models.BooleanField(default=False)
    viewDepartmentSummary = models.BooleanField(default=False)
    manageTeamPermission = models.BooleanField(default=False)
    viewProgressPermission = models.BooleanField(default=False)

    def __str__(self):
        return self.roleName
    
