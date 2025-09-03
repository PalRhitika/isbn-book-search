
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from django.conf import settings
from .services import fetch_book

@api_view(['GET'])
def get_book(request, isbn: str):
    cache_key = f'book:{isbn}'
    cached = cache.get(cache_key)
    if cached:
        return Response(cached)
    #Get the Google books api key if available
    google_key = getattr(settings, 'GOOGLE_BOOKS_API_KEY', None)
    data = fetch_book(isbn, google_key)
    if not data:
        return Response({"detail": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
    cache.set(cache_key, data, 60 * 60)
    return Response(data)
