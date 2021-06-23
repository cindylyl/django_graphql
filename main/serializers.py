from rest_framework import serializers

from main import models


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Author
        fields = ['id', "first_name", "last_name", "email"]


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Post
        fields = ['id', "title", "contents", "author"]