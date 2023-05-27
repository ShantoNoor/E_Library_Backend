from rest_framework import serializers
from .models import (Book, Review, User, Rating,
                     STATUS_CHOICES)

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'rating', 'date_time']


class ReviewSerializer(serializers.ModelSerializer):
    # user_id = serializers.ModelField(model_field=User, read_only=True)
    # book_id = serializers.ModelField(model_field=Book, read_only=True)
    class Meta:
        model = Review
        fields = ['id', 'review', 'date_time']
    
    def create(self, validated_data):
        book_id = self.context['book_id']
        user_id = self.context['request'].user.id
        return Review.objects.create(book_id=book_id, user_id=user_id, **validated_data)


class BookSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    book_status = serializers.ChoiceField(choices=STATUS_CHOICES, read_only=True)
    views = serializers.IntegerField(read_only=True)
    ratings = RatingSerializer(many=True, read_only=True)
    
    class Meta:
        model = Book
        fields = ['id', 'name', 'author', 'description', 'isbn', 'views', 'publisher', 'publish_date', 'language', 'page_number', 'cover_photo', 'pdf', 'book_status', 'ratings', 'reviews']
        # fields = ('id', 'field1', 'field2')
        # exclude = ('field3',)