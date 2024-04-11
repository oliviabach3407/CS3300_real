from django.shortcuts import render
from django.http import HttpResponse
from .models import Apiary
from .models import Keeper
from .models import Hive
from .models import Event

from .forms import HiveForm
from .forms import ApiaryForm
from django.shortcuts import redirect

#for resizing the image as it's recieved
from PIL import Image
from io import BytesIO

#calendars:
from datetime import datetime
from django.views import generic
from django.utils.safestring import mark_safe
from .utils import Calendar
from .models import Event


# Create your views here.
def index(request):
    # Render index.html

    all_apiarys = Apiary.objects.all() 

    return render( request, 'beekeeping_app/index.html', {'Apiaries': all_apiarys})

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
    events = Event.objects.filter(hive=hive)
    return render(request, 'beekeeping_app/hive-detail.html', {'hive': hive, 'events': events})


#new should show an empty form - when submitted it adds that hive to the keeper's apiary
def newHive(request, apiary):
    apiary_instance = Apiary.objects.get(pk=apiary)

    if request.method == "POST":
        form = HiveForm(request.POST)
        if form.is_valid():
            hive = form.save(commit=False)
            hive.apiary = apiary_instance  # Associate the hive with the apiary
            hive.save()
            return redirect('hive-detail', hive.id)
    else:
        form = HiveForm()

    return render(request, 'beekeeping_app/create_hive.html', {'apiary': apiary_instance, 'form': form})

#update should show the existing hive with the fields filled and editable
def updateHive(request, apiary, hive):
    apiary_instance = Apiary.objects.get(id=apiary)
    hive_instance = Hive.objects.get(id=hive)

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
def deleteHive(request, apiary, hive):
    hive_instance = Hive.objects.get(id=hive)
    
    if request.method == "POST":
        hive_instance.delete()
        #redirecting to the apiary again after deletion
        return redirect('apiary-detail', apiary) 

    return render(request, 'beekeeping_app/delete_hive.html', {'hive': hive_instance})


#update should show the existing hive with the fields filled and editable
def updateApiary(request, keeper, apiary):
    apiary_instance = Apiary.objects.get(id=apiary)

    if request.method == "POST":
        form = ApiaryForm(request.POST, request.FILES, instance=apiary_instance)
        if form.is_valid():
            image = request.FILES.get('company_logo')
            if image:
                # Open the image using PIL
                img = Image.open(image)
                # Convert RGBA to RGB
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                # Resize the image to the desired dimensions (e.g., 300x300)
                img.thumbnail((40, 40))
                # Save the resized image to a BytesIO buffer
                output = BytesIO()
                img.save(output, format='JPEG')
                # Save the resized image to the FileField
                apiary_instance.company_logo.save(image.name, output)
            form.save()
            return redirect('apiary-detail', apiary_instance.id) 
    else:
        form = ApiaryForm(instance=apiary_instance)

    return render(request, 'beekeeping_app/update_apiary.html', {'apiary': apiary_instance, 'form': form})

#calendar views:

class CalendarView(generic.ListView):
    model = Event
    template_name = 'cal/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        return context

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return datetime.date(year, month, day=1)
    return datetime.today()


