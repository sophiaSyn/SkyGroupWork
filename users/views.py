from django.shortcuts import render, redirect
from .models import User, Role
from .forms import SignUpForm, LoginForm
from django.contrib import messages

# View for the About Us Page (index.html) which is now the homepage
def index(request):
    return render(request, 'index.html')

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
                # Store user information in session
                request.session["user_id"] = user.userID
                request.session["username"] = user.username
                
                # Get the user's role
                try:
                    role = Role.objects.get(userID=user)
                    request.session["role"] = role.roleName
                except Role.DoesNotExist:
                    request.session["role"] = "No Role"
                
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
            name = form.cleaned_data["name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            role = form.cleaned_data["role"]
            team = form.cleaned_data["team"]
            
            if User.objects.filter(email=email).exists():
                form.add_error("email", "Email already exists.")
            elif User.objects.filter(username=username).exists():
                form.add_error("username", "Username already exists.")
            else:
                # Create the user
                user = User.objects.create(
                    name=name,
                    username=username,
                    email=email,
                    password=password,
                    teamID=team
                )
                
                # Associate the role with the user
                role.userID = user
                role.save()
                
                # Store user information in session
                request.session["user_id"] = user.userID
                request.session["username"] = user.username
                request.session["role"] = role.roleName
                
                return redirect("dashboard")
    else:
        form = SignUpForm()
    
    return render(request, "users/signup.html", {"form": form})

# Dashboard View
def dashboard_view(request):
    if "user_id" not in request.session:
        return redirect("login")  # Redirect to login if not logged in
    
    username = request.session.get("username")
    role = request.session.get("role")
    
    return render(request, "users/dashboard.html", {"username": username, "role": role})

# Log Out View
def logout_view(request):
    request.session.flush()
    return redirect("login")

# Home Redirect View
def home_redirect_view(request):
    if "user_id" in request.session:
        return redirect("dashboard")  # Redirect to dashboard if logged in
    else:
        return redirect("login")  # Redirect to login if not logged in