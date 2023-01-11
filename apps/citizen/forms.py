from django.forms.widgets import Textarea
import datetime
from datetime import timedelta
from django import forms
from .models import Citizen

class CitizenForm(forms.ModelForm):
    """
    A class to create leader form
    """
    def __init__(self, *args, **kwargs):
        super(CitizenForm, self).__init__(*args, **kwargs)
        self.fields['gender'].empty_label           = 'Select'
        self.fields['id_type'].empty_label          = 'Select'
        self.fields['ward'].empty_label             = 'Select'
        self.fields['village'].empty_label          = 'Select'

    class Meta:
        model  = Citizen
        exclude =('be_jembe', 'designation', 'working_ward' ,'working_village', 'working_shina', 'password', 'unique_id', 'created_by', 'updated_by')
        fields  = ('__all__')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'name', 'placeholder': 'Write fullname...', 'required':'' }),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'id': 'label', 'placeholder': 'Write label...', 'required':'' }),
            'work': forms.TextInput(attrs={'class': 'form-control', 'id': 'work', 'placeholder': 'Write occupation...', }),
            'gender': forms.Select(attrs={'class': 'form-control', 'id': 'gender', 'required':''}),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'id': 'dob', 'placeholder': 'Write dob...', 'type': 'date', 'required':'' }),
            'id_type': forms.Select(attrs={'class': 'form-control', 'id': 'id_type', 'required':''}),
            'id_number': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_number', 'placeholder': 'Write id number...', 'required':'' }),
            'ward': forms.Select(attrs={'class': 'form-control', 'id': 'ward_id', 'required':''}),
            'village': forms.Select(attrs={'class': 'form-control', 'id': 'village_id', 'required':''}),
            'physical_address': forms.TextInput(attrs={'class': 'form-control', 'id': 'title', 'placeholder': 'Write house number...' }),
            'work': forms.TextInput(attrs={'class': 'form-control', 'id': 'work', 'placeholder': 'Write occupation...', }),
            'hamlet': forms.TextInput(attrs={'class': 'form-control', 'id': 'work', 'placeholder': 'Write neighborhood...', }),
        } 

        labels = {
            'name': 'Full Name',
            'phone': 'Phone',
            'work': 'Occupation',
            'gender': 'Gender',
            'dob': 'Date of birth',
            'id_type': 'ID Type',
            'id_number': 'ID Number',
            'ward': 'Ward',
            'village': 'Village',
            'physical_address': 'House Number',
            'work': 'Occupation',
            'hamlet': 'Neighborhood',
        }      
