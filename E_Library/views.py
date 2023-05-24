from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer
from django.core.files.storage import default_storage

# Create your views here.

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def destroy(self, request, *args, **kwargs):
        book = Book.objects.filter(id=kwargs['pk'])
        instance = self.get_object()
        if instance.cover_photo:
            file_path = instance.cover_photo.path
            if default_storage.exists(file_path):
                default_storage.delete(file_path)
        return super().destroy(request, *args, **kwargs)