from django.forms.widgets import Textarea
import datetime
from datetime import timedelta
from django import forms
from apps.account.models import Profile

class LeaderForm(forms.ModelForm):
    """
    A class to create leader form
    """
    def __init__(self, *args, **kwargs):
        super(LeaderForm, self).__init__(*args, **kwargs)
        self.fields['sex'].empty_label              = 'Select'
        self.fields['id_type'].empty_label          = 'Select'
        self.fields['region'].empty_label           = 'Select'
        self.fields['district'].empty_label         = 'Select'
        self.fields['ward'].empty_label             = 'Select'
        self.fields['village'].empty_label          = 'Select'
        self.fields['working_ward'].empty_label     = 'Select'

    class Meta:
        model  = Profile
        exclude =('be_jembe', 'designation', 'working_village', 'working_shina')
        fields  = ('__all__')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'name', 'placeholder': 'Write fullname...', }),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'id': 'label', 'placeholder': 'Write label...', }),
            'work': forms.TextInput(attrs={'class': 'form-control', 'id': 'work', 'placeholder': 'Write occupation...', }),
            'sex': forms.Select(attrs={'class': 'form-control', 'id': 'sex'}),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'id': 'dob', 'placeholder': 'Write dob...', 'type': 'date', }),
            'id_type': forms.Select(attrs={'class': 'form-control', 'id': 'id_type'}),
            'id_number': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_number', 'placeholder': 'Write id number...', }),
            'region': forms.Select(attrs={'class': 'form-control', 'id': 'region_id'}),
            'district': forms.Select(attrs={'class': 'form-control', 'id': 'district_id'}),
            'ward': forms.Select(attrs={'class': 'form-control', 'id': 'ward_id'}),
            'village': forms.Select(attrs={'class': 'form-control', 'id': 'village_id'}),
            'physical_address': forms.Textarea(attrs={'class': 'form-control', 'id': 'title', 'placeholder': 'Write physical address...', 'rows': 3 }),
            # 'house_number': forms.TextInput(attrs={'class': 'form-control', 'id': 'house_number', 'placeholder': 'Write house number...', }),
            'working_ward': forms.Select(attrs={'class': 'form-control', 'id': 'working_ward_id'}),
        } 

        labels = {
            'name': 'VEO Name',
            'phone': 'Phone',
            'work': 'Occupation',
            'sex': 'Sex',
            'dob': 'Date of birth',
            'id_type': 'ID Type',
            'id_number': 'ID Number',
            'region': 'Region',
            'district': 'District',
            'ward': 'Ward',
            'village': 'Village',
            'physical_address': 'Physical address',
            # 'house_number': 'House Number',
            'working_ward': 'Ward',
        }      
