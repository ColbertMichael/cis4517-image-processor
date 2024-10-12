from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("selectFilter/<int:image_id>/", views.selectFilter, name="selectFilter"),
    #path("FilterApplied/<int:image_id>/", views.filteredImage, name="filteredImage"),
    

]#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)