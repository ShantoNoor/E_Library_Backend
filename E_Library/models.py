from django.db import models

# Create your models here.

class Book(models.Model):
    name = models.CharField(max_length=100)
    author_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    isbn = models.CharField(max_length=100, blank=True, null=True)
    publisher = models.CharField(max_length=100, blank=True, null=True)
    publish_date = models.DateField(blank=True, null=True)
    language = models.CharField(max_length=100, blank=True, null=True)
    page_number = models.PositiveIntegerField(default=0, blank=True, null=True)
    cover_photo = models.ImageField(upload_to='cover_photos', blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    review = models.TextField(blank=True, null=True)


class Rating(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now=True)
    rating = models.PositiveIntegerField(default=0)
