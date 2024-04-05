from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from Event.forms import EventForm
from Event.models import Event
from django.contrib.auth.models import User
from django.utils.dateparse import parse_date
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import JsonResponse


def is_admin(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(is_admin)
def dashboard(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            print(event+'added')
            return redirect('AdminPage:dashboard')
    else:
        form = EventForm()
        events = Event.objects.all()
        users = User.objects.all()  # Fetch users if needed for the dashboard
        return render(request, 'AdminPage/dashboard.html', {'form': form, 'users': users, 'events': events})

@user_passes_test(is_admin)
def add_event(request):
    if request.method == 'POST':
        event_form = EventForm(request.POST)
        if event_form.is_valid():
            event = event_form.save(commit=False)
            date_from = parse_date(request.POST.get('date_from'))
            date_to = parse_date(request.POST.get('date_to'))

            if date_from and date_to:
                event.start_date = date_from
                event.end_date = date_to
                event.save()
                messages.success(request, 'Event created successfully')  
            else:
                messages.error(request, 'There was a problem with the dates.')
            
            return redirect('Event:event_list')
        else:
            for error in event_form.errors:
                messages.error(request, f"{error}: {event_form.errors[error]}")
            return redirect('Event:event_list')
    else:
        event_form = EventForm()
        return render(request, 'AdminPage/addEvent.html', {'form': event_form})

@user_passes_test(is_admin)
def delete_user(request, user_id):
    if request.user.is_staff or request.user.id == user_id:
        try:
            user = get_object_or_404(User, id=user_id)
            user.delete()
            messages.success(request, 'User deleted successfully')
            return redirect('Event:event_list')
        except Exception as e:
            messages.error(request, 'User could not be deleted')
            return redirect('Event:event_list')
    else:
        messages.error(request, 'Unauthorized attempt to delete user')
        return redirect('Event:event_list')
    
@user_passes_test(lambda user: user.is_staff)
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('Event:event_list')
    else:
        form = EventForm(instance=event)
    
    # Render a dedicated edit event template
    return render(request, 'adminpage/editEvent.html', {'form': form, 'event': event})
    
@user_passes_test(is_admin)
def delete_event(request, event_id):
    if request.user.is_staff:
        try:
            event = get_object_or_404(Event, id=event_id)
            event.delete()
            messages.success(request, 'Event deleted successfully')
            return redirect('Event:event_list')
        except:
            messages.error(request, 'Event could not be deleted')
            return redirect('Event:event_list')
    else:
        messages.error(request, 'Unauthorized attempt to delete event')
        return HttpResponse('')

