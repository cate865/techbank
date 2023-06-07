from django.urls import path
from .views import upload_resource,fetch_resources,search_by_category,search_by_filename
 
urlpatterns = [ 
    path('upload', upload_resource),
    path('all', fetch_resources),
    path('search/category', search_by_category),
    path('search/query', search_by_filename)
]