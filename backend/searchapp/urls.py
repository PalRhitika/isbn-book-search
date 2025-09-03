
from django.urls import path, include
from .views import get_book

urlpatterns = [
    path('books/<str:isbn>/',get_book, name="books")
]
