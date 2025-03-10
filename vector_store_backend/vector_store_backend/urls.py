"""
URL configuration for vector_store_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core.views import (
    get_details,
    get_resources,
    create_collection,
    delete_collection,
    search_vectors,
    insert_data,
    delete_data,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("details/", get_details, name="get_details"),
    path("resources/", get_resources, name="get_resources"),
    path("create-collection/", create_collection, name="create_collection"),
    path("delete-collection/", delete_collection, name="delete_collection"),
    path("search-vectors/", search_vectors, name="search_vectors"),
    path("insert-data/", insert_data, name="insert_data"),
    path("delete-data/", delete_data, name="delete_data"),
]
