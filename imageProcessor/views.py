from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django import forms
from .forms import UploadFileForm, filterToSelect
from .models import Image
from PIL import Image as PILImage, ImageOps, ImageFilter
from django.conf import settings
import os

# Create your views here.

#default home page
#Todo : create template for image selection and filter selection



def index(request):
    #enters this branch once upload photo button is clicked
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()
            #saves id to transfer to next page
            request.session['image_id']=image.id
            
            return redirect('selectFilter', image_id=image.id)
    else:
        #defaults to here until user hits submit
        form = UploadFileForm()
        return render(request, "imageProcessor/upload.html", {"form": form})

def selectFilter(request, image_id):

    if request.method=="POST":
        form = filterToSelect(request.POST)
        if form.is_valid():
            
            #gets selected choice from form
            selectedFilter = form.cleaned_data['choice']
            
            #apply filter here
            applyFilter(image_id, selectedFilter)
            
            #get image object
            imageObject = Image.objects.get(id = image_id)

            return render(request, 'imageProcessor/successPage.html', {'image': imageObject, 'choice': selectedFilter})
    else:
        #defaults to here until user hits submit
        imageObject = Image.objects.get(id = image_id)
        form = filterToSelect()
        
        return render(request, 'imageProcessor/filterSelect.html', {'form': form, 'image': imageObject})


def applyFilter(image_id, choice):

    

    #gets image that was uploaded
    imageObject = Image.objects.get(id = image_id)
    
    #gets image from object for copying
    img = imageObject.uploadedImage


    #tokenizes image path so that choice is added to image name
    splitPath = os.path.basename(imageObject.uploadedImage.name).split('.')
    newBaseName = splitPath[0]+'-'+choice+'.'+splitPath[1]

    #creates and absolute path based on media_root for new image
    newImagePath = os.path.join(settings.MEDIA_ROOT, 'processedImage/', newBaseName)

    #copies original image into new file
    with open(newImagePath, 'wb+') as destination:
        for chunk in img.chunks():
            destination.write(chunk)

    #need to apply filters to newly created image here
    
    
    
    #updates the imageObject filtered image field with relative path
    imageObject.filteredImage = 'processedImage/'+newBaseName
    #saves database
    imageObject.save()




    #use if else to apply different filters

