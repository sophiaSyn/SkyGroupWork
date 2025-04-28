from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Department(models.Model):
    departmentNo = models.AutoField(primary_key=True) 
    departmentName = models.CharField(max_length=50) 

    def __str__(self):
        return self.departmentName
    
class Team(models.Model):
    teamID = models.AutoField(primary_key=True)
    teamName = models.CharField(max_length=50, unique=True)
    departmentNo = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.teamName

class Session(models.Model):
    sessionID = models.AutoField(primary_key=True)
    startDate = models.DateField()
    endDate = models.DateField()
    summary = models.TextField()
    progress = models.TextField()
    userID = models.ForeignKey('users.User', on_delete=models.CASCADE)
    teamID = models.ForeignKey(Team, on_delete=models.CASCADE)
    departmentNo = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"Session {self.sessionID} - {self.startDate} to {self.endDate}"
    
class State(models.Model):
    stateID = models.AutoField(primary_key=True)
    stateColour = models.CharField(max_length=5)

    def __str__(self):
        return self.stateColour
    
class Trend(models.Model):
    trendID = models.AutoField(primary_key=True)
    trendStatus = models.CharField(max_length=15)

    def __str__(self):
        return self.trendStatus 
    
class Card(models.Model):
    cardID = models.AutoField(primary_key=True)
    cardName = models.CharField(max_length=50)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.cardName

    
class Vote(models.Model):
    voteID = models.AutoField(primary_key=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    sessionID = models.ForeignKey(Session, on_delete=models.CASCADE)
    userID = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True, blank=True)  # 👈 Add null=True
    cardID = models.ForeignKey(Card, on_delete=models.CASCADE, null=True, blank=True)           # 👈 Add null=True
    stateID = models.ForeignKey(State, on_delete=models.CASCADE)
    trendID = models.ForeignKey(Trend, on_delete=models.CASCADE)
    comment = models.TextField(blank=True, null=True)                                           # 👈 Add null=True


    def __str__(self):
        return f"Vote {self.voteID} - Session {self.sessionID.sessionID}"
