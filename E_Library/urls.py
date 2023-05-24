from django.urls import path, include 
from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(r'books', views.BookViewSet)
# router.register(r'reviews', views.ReviewViewSet)

book_router = routers.NestedDefaultRouter(router, 'books', lookup='book')
book_router.register('reviews', views.ReviewViewSet, basename='book-reviews')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(book_router.urls)),
]
