from rest_framework import serializers
from .models import (Book, Review, User, UserProfile, Rating, STATUS_CHOICES)
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'first_name', 'last_name', 'username', 'email']
        

class RatingSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    book_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Rating
        fields = ['id', 'user_id', 'book_id', 'rating', 'date_time']
    
    def create(self, validated_data):
        book_id = self.context['book_id']
        user_id = self.context['request'].user.id
        return Rating.objects.create(book_id=book_id, user_id=user_id, **validated_data)


class ReviewSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    book_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Review
        fields = ['id', 'user_id', 'book_id', 'review', 'date_time']
    
    def create(self, validated_data):
        book_id = self.context['book_id']
        user_id = self.context['request'].user.id
        return Review.objects.create(book_id=book_id, user_id=user_id, **validated_data)


class BookSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    book_status = serializers.ChoiceField(choices=STATUS_CHOICES, read_only=True)
    views = serializers.IntegerField(read_only=True)
    ratings = RatingSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField(method_name='get_rating')
    added_by = UserSerializer(read_only=True)

    def get_rating(self, book):
        qs = Rating.objects.all().filter(book_id=book.id)
        total_rating = 0
        count_user = 0
        for rating in qs:
            total_rating += rating.rating
            count_user += 1

        if count_user == 0:
            return 0.0
        return total_rating / count_user
        
    def create(self, validated_data):
        added_by = self.context['request'].user
        return Book.objects.create(added_by=added_by, **validated_data)
    
    class Meta:
        model = Book
        fields = ['id', 'name', 'author', 'added_by', 'description', 'isbn', 'views', 'publisher', 'publish_date', 'language', 'page_number', 'cover_photo', 'pdf', 'book_status', 'ratings', 'rating', 'reviews']
        # fields = ('id', 'field1', 'field2')
        # exclude = ('field3',)


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password']


class UserProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = UserProfile
        fields = ['id', 'user_id', 'profile_picture', 'phone', 'birth_date']