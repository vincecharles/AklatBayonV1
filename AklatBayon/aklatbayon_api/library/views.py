from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter
from .models import Author, Publisher, Category, Book, BookCopy
from .serializers import (
    AuthorSerializer, PublisherSerializer, CategorySerializer,
    BookSerializer, BookListSerializer, BookCopySerializer,
)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    search_fields = ['name']


class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    search_fields = ['name']


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    search_fields = ['name']

    def get_queryset(self):
        if self.action == 'list':
            return Category.objects.filter(parent__isnull=True)
        return Category.objects.all()


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related('author', 'publisher', 'category').prefetch_related('copies').all()
    search_fields = ['title', 'isbn', 'author__name']
    ordering_fields = ['title', 'publication_year', 'created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return BookListSerializer
        return BookSerializer


class BookCopyViewSet(viewsets.ModelViewSet):
    queryset = BookCopy.objects.select_related('book').all()
    serializer_class = BookCopySerializer
    search_fields = ['accession_number', 'book__title']


class PublicCatalogViewSet(viewsets.ReadOnlyModelViewSet):
    """Public catalog — no auth required."""
    queryset = Book.objects.select_related('author', 'category').all()
    serializer_class = BookListSerializer
    permission_classes = [permissions.AllowAny]
    search_fields = ['title', 'isbn', 'author__name']
