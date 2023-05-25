from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Book, Review
from .serializers import BookSerializer, ReviewSerializer
from django.core.files.storage import default_storage

# Create your views here.

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.prefetch_related('reviews').all()
    serializer_class = BookSerializer

    def destroy(self, request, *args, **kwargs):
        book = Book.objects.filter(id=kwargs['pk'])
        instance = self.get_object()
        if instance.cover_photo:
            file_path = instance.cover_photo.path
            if default_storage.exists(file_path):
                default_storage.delete(file_path)
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(book_id=self.kwargs['book_pk'])

    def get_serializer_context(self):
        return {'book_id': self.kwargs['book_pk']}