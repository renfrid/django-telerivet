from django.forms.widgets import Textarea
import datetime
from datetime import timedelta
from django import forms
from .models import Menu, SubMenu, MenuLink

class MenuForm(forms.ModelForm):
    """
    A class to create menu form
    """
    def __init__(self, *args, **kwargs):
        super(MenuForm, self).__init__(*args, **kwargs)
        self.fields['keyword'].empty_label      = 'Select'

    class Meta:
        model  = Menu
        exclude = ('sequence', 'created_by', 'updated_by', 'relate')
        fields  = ('__all__')

        widgets = {
            'step': forms.TextInput(attrs={'class': 'form-control', 'id': 'step', 'placeholder': 'Write step...',}),
            'keyword': forms.Select(attrs={'class': 'form-control', 'id': 'keyword'}),
            'title': forms.Textarea(attrs={'class': 'form-control', 'id': 'title', 'placeholder': 'Write title...', 'rows': 3 }),
            'flag': forms.TextInput(attrs={'class': 'form-control', 'id': 'flag', 'placeholder': 'Write flag...', }),
            'label': forms.TextInput(attrs={'class': 'form-control', 'id': 'label', 'placeholder': 'Write label...', }),
            'pull': forms.NumberInput(attrs={'class': 'form-control', 'id': 'pull', 'placeholder': 'Write pull...', }),
            'url': forms.TextInput(attrs={'class': 'form-control', 'id': 'url', 'placeholder': 'Write pull url...', }),
        } 

        labels = {
            'step': "Menu Step",
            'keyword': 'Keyword',
            'title': 'Title',
            'flag': 'Flag',
            'label': 'Label',
            'pull': 'PULL',
            'url': 'PULL URL',
        }      
