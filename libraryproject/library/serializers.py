from rest_framework import serializers
from .models import Author, Book, Category

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Book
        fields = '__all__'

    def create(self, validated_data):
        authors_data = validated_data.pop('author')
        category_data = validated_data.pop('category')
        category, _ = Category.objects.get_or_create(**category_data)
        book = Book.objects.create(category=category, **validated_data)
        for author_data in authors_data:
            author, _ = Author.objects.get_or_create(**author_data)
            book.author.add(author)
        return book

    def update(self, instance, validated_data):
        authors_data = validated_data.pop('author')
        category_data = validated_data.pop('category')
        category, _ = Category.objects.get_or_create(**category_data)
        instance.category = category
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.published_date = validated_data.get('published_date', instance.published_date)
        instance.save()

        instance.author.clear()
        for author_data in authors_data:
            author, _ = Author.objects.get_or_create(**author_data)
            instance.author.add(author)

        return instance
