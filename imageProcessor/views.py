from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django import forms
from .forms import UploadFileForm, filterToSelect
from .models import ImageTable
from PIL import Image, ImageOps, ImageFilter
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
            imageObject = ImageTable.objects.get(id = image_id)

            return render(request, 'imageProcessor/successPage.html', {'image': imageObject, 'choice': selectedFilter})
    else:
        #defaults to here until user hits submit
        imageObject = ImageTable.objects.get(id = image_id)
        form = filterToSelect()
        
        return render(request, 'imageProcessor/filterSelect.html', {'form': form, 'image': imageObject})


def applyFilter(image_id, choice):

    #print(Image.__version__)

    #gets image that was uploaded
    imageObject = ImageTable.objects.get(id = image_id)
    
    #gets image from object for copying
    #img = imageObject.uploadedImage


    #tokenizes image path so that choice is added to image name
    splitPath = os.path.basename(imageObject.uploadedImage.name).split('.')
    newBaseName = splitPath[0]+'-'+choice+'.'+splitPath[1]

    #creates an absolute path based on media_root for new image
    newImagePath = os.path.join(settings.MEDIA_ROOT, 'processedImage/', newBaseName)
    
    #open image again
    print("Image to open" + imageObject.uploadedImage.path)
    imgToFilter = Image.open(imageObject.uploadedImage.path)

    #debug
    print("Original Image Format:", imgToFilter.format)
    print("Original Image Size:", imgToFilter.size)
    
    #preserves the format
    original_format = imgToFilter.format


    if(choice == 'blur'):
        print(choice)
        imgToFilter = imgToFilter.filter(ImageFilter.GaussianBlur)
        

        
        
        
    elif(choice == 'gray'):
        print('gray')
        imgToFilter = ImageOps.grayscale(imgToFilter)
    elif(choice =='edge'):
        print('edge')
    elif(choice == 'poster'):
        print('poster')
    elif(choice == 'sepia'):
        print('sepia')
    elif(choice == 'solar'):
        print('solar')

    #debug
    print("After Image Format:", imgToFilter.format)
    print("After Image Size:", imgToFilter.size)
    
    #image filtering is not actually happening


    print(newImagePath)
    imgToFilter.save(newImagePath, format=original_format)
    
    
    #updates the imageObject filtered image field with relative path
    imageObject.filteredImage = 'processedImage/'+newBaseName
    #saves database
    imageObject.save()




    #use if else to apply different filters

