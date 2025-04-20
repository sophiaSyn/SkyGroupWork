from django.contrib import admin
from .models import Department, Team, Session, State, Trend, Card, Vote

# Register your models here.

admin.site.register(Department)
admin.site.register(Team)
admin.site.register(Session)
admin.site.register(State)
admin.site.register(Trend)
admin.site.register(Card)
admin.site.register(Vote)