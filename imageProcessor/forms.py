from django import forms
from .models import Image

class UploadFileForm(forms.ModelForm):

    #creates a file input
    class Meta:
        model = Image
        fields = ['uploadedImage']



CHOICES = [
    ('gray', 'Gray'),
    ('blur', 'Blur'),
    ('sepia', 'Sepia'),
    ('poster', 'Poster'),
    ('edge', 'Edge'),
    ('solar', 'Solar'),
]

class filterToSelect(forms.Form):
    choice = forms.ChoiceField(
        choices = CHOICES,
        widget=forms.RadioSelect,
        label="Select Filter to apply"
    )