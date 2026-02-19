from rest_framework import serializers
from .models import Author, Publisher, Category, Book, BookCopy


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio', 'created_at']


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name', 'address', 'contact', 'created_at']


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'children', 'created_at']

    def get_children(self, obj):
        children = obj.children.all()
        return CategorySerializer(children, many=True).data


class BookCopySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCopy
        fields = ['id', 'book', 'accession_number', 'status', 'created_at']


class BookSerializer(serializers.ModelSerializer):
    author_detail = AuthorSerializer(source='author', read_only=True)
    publisher_detail = PublisherSerializer(source='publisher', read_only=True)
    category_detail = CategorySerializer(source='category', read_only=True)
    copies = BookCopySerializer(many=True, read_only=True)
    available_copies = serializers.IntegerField(read_only=True)
    total_copies = serializers.IntegerField(read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'isbn', 'description', 'publication_year',
            'author', 'author_detail',
            'publisher', 'publisher_detail',
            'category', 'category_detail',
            'copies', 'available_copies', 'total_copies',
            'created_at', 'updated_at',
        ]


class BookListSerializer(serializers.ModelSerializer):
    """Lighter serializer for list views (no copies detail)."""
    author_name = serializers.CharField(source='author.name', read_only=True, default='')
    category_name = serializers.CharField(source='category.name', read_only=True, default='')
    available_copies = serializers.IntegerField(read_only=True)
    total_copies = serializers.IntegerField(read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'isbn', 'publication_year',
            'author', 'author_name',
            'category', 'category_name',
            'available_copies', 'total_copies',
            'created_at',
        ]
