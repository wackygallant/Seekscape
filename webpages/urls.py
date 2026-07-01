from django.urls import path

from webpages.views import Index_Page

urlpatterns = [
    path('', Index_Page.as_view(), name="index_page"),
]