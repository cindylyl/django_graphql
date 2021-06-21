import graphene
from graphene_django import DjangoObjectType

from main.models import Author, Post


class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        fields = ("id", "first_name", "last_name")


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ("id", "name", "notes", "category")


class Query(graphene.ObjectType):
    all_authors = graphene.List(AuthorType)
    author_by_email = graphene.Field(AuthorType, email=graphene.String(required=True))

    def resolve_all_authors(root, info):
        # We can easily optimize query count in the resolve method
        return Author.objects.prefetch_related("posts").all()

    def resolve_category_by_name(root, info, email):
        try:
            return Author.objects.get(email=email)
        except Author.DoesNotExist:
            return None


schema = graphene.Schema(query=Query)
