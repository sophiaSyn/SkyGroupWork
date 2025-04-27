# In models.py

from django.db import models

class Department(models.Model):
    departmentNo = models.AutoField(primary_key=True)
    departmentName = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return self.departmentName

class Team(models.Model):
    teamID = models.AutoField(primary_key=True)
    teamName = models.CharField(max_length=20, unique=True)
    departmentNo = models.ForeignKey(Department, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.teamName

class User(models.Model):
    userID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)
    username = models.CharField(max_length=15, unique=True, null=False)
    email = models.EmailField(max_length=100, unique=True, null=False)
    password = models.CharField(max_length=15, null=False)
    teamID = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.username

class Role(models.Model):
    roleID = models.AutoField(primary_key=True)
    roleName = models.CharField(max_length=20, unique=True, null=False)
    votePermission = models.BooleanField(default=False, null=False)
    viewTeamSummary = models.BooleanField(default=False, null=False)
    viewDepartmentSummary = models.BooleanField(default=False, null=False)
    manageTeamsPermission = models.BooleanField(default=False, null=False)
    viewProgressPermission = models.BooleanField(default=False, null=False)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.roleName

# Add other models from your schema (States, Trends, Votes, Cards, etc.)