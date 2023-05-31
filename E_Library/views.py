from django.shortcuts import render
from django.core.files.storage import default_storage
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, DjangoModelPermissions
from rest_framework import viewsets, mixins, permissions
from rest_framework.decorators import action
from .models import Book, Review, Rating, UserProfile, STATUS_PUBLISHED
from .serializers import BookSerializer, ReviewSerializer, RatingSerializer, UserProfileSerializer
from .permissions import IsOwnerOrAdmin, IsOwner, BookIsOwner
from .admin import GROUP_MODERATOR

UNSAFE_METHODS = ('PATCH', 'PUT', 'DELETE')

# Create your views here.

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.prefetch_related('reviews').prefetch_related('ratings').all().filter(book_status=STATUS_PUBLISHED).order_by('-created_at')
    serializer_class = BookSerializer

    def get_permissions(self):
        method = self.request.method
        if method in permissions.SAFE_METHODS:
            return [AllowAny()]
        elif method == 'POST':
            return [IsAuthenticated()]
        elif method in ('PATCH', 'PUT', 'DELETE'):
            return [BookIsOwner()]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save()
        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if instance.cover_photo:
            file_path = instance.cover_photo.path
            if default_storage.exists(file_path):
                default_storage.delete(file_path)
        
        if instance.pdf:
            file_path = instance.pdf.path
            if default_storage.exists(file_path):
                default_storage.delete(file_path)

        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    
    def get_permissions(self):
        method = self.request.method
        if method in permissions.SAFE_METHODS:
            return [AllowAny()]
        elif method == 'POST':
            return [IsAuthenticated()]
        elif method in ('PATCH', 'PUT', 'DELETE'):
            return [IsOwner()]

    def get_queryset(self):
        return Review.objects.filter(book_id=self.kwargs['book_pk']).order_by('-date_time')
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        context.update({'book_id': self.kwargs['book_pk']})
        return context
    

class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer

    def get_queryset(self):
        return Rating.objects.filter(book_id=self.kwargs['book_pk']).order_by('-date_time')
    
    def get_permissions(self):
        method = self.request.method
        if method in permissions.SAFE_METHODS:
            return [AllowAny()]
        elif method == 'POST':
            return [IsAuthenticated()]
        elif method in UNSAFE_METHODS:
            return [IsOwner()]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        context.update({'book_id': self.kwargs['book_pk']})
        return context
    

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer 
    
    def get_permissions(self):
        method = self.request.method
        if method in permissions.SAFE_METHODS:
            return [AllowAny()]
        elif method == 'POST':
            return [IsAuthenticated()]
        elif method in ('PATCH', 'PUT', 'DELETE'):
            return [IsOwner()]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if instance.profile_picture:
            file_path = instance.profile_picture.path
            if default_storage.exists(file_path):
                default_storage.delete(file_path)

        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['GET', 'PATCH', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        (profile, created) = UserProfile.objects.get_or_create(user_id=request.user.id)

        if request.method in permissions.SAFE_METHODS:
            serializer = UserProfileSerializer(profile)
        else:
            serializer = UserProfileSerializer(profile, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response(serializer.data)