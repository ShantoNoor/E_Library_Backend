from typing import Any, Dict, List, Optional, Sequence, Tuple, Union
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.auth.models import Group
from .models import (Book, Rating, Review, User, UserProfile,
                     PROFILE_ADMIN, PROFILE_MODERATOR, PROFILE_USER, STATUS_PUBLISHED, STATUS_PENDING, STATUS_REJECTED)


GROUP_MODERATOR = Group.objects.get(name='Moderator')

# Register your models here.
admin.site.register(Rating)
admin.site.register(Review)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'username', 'email', 'password1', 'password2'),
        }),
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'birth_date', 'profile_type']
    list_editable = ['profile_type']
    list_per_page = 10
    ordering = ['user']

    def save_form(self, request: Any, form: Any, change: Any) -> Any:
        form_data = form.cleaned_data
        
        user = None
        if form_data.get('user'):
            user = form_data.get('user') # getting user
        elif form_data.get('id'):
            user = User.objects.all().filter(profile=form_data.get('id')).first()

        if user and form_data.get('profile_type') == PROFILE_ADMIN:
            user.is_superuser = True
        else:
            user.is_superuser = False

        if user and form_data.get('profile_type') == PROFILE_USER:
            user.is_staff = False
        else:
            user.is_staff = True

        if user and form_data.get('profile_type') == PROFILE_MODERATOR:
            GROUP_MODERATOR.user_set.add(user)
        else:
            GROUP_MODERATOR.user_set.remove(user)

        if user: 
            user.save()

        return super().save_form(request, form, change)


@admin.register(Book)
class BookProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'added_by', 'book_status']
    list_editable = ['book_status']
    list_per_page = 10
    ordering = ['name']

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        qs1 = Book.objects.filter(book_status=STATUS_PENDING).all().order_by('-created_at')
        qs2 = Book.objects.filter(book_status=STATUS_PUBLISHED).all().order_by('-created_at')
        qs3 = Book.objects.filter(book_status=STATUS_REJECTED).all().order_by('-created_at')
        # qs = qs1.union(qs2)
        return qs1 | qs2 |qs3