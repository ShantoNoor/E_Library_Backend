from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import admin
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator

PROFILE_ADMIN = 'A'
PROFILE_MODERATOR = 'M'
PROFILE_USER = 'U'
PROFILE_CHOICES = {
        (PROFILE_ADMIN, 'Admin'),
        (PROFILE_MODERATOR, 'Moderator'),
        (PROFILE_USER, 'User'),
    }

STATUS_PENDING = 'Pending'
STATUS_PUBLISHED = 'Published'
STATUS_REJECTED = 'Rejected'
STATUS_CHOICES = {
        (STATUS_PENDING, STATUS_PENDING),
        (STATUS_PUBLISHED, STATUS_PUBLISHED),
        (STATUS_REJECTED, STATUS_REJECTED),
    }


# Create your models here.

class User(AbstractUser):
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(unique=True)
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)
    phone = models.CharField(max_length=12)
    birth_date = models.DateField(null=True, blank=True)
    profile_type = models.CharField(
        max_length=1, choices=PROFILE_CHOICES, default=PROFILE_USER
    )

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'
    
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
    
    class Meta:
        ordering = ['user__first_name', 'user__last_name']


class Book(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    isbn = models.CharField(max_length=100, blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    publisher = models.CharField(max_length=100, blank=True, null=True)
    publish_date = models.DateField(blank=True, null=True)
    language = models.CharField(max_length=100, blank=True, null=True)
    page_number = models.PositiveIntegerField(default=0, blank=True, null=True)
    cover_photo = models.ImageField(upload_to='cover_photos', blank=True, null=True)
    pdf = models.FileField(upload_to='pdfs', blank=True, null=True, 
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf'])
        ]
    )
    book_status = models.CharField(
        max_length=9, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')

    def __str__(self) -> str:
        return self.name
    

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    date_time = models.DateTimeField(auto_now=True)
    review = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ('user', 'book')

    def __str__(self) -> str:
        return self.review


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='ratings')
    date_time = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(blank=False, null=False, validators=[
        MaxValueValidator(5),
        MinValueValidator(1)
    ])

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name} - {self.rating}'
