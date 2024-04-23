from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Apiary
from .models import Keeper
from .models import Hive
from .models import Calendar
from .models import Event

from .forms import HiveForm
from .forms import ApiaryForm
from .forms import EventForm

#authentication
from django.contrib.auth import authenticate, login, logout
from .decorators import unauthenticated_user, allowed_users
from django.contrib import messages
from django.contrib.auth.models import Group
from .forms import CreateUserForm
from .forms import BeekeeperForm
#this is for class-based views:
from django.contrib.auth.mixins import LoginRequiredMixin
#I'm using the login_required tag to achieve the same thing

#permissions
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from .decorators import allowed_users

from django.shortcuts import redirect

#for resizing the image as it's recieved
from PIL import Image
from io import BytesIO

#calendars:
from datetime import datetime
from django.views import generic
from django.utils.safestring import mark_safe
from .utils import Calendar

from django.db.models.signals import post_save
from django.dispatch import receiver

import calendar
from datetime import timedelta
from django.http import HttpResponseRedirect

# Create your views here.
def index(request):
    #render index.html

    all_apiarys = Apiary.objects.all() 

    return render( request, 'beekeeping_app/index.html', {'Apiaries': all_apiarys})

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['beekeeper_role'])
#want them to be able to view all keepers when not logged in
def keeperView(request):
    all_keepers = Keeper.objects.all()
    #pass all keepers to the html file 
    return render(request, 'beekeeping_app/keepers.html', {'Keepers': all_keepers})

def apiaryDetail(request, apiary):
    apiary_instance = Apiary.objects.get(pk=apiary) #getting the specific id of the apiary being viewed
    #pass the id to the html file so it can display the specific details
    return render(request, 'beekeeping_app/apiary-detail.html', {'apiary': apiary_instance})

def keeperDetail(request, keeper):
    keeper_instance = Keeper.objects.get(pk=keeper)
    return render(request, 'beekeeping_app/keeper-detail.html', {'keeper': keeper_instance})

def hiveDetail(request, hive):
    hive_instance = Hive.objects.get(pk=hive)
    #for calendar:
    #events = Event.objects.filter(hive=hive)
    #return render(request, 'beekeeping_app/hive-detail.html', {'hive': hive, 'events': events})
    return render(request, 'beekeeping_app/hive-detail.html', {'hive': hive_instance})


#new should show an empty form - when submitted it adds that hive to the keeper's apiary
@login_required(login_url='login')
@allowed_users(allowed_roles=['beekeeper_role'])
def newHive(request, apiary_id):
    apiary_instance = Apiary.objects.get(pk=apiary_id)

    #can do this because of our reverse reference
    if apiary_instance.keeper.user != request.user:
        raise PermissionDenied("You don't have permission to edit this hive.")
    
    if request.method == "POST":
        hive_form = HiveForm(request.POST)
        if hive_form.is_valid():
            hive = hive_form.save(commit=False)
            hive.apiary = apiary_instance  #associate the hive with the apiary
            hive.save()

            #calendar_instance = Calendar.objects.create(hive=hive)

            return redirect('hive-detail', hive.id)
    else:
        hive_form = HiveForm()

    return render(request, 'beekeeping_app/create_hive.html', {'apiary': apiary_instance, 'form': hive_form})


#update should show the existing hive with the fields filled and editable
@login_required(login_url='login')
@allowed_users(allowed_roles=['beekeeper_role'])
def updateHive(request, apiary, hive):
    apiary_instance = Apiary.objects.get(id=apiary)
    hive_instance = Hive.objects.get(id=hive)

    if apiary_instance.keeper.user != request.user:
        raise PermissionDenied("You don't have permission to edit this hive.")
    
    if request.method == "POST":
        form = HiveForm(request.POST, instance=hive_instance)
        if form.is_valid():
            form.save()
            return redirect('hive-detail', hive_instance.id) 
    else:
        form = HiveForm(instance=hive_instance)

    return render(request, 'beekeeping_app/update_hive.html', {'apiary': apiary_instance, 'hive': hive_instance, 'form': form})


#delete should show a 'Are you sure you want to delete 'Hive Name'?' 
#Cancel (brings back to apiary-detail) Submit (deletes the hive)
@login_required(login_url='login')
@allowed_users(allowed_roles=['beekeeper_role'])
def deleteHive(request, apiary, hive):
    apiary_instance = Apiary.objects.get(id=apiary)
    hive_instance = Hive.objects.get(id=hive)
    if apiary_instance.keeper.user != request.user:
        raise PermissionDenied("You don't have permission to edit this hive.")

    if request.method == "POST":
        hive_instance.delete()
        #redirecting to the apiary again after deletion
        return redirect('apiary-detail', apiary) 

    return render(request, 'beekeeping_app/delete_hive.html', {'hive': hive_instance})


#update should show the existing hive with the fields filled and editable
@login_required(login_url='login')
@allowed_users(allowed_roles=['beekeeper_role'])
def updateApiary(request, keeper, apiary):
    apiary_instance = Apiary.objects.get(id=apiary)
    if apiary_instance.keeper.user != request.user:
        raise PermissionDenied("You don't have permission to edit this apiary.")
    
    if request.method == "POST":
        form = ApiaryForm(request.POST, request.FILES, instance=apiary_instance)
        if form.is_valid():
            image = request.FILES.get('company_logo')
            if image:
                #open the image using PIL
                img = Image.open(image)
                #convert RGBA to RGB
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                #resize the image to the desired dimensions (e.g., 300x300)
                img.thumbnail((40, 40))
                #save the resized image to a BytesIO buffer
                output = BytesIO()
                img.save(output, format='JPEG')
                #save the resized image to the FileField
                apiary_instance.company_logo.save(image.name, output)
            form.save()
            return redirect('apiary-detail', apiary_instance.id) 
    else:
        form = ApiaryForm(instance=apiary_instance)

    return render(request, 'beekeeping_app/update_apiary.html', {'apiary': apiary_instance, 'form': form})

#calendar views:
@login_required(login_url='login')
@allowed_users(allowed_roles=['beekeeper_role'])
def editCalendar(request, hive_id):
    hive_instance = Hive.objects.get(id=hive_id)
    calendar = hive_instance.calendar

    #get the events related to the calendar
    events = calendar.events.all()

    #initialize a calendar object with today's date
    d = getDate(request.GET.get('day', None))
    cal = Calendar(d.year, d.month)

    #add events to the calendar
    for event in events:
        cal.add_event(event.title, event.start_time, event.end_time)

    #generate HTML for the calendar
    html_cal = cal.formatmonth(withyear=True)

    return render(request, 'beekeeping_app/edit-calendar.html', {'hive': hive_instance, 'calendar': calendar, 'beekeeping_app/calendar.html': mark_safe(html_cal)})

def calendarView(request, hive_id):
    #retrieve the hive associated with the hive_id from the URL
    hive_instance = Hive.objects.get(id=hive_id)
    
    #retrieve the month from the request GET parameters or use the current month
    month = request.GET.get('month')
    d = getDate(month) if month else getDate(None)

    #filter events by the associated hive
    events = Event.objects.filter(calendar__hive=hive_instance)

    #instantiate our calendar class with the requested month
    cal = Calendar(d.year, d.month)

    #call the formatmonth method, which returns our calendar as a table
    html_cal = cal.formatmonth(withyear=True)

    #add previous and next month information to the context
    prev_month = prevMonth(d)
    next_month = nextMonth(d)

    #group context data
    context = {
        'calendar': mark_safe(html_cal),
        'prev_month': prev_month,
        'next_month': next_month,
        'hive_id': hive_id,
        'events': events 
    }

    return render(request, 'beekeeping_app/calendar.html', context)
    
def prevMonth(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def nextMonth(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

#get the current day based on imported libraries
def getDate(req_day):
    if req_day:
        year, month = map(int, req_day.split('-'))
        return datetime(year, month, day=1)
    return datetime.today()

#authentication for registering a user:
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            # Create a new group 'beekeeper_role' if it doesn't exist
            group, created = Group.objects.get_or_create(name='beekeeper_role')
            # Add the user to the 'beekeeper_role' group
            group.user_set.add(user)
            apiary = Apiary.objects.create()
            keeper = Keeper.objects.create(user=user, apiary=apiary)
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
    
    context = {'form':form}
    return render(request, 'registration/register.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['beekeeper_role'])
def userPage(request):
    keeper = request.user.keeper

    form = BeekeeperForm(instance=keeper)
    apiary = keeper.apiary
    if request.method == 'POST':
        form = BeekeeperForm(request.POST, request.FILES, instance=keeper)
        if form.is_valid():
            form.save()
    context = {'apiaries': apiary, 'keeper': keeper, 'form': form}
    return render(request, 'beekeeping_app/user.html', context)

def logoutView(request):
    logout(request)
    return render(request, 'registration/logout.html') 
