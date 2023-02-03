from django.forms.widgets import Textarea
import datetime
from datetime import timedelta
from django import forms
from apps.citizen.models import Citizen

class LeaderForm(forms.ModelForm):
    """
    A class to create leader form
    """
    def __init__(self, *args, **kwargs):
        super(LeaderForm, self).__init__(*args, **kwargs)
        self.fields['designation'].empty_label      = 'Select'
        self.fields['gender'].empty_label           = 'Select'
        self.fields['id_type'].empty_label          = 'Select'
        self.fields['ward'].empty_label     = 'Select'
        self.fields['village'].empty_label  = 'Select'

    class Meta:
        model  = Citizen
        exclude =('be_jembe', 'password', 'unique_id', 'created_by', 'updated_by')
        fields  = ('__all__')

        widgets = {
            'designation': forms.Select(attrs={'class': 'form-control', 'id': 'designation_id', 'required':''}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'name', 'placeholder': 'Write fullname...', 'required':'' }),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'id': 'label', 'placeholder': 'Write label...', 'required':'' }),
            'work': forms.TextInput(attrs={'class': 'form-control', 'id': 'work', 'placeholder': 'Write occupation...', }),
            'gender': forms.Select(attrs={'class': 'form-control', 'id': 'gender', 'required':''}),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'id': 'dob', 'placeholder': 'Write dob...', 'type': 'date', 'required':'' }),
            'id_type': forms.Select(attrs={'class': 'form-control', 'id': 'id_type', 'required':''}),
            'id_number': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_number', 'placeholder': 'Write id number...', 'required':'' }),
            'ward': forms.Select(attrs={'class': 'form-control', 'id': 'ward_id', 'required':''}),
            'village': forms.Select(attrs={'class': 'form-control', 'id': 'village_id'}),
            'shina': forms.TextInput(attrs={'class': 'form-control', 'id': 'shina', 'placeholder': 'Write shina...', }),
            'hamlet': forms.TextInput(attrs={'class': 'form-control', 'id': 'hamlet', 'placeholder': 'Write hamlet...', }),
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
            'hamlet': 'Where you live? (Hamlet)',
        }   