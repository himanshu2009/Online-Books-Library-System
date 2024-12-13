"""
URL configuration for the library application.

This module defines the URL patterns for the library management system's API endpoints.
It uses Django REST Framework's DefaultRouter to automatically generate URLs for the ViewSet.

URL Patterns:
    - api/library/order/ (POST): Endpoint for borrowing items
    - api/library/return/ (POST): Endpoint for returning items

API Structure:
    All endpoints are prefixed with 'api/' and require authentication.
    The LibraryViewSet handles all library-related operations.

Example Usage:
    POST api/library/order/
        Request: {"title": "Book Title"}
        Response: {"message": "Item borrowed successfully"}

    POST api/library/return/
        Request: {"titles": ["Book Title 1", "Book Title 2"]}
        Response: {"message": "Items returned successfully"}
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LibraryViewSet

# Initialize the DefaultRouter for automatic URL routing
router = DefaultRouter()

# Register the LibraryViewSet with the router
# This creates URLs for all actions defined in the ViewSet
router.register(r'library', LibraryViewSet, basename='library')

# URL patterns for the library app
urlpatterns = [
    # Include all router-generated URLs under the 'api/' prefix
    path('api/', include(router.urls)),
]
