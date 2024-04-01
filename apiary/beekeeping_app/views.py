from django.shortcuts import render
from django.http import HttpResponse
from .models import Apiary
from .models import Keeper
from .models import Hive

from .forms import HiveForm
from .forms import ApiaryForm
from django.shortcuts import redirect

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
    return render(request, 'beekeeping_app/hive-detail.html', {'hive': hive_instance})


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
        form = ApiaryForm(request.POST, instance=apiary_instance)
        if form.is_valid():
            form.save()
            return redirect('apiary-detail', apiary_instance.id) 
    else:
        form = ApiaryForm(instance=apiary_instance)

    return render(request, 'beekeeping_app/update_apiary.html', {'apiary': apiary_instance, 'form': form})


