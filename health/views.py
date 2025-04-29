from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Vote, State, Session, Card, Trend, Team, Department
from users.models import User

from datetime import date, timedelta

@csrf_exempt
def vote_view(request):
    if 'user_id' not in request.session:
        return redirect('login')

    user_id = request.session['user_id']
    user = User.objects.get(userId=user_id)

    cards = Card.objects.all().order_by('order')

    # check for active session
    active_sessions = Session.objects.filter(userID=user).order_by('-startDate')

    if active_sessions.exists():
        session = active_sessions.first()
    else:
        today = date.today()
        tomorrow = today + timedelta(days=1)

        session = Session.objects.create(
            startDate=today,
            endDate=tomorrow,
            summary=f"Voting session for {user.username} starting {today}",
            progress="Started",
            userID=user,
            teamID=user.teamID,
            departmentNo=user.teamID.departmentNo,
        )

    sessions = [session]

    if request.method == "POST":
        data = request.POST
        selected_session_id = data.get('session')
        selected_session = Session.objects.get(sessionID=selected_session_id)

        for card in cards:
            vote_value = data.get(f'vote_{card.cardID}')
            trend_value = data.get(f'trend_{card.cardID}')
            comment_text = data.get(f'comment_{card.cardID}', '').strip()

            if vote_value:
                Vote.objects.create(
                    sessionID=selected_session,
                    userID=user, 
                    stateID=State.objects.get(stateColour=vote_value),
                    trendID=Trend.objects.get(trendStatus=trend_value),
                    cardID=card,
                    comment=comment_text,
                )

        return JsonResponse({"success": True})

    context = {
        'user': user,
        'cards': cards,
        'sessions': sessions,
    }
    return render(request, 'health/vote.html', context)
