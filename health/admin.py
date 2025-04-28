from django.contrib import admin
from .models import Department, Team, Session, State, Trend, Card, Vote

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    pass

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    pass

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    pass

@admin.register(Trend)
class TrendAdmin(admin.ModelAdmin):
    pass

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('cardName', 'order')  # show cardName and order in Django admin
    ordering = ('order',)  # default order by 'order' field

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    pass
