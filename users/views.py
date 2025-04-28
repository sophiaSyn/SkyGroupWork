from django.shortcuts import render, redirect
from .models import User
from .forms import SignUpForm, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from users.models import User as CustomUser
from django.contrib.auth.decorators import login_required
from health.models import Vote, Department, Team, State, Session
from users.models import Role

# View for the About Us Page (index.html) which is now the homepage
def index(request):
    return render(request, 'index.html')  # This is the About Us page now

# Login View
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data["identifier"]
            password = form.cleaned_data["password"]

            try:
                # Try finding by email first
                user = User.objects.get(email=identifier, password=password)
            except User.DoesNotExist:
                try:
                    # Then try by username
                    user = User.objects.get(username=identifier, password=password)
                except User.DoesNotExist:
                    user = None

            if user:
                request.session["user_id"] = user.userId
                request.session["username"] = user.username
                request.session["role"] = user.roleId.roleName
                return redirect("dashboard")
            else:
                messages.error(request, "Invalid login credentials.")
    else:
        form = LoginForm()

    return render(request, "users/login.html", {"form": form})

# Sign Up View
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            role = form.cleaned_data["role"]
            team = form.cleaned_data["team"]

            if User.objects.filter(email=email).exists():
                form.add_error("email", "Email already exists.")
            else:
                user = User.objects.create(
                    username=username,
                    email=email,
                    password=password,
                    roleId=role,
                    teamID=team
                )
                request.session["user_id"] = user.userId
                request.session["username"] = user.username
                request.session["role"] = role.roleName
                return redirect("dashboard")
    else:
        form = SignUpForm()

    return render(request, "users/signup.html", {"form": form})

# Dashboard View
def dashboard_view(request):
    if 'user_id' not in request.session:
        return redirect("login")

    try:
        user = CustomUser.objects.get(userId=request.session['user_id'])
    except CustomUser.DoesNotExist:
        return redirect("login")

    return render(request, "users/dashboard.html", {
        "username": user.username,
        "role_name": user.roleId.roleName,  # Pass roleName directly
        "custom_user": user  # Full user object if needed
    })

# Log Out View
def logout_view(request):
    request.session.flush()
    return redirect("login")

# Home Redirect View (Redirect to About Us page or Dashboard)
def home_redirect_view(request):
    if "user_id" in request.session:
        return redirect("dashboard")  # Redirect to dashboard if logged in
    else:
        return redirect("login")  # Redirect to login if not logged in



def summary_view(request):
    if 'user_id' not in request.session:
        return redirect('login')

    try:
        user = User.objects.get(userId=request.session['user_id'])  # Make sure you imported your correct User model
    except User.DoesNotExist:
        return redirect('login')

    # Fetch only completed sessions (future-proof)
    completed_sessions = Session.objects.all()

    # Department Summary
    departments = Department.objects.all()
    department_data = {}

    for department in departments:
        votes = Vote.objects.filter(
            sessionID__in=completed_sessions,
            userID__teamID__departmentNo=department
        )
        red_count = votes.filter(stateID__stateColour="RED").count()
        amber_count = votes.filter(stateID__stateColour="AMBER").count()
        green_count = votes.filter(stateID__stateColour="GREEN").count()

        if red_count > 0 or amber_count > 0 or green_count > 0:
            department_data[department.departmentName] = {
                "Red": red_count,
                "Amber": amber_count,
                "Green": green_count,
            }

    # Team Summary
    teams = Team.objects.all()
    team_data = {}

    for team in teams:
        votes = Vote.objects.filter(
            sessionID__in=completed_sessions,
            userID__teamID=team.teamID
        )
        red_count = votes.filter(stateID__stateColour="RED").count()
        amber_count = votes.filter(stateID__stateColour="AMBER").count()
        green_count = votes.filter(stateID__stateColour="GREEN").count()

        if red_count > 0 or amber_count > 0 or green_count > 0:
            team_data[team.teamName] = {
                "Red": red_count,
                "Amber": amber_count,
                "Green": green_count,
            }

    return render(request, 'health/summary.html', {
        'department_data': department_data,
        'team_data': team_data,
    })
