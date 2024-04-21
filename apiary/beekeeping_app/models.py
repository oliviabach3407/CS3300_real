from django.db import models
from django.urls import reverse
from django.forms import ModelForm

#permissions
from django.contrib.auth.models import User

# Create your models here.

#a keeper should have only ONE apiary (one-to-one)
class Apiary(models.Model):

    title = models.CharField(max_length=200)

    #optional 
    company = models.CharField(max_length=200, blank=True)

    #image field (optional company logo)
    company_logo = models.ImageField(upload_to='C:/Users/olivi/OneDrive/GitHub/CS3300_real/apiary/static/images/company_logos/', blank=True, null=True)

    contact_email = models.CharField(max_length=200)
    is_published = models.BooleanField(default=False)
    
    #might need to change the max length here
    #optional to fill out, so blank property
    about = models.CharField(max_length=400, blank = True)

    #Define default String to return the name for representing the Model object."
    def __str__(self):
        return self.title

    #Returns the URL to access a particular instance of MyModelName.
    #if you define this method then Django will automatically
    # add a "View on Site" button to the model's record editing screens in the Admin site
    def get_absolute_url(self):
        return reverse('apiary-detail', args=[str(self.id)])


class Keeper(models.Model):

    name = models.CharField(max_length=200)
    email = models.CharField("Email", max_length=200)
    #removed blank = true

    #one keeper, one apiary
    #apiary = models.OneToOneField(Apiary, on_delete=models.CASCADE)
    apiary = models.OneToOneField(Apiary, on_delete=models.CASCADE, related_name='keeper')

    #for authentication
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    #Define default String to return the name for representing the Model object."
    def __str__(self):
        return self.name

    #Returns the URL to access a particular instance of MyModelName.
    #if you define this method then Django will automatically
    # add a "View on Site" button to the model's record editing screens in the Admin site
    def get_absolute_url(self):
        return reverse('keeper-detail', args=[str(self.id)])

#an Apiary should have MANY hives (one-to-many)
class Hive(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=400)

    #one apiary, many hives
    apiary = models.ForeignKey(Apiary, on_delete=models.CASCADE)

    #one hive, one calendar
    #event = models.ForeignKey(Event, on_delete=models.CASCADE)

    #Define default String to return the name for representing the Model object."
    def __str__(self):
        return self.title

    #Returns the URL to access a particular instance of MyModelName.
    #if you define this method then Django will automatically
    # add a "View on Site" button to the model's record editing screens in the Admin site
    def get_absolute_url(self):
        return reverse('hive-detail', args=[str(self.id)])
    
class HiveForm(ModelForm):
    class Meta:
        model = Hive
        fields = ["title", "description"]
    
class Calendar(models.Model):
    hive = models.OneToOneField(Hive, on_delete=models.CASCADE, related_name='calendar')

#each calendar can have MULTIPLE events
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    calendar = models.ForeignKey('Calendar', on_delete=models.CASCADE, related_name='events')

    def __str__(self):
        return self.title

    @property
    def get_html_url(self):
        url = reverse('event_edit', args=(self.calendar.hive_id, self.id))
        return f'<a href="{url}"> {self.title} </a>'