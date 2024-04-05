from django.shortcuts import render
from .models import Event
from .forms import EventForm
from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

def landing_page(request):
    return render(request, 'events/landing.html')

def login_view(request):
    form = LoginForm(data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('Event:event_list')  
        else:
            form.add_error(None, 'Invalid username or password')

    return render(request, 'events/landing.html', {'form': form})

@login_required
def event_list(request):
    my_events = Event.objects.filter(participants=request.user)
    all_events = Event.objects.all()
    is_admin = request.user.is_staff
    context = {
        'my_events': my_events,
        'all_events': all_events,
        'is_admin': is_admin,  # Add this to your context
    }
    return render(request, 'events/events_list.html', context)

@login_required
def join_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user not in event.participants.all():
        event.participants.add(request.user)
    return redirect('Event:event_list')  

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # Load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            auth_login(request, user)
            return redirect('Event:event_list')  # Redirect to a home page or another appropriate page
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def custom_logout_view(request):
    logout(request)
    return redirect('Event:landing')
