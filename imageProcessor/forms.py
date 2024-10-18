from django import forms
from .models import ImageTable

class UploadFileForm(forms.ModelForm):

    #creates a file input
    class Meta:
        model = ImageTable
        fields = ['uploadedImage']

    #ensures a file is an image
    def cleanUploadedImage(self):
        uploadedImage = self.cleaned_date.get('uploadedImage')

	#ensures file is an image
        if not uploaded_image:
            raise forms.ValidationError("Please upload an image.")

	#checks if image is jpeg, png or gif
        imageTypes = ['image/jpeg', 'image/png', 'image/gif']
        if uploaded_image.content_type not in imageTypes:
            raise forms.ValidationError("Please upload a JPEG, PNG, or GIF image")

        return uploaded_image


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
