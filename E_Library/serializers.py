from rest_framework import serializers
from .models import Book, Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'review', 'date_time']
    
    def create(self, validated_data):
        book_id = self.context['book_id']
        return Review.objects.create(book_id=book_id, **validated_data)

class BookSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = Book
        fields = ['id', 'name', 'author', 'description', 'isbn', 'publisher', 'publish_date', 'language', 'page_number', 'cover_photo', 'reviews']
        # fields = ('id', 'field1', 'field2')
        # exclude = ('field3',)