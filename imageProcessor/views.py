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
import boto3
import io

# Create your views here.

#default home page
#Todo : create template for image selection and filter selection



def index(request):
    #enters this branch once upload photo button is clicked
    if (request.method == "POST"):
        form = UploadFileForm(request.POST, request.FILES)
        if (form.is_valid()):
            image = form.save()
            #saves id to transfer to next page
            request.session['image_id']=image.id
            
            return redirect('selectFilter', image_id=image.id)
    else:
        #defaults to here until user hits submit
        form = UploadFileForm()

    #returns to upload.html if first time, or if form is invalid
    return render(request, "imageProcessor/upload.html", {"form": form})

def selectFilter(request, image_id):

    if (request.method=="POST"):
        form = filterToSelect(request.POST)
        if (form.is_valid()):
            
            #gets selected choice from form
            selectedFilter = form.cleaned_data['choice']
            
            #apply filter here
            applyFilter(image_id, selectedFilter)
            
            #get image object
            imageObject = ImageTable.objects.get(id = image_id)

            return render(request, 'imageProcessor/successPage.html', {'image': imageObject, 'choice': selectedFilter})
        
    else:
        #defaults to here until user hits submit
        form = filterToSelect()

        #gets database row from imageTable
        imageObject = ImageTable.objects.get(id = image_id)
        
        return render(request, 'imageProcessor/filterSelect.html', {'form': form, 'image': imageObject})


def applyFilter(image_id, choice):

    #gets table row from database
    imageObject = ImageTable.objects.get(id = image_id)


    #tokenizes image path so that choice is added to image name
    splitPath = os.path.basename(imageObject.uploadedImage.name).split('.')
    newBaseName = splitPath[0]+'-'+choice+'.'+splitPath[1]
    

    #sets up s3 client to download image from bucket
    s3 = boto3.client('s3')
    bucketName = settings.AWS_STORAGE_BUCKET_NAME
    s3Key = imageObject.uploadedImage.name

    #hardcoded in because file storage is defaulted to s3
    localPath = '/home/ubuntu/cis4517-image-processor/media/imgToFilter/'+newBaseName

    #downloads image from s3 to edit
    s3.download_file(bucketName, s3Key, localPath)
    
    #opens downloaded image for processing
    imgToFilter = Image.open(localPath)
    
    
    #ensures photo can be filtered with below filters
    if(imgToFilter.mode != 'RGB'):
        imgToFilter = imgToFilter.convert('RGB')


    #filters image based on users choice
    if(choice == 'blur'):
        imgToFilter = imgToFilter.filter(ImageFilter.GaussianBlur)
    elif(choice == 'gray'):
        imgToFilter = ImageOps.grayscale(imgToFilter)
    elif(choice =='edge'):
        imgToFilter = ImageOps.grayscale(imgToFilter)
        imgToFilter = imgToFilter.filter(ImageFilter.FIND_EDGES)
    elif(choice == 'poster'):
        imgToFilter = ImageOps.posterize(imgToFilter,3)
    elif(choice == 'sepia'):
        sepia = []
        r, g, b = (239, 224, 185)
        for i in range(255):
            sepia.extend([int(r*i/255), int(g*i/255), int(b*i/255)])
        imgToFilter = imgToFilter.convert("L")
        imgToFilter.putpalette(sepia)
        imgToFilter = imgToFilter.convert("RGB")
    elif(choice == 'solar'):
        imgToFilter = ImageOps.solarize(imgToFilter, threshold=80)

    #saves filtered image to local path
    imgToFilter.save(localPath)
    shortName = os.path.basename(localPath)

    #places filtered image into s3 bucket
    s3.put_object(
        Bucket = bucketName,
        Key = 'media/filteredImage/'+shortName,
        Body = open(localPath, 'rb')
    )
    
    #updates database with location of filtered image
    imageObject.filteredImage = 'media/filteredImage/'+shortName

    #saves database
    imageObject.save()
    
    #deletes image from local server
    #os.remove(localPath)


