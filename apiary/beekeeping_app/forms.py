from django import forms
from .models import Hive
from .models import Apiary

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
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'company_logo': forms.FileInput(attrs={'class': 'form-control-file'}),  # FileInput for uploading files
            'contact_email': forms.TextInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}), #a checkbox
            'about': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

