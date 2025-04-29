from django.shortcuts import render, redirect
from .models import User
from .forms import SignUpForm, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from users.models import User as CustomUser
from django.contrib.auth.decorators import login_required
from health.models import Vote, Department, Team, State, Session, Card
from users.models import Role
from django.shortcuts import get_object_or_404
from collections import defaultdict

# about us view
def index(request):
    return render(request, 'index.html')  

# login View
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data["identifier"]
            password = form.cleaned_data["password"]

            try:
                user = User.objects.get(email=identifier, password=password)
            except User.DoesNotExist:
                try:
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



# sign up view
from django.contrib.auth.hashers import make_password

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            role = form.cleaned_data["role"]
            team = form.cleaned_data["team"]

            # check if email or username already exists
            if User.objects.filter(email=email).exists():
                form.add_error("email", "Email already exists.")
            elif User.objects.filter(username=username).exists():
                form.add_error("username", "Username already exists.")
            else:
                user = User.objects.create(
                    username=username,
                    email=email,
                    roleId=role,
                    teamID=team
                )
                
                user.password = make_password(password)
                user.save()

                request.session["user_id"] = user.userId
                request.session["username"] = user.username
                request.session["role"] = role.roleName
                return redirect("dashboard")
    else:
        form = SignUpForm()

    return render(request, "users/signup.html", {"form": form})


# dashboard view
def dashboard_view(request):
    if 'user_id' not in request.session:
        return redirect("login")

    try:
        user = CustomUser.objects.get(userId=request.session['user_id'])
    except CustomUser.DoesNotExist:
        return redirect("login")

    role = request.session.get('role')

    context = {
        "username": user.username,
        "role_name": user.roleId.roleName,
        "custom_user": user
    }

    if role == "Team Leader":
        
        team_votes = Vote.objects.filter(userID__teamID=user.teamID)
        
        red_count = team_votes.filter(stateID__stateColour="RED").count()
        amber_count = team_votes.filter(stateID__stateColour="AMBER").count()
        green_count = team_votes.filter(stateID__stateColour="GREEN").count()

        context.update({
            "team_summary": {
                "Red": red_count,
                "Amber": amber_count,
                "Green": green_count
            }
        })
        print("Logged in session:", request.session.get('user_id'))

    return render(request, "users/dashboard.html", context)

# log out view
def logout_view(request):
    request.session.flush()
    return redirect("login")

# home redirect view 
def home_redirect_view(request):
    if "user_id" in request.session:
        return redirect("dashboard")  
    else:
        return redirect("index")  



def summary_view(request):
    if 'user_id' not in request.session:
        return redirect('login')

    try:
        user = User.objects.get(userId=request.session['user_id'])  
    except User.DoesNotExist:
        return redirect('login')

    # fetch only completed sessions 
    completed_sessions = Session.objects.all()

    # department summary
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

    # team summary
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

def team_summary_view(request):
    if 'user_id' not in request.session:
        return redirect('login')

    try:
        user = CustomUser.objects.get(userId=request.session['user_id'])
    except CustomUser.DoesNotExist:
        return redirect('login')

    role = request.session.get('role')

    if role != "Team Leader":
        return redirect('dashboard')  

    
    team_votes = Vote.objects.filter(userID__teamID=user.teamID)

    red_count = team_votes.filter(stateID__stateColour="RED").count()
    amber_count = team_votes.filter(stateID__stateColour="AMBER").count()
    green_count = team_votes.filter(stateID__stateColour="GREEN").count()

    context = {
        'team_name': user.teamID.teamName,
        'team_summary': {
            'Red': red_count,
            'Amber': amber_count,
            'Green': green_count,
        }
    }

    return render(request, 'users/team_summary.html', context)



def team_progress_view(request):
    if 'user_id' not in request.session:
        return redirect('login')

    try:
        user = CustomUser.objects.get(userId=request.session['user_id'])
    except CustomUser.DoesNotExist:
        return redirect('login')

    role = request.session.get('role')

    if role != "Team Leader":
        return redirect('dashboard')

    
    sessions = Session.objects.all().order_by('startDate')

    
    session_labels = []
    red_counts = []
    amber_counts = []
    green_counts = []

    for session in sessions:
        votes = Vote.objects.filter(sessionID=session, userID__teamID=user.teamID)
        red_count = votes.filter(stateID__stateColour="RED").count()
        amber_count = votes.filter(stateID__stateColour="AMBER").count()
        green_count = votes.filter(stateID__stateColour="GREEN").count()

        session_labels.append(str(session.startDate))   
        red_counts.append(red_count)
        amber_counts.append(amber_count)
        green_counts.append(green_count)

    context = {
        'team_name': user.teamID.teamName,
        'session_labels': session_labels,
        'red_counts': red_counts,
        'amber_counts': amber_counts,
        'green_counts': green_counts,
    }

    return render(request, 'users/team_progress.html', context)



def select_card_view(request):
    if 'user_id' not in request.session:
        return redirect('login')

    cards = Card.objects.all().order_by('order')  

    return render(request, 'users/select_card.html', {
        'cards': cards,
    })



def card_progress_view(request):
    if 'user_id' not in request.session:
        return redirect('login')

    card_id = request.GET.get('card')
    if not card_id:
        return redirect('select_card')

    try:
        selected_card = Card.objects.get(cardID=card_id)
    except Card.DoesNotExist:
        return redirect('select_card')

    try:
        current_user = User.objects.get(userId=request.session['user_id'])
    except User.DoesNotExist:
        return redirect('login')

    # get the team of the current user
    user_team = current_user.teamID

    # find all users in that team
    team_users = User.objects.filter(teamID=user_team)

    # find all votes by those users for the selected card
    votes = Vote.objects.filter(
        userID__in=team_users,
        cardID=selected_card
    )

    # group votes by session date
    votes_by_date = defaultdict(lambda: {'RED': 0, 'AMBER': 0, 'GREEN': 0})

    for vote in votes:
        session_date = vote.sessionID.startDate.strftime('%Y-%m-%d')
        if vote.stateID.stateColour == 'RED':
            votes_by_date[session_date]['RED'] += 1
        elif vote.stateID.stateColour == 'AMBER':
            votes_by_date[session_date]['AMBER'] += 1
        elif vote.stateID.stateColour == 'GREEN':
            votes_by_date[session_date]['GREEN'] += 1

    if votes_by_date:
        session_labels = sorted(votes_by_date.keys())
        red_counts = [votes_by_date[date]['RED'] for date in session_labels]
        amber_counts = [votes_by_date[date]['AMBER'] for date in session_labels]
        green_counts = [votes_by_date[date]['GREEN'] for date in session_labels]
    else:
        session_labels = []
        red_counts = []
        amber_counts = []
        green_counts = []

    context = {
        'selected_card': selected_card,
        'session_labels': session_labels,
        'red_counts': red_counts,
        'amber_counts': amber_counts,
        'green_counts': green_counts,
    }

    return render(request, 'users/card_progress.html', context)



