from django.urls import path
from .views import  landing_page
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('',landing_page.as_view(),name="landing"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

