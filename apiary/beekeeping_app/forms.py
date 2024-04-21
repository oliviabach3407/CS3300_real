from django import forms
from .models import Hive
from .models import Apiary
from .models import Keeper

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#calendar
from django.forms import ModelForm, DateInput
from .models import Event

#all hive forms use this base:
class HiveForm(forms.ModelForm):
    class Meta: 
        model = Hive
        #by default, ModelForm populates every form with all of the variables in the Project Model
        #we don't want the keeper being able to choose which portfolio to link to their project, so exclude it
        exclude = ['apiary'] 
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

class ApiaryForm(forms.ModelForm):
    class Meta:
        model = Apiary
        #shouldn't be able to edit their ownership
        exclude = ['owner']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'company_logo': forms.FileInput(attrs={'class': 'form-control-file'}),  #fileInput for uploading files
            'contact_email': forms.TextInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}), #a checkbox
            'about': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

#authentication
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class BeekeeperForm(forms.ModelForm):
    class Meta:
        model = Keeper
        fields = '__all__'
        exclude = ['user', 'apiary']

#calendars
class EventForm(ModelForm):
  class Meta:
    model = Event
    #datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
    }
    fields = '__all__'

  def __init__(self, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)
    #input_formats to parse HTML5 datetime-local input to datetime field
    self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)