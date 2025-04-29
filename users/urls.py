from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # about us page (following basic html standards)
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('summary/', views.summary_view, name='summary'),  
    path('team-summary/', views.team_summary_view, name='team_summary'),  
    path('team-progress/', views.team_progress_view, name='team_progress'),
    path('select-card/', views.select_card_view, name='select_card'),
    path('card-progress/', views.card_progress_view, name='card_progress'),
]
