import graphene
from graphene_django import DjangoObjectType
from graphene_django.rest_framework.mutation import SerializerMutation

from main.models import Author, Post
from main.serializers import PostSerializer


class AuthorType(DjangoObjectType):
    """
    It has the following schema representation
    ```
    type AuthorType{
        id: ID!
        first_name: String!
        last_name: String!
        email: String!
        posts: [PostType!]!
    }
    ```
    """
    class Meta:
        model = Author
        fields = ("id", "first_name", "last_name", "email", "posts")


class PostType(DjangoObjectType):
    """
    It has the following schema representation
    ```
    type PostType{
        id: ID!
        title: String!
        contents: String!
        author: AuthorType!
    }
    ```
    """
    class Meta:
        model = Post
        fields = ("id", "title", "contents", "author")


class CreateAuthor(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=True)

    # The class attributes define the response of the mutation
    author = graphene.Field(AuthorType)

    @classmethod
    def mutate(cls, root, info, first_name, last_name, email):
        author, _ = Author.objects.get_or_create(first_name=first_name, last_name=last_name, email=email)
        # Notice we return an instance of this mutation
        return CreateAuthor(author=author)


class PostInput(graphene.InputObjectType):
    """
    input PostInput{
        title: String!
        contents: String
        author_id: Int!
    }
    """
    title = graphene.String(required=True)
    contents = graphene.String()
    author_id = graphene.Int(required=True)


class CreatePost(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        post_data = PostInput(required=True)

    # The class attributes define the response of the mutation
    post = graphene.Field(PostType)

    @classmethod
    def mutate(cls, root, info, post_data=None):
        post, _ = Post.objects.get_or_create(
            title=post_data.title, contents=post_data.contents, author_id=post_data.author_id
        )
        # Notice we return an instance of this mutation
        return CreatePost(post=post)


class PostMutation(SerializerMutation):
    class Meta:
        serializer_class = PostSerializer
        model_operations = ['create', 'update']
        lookup_field = 'id'


class Mutation(graphene.ObjectType):
    create_author = CreateAuthor.Field()
    # create_or_update_post = PostMutation.Field()
    create_post = CreatePost.Field()


class Query(graphene.ObjectType):
    all_authors = graphene.List(AuthorType)
    author_by_email = graphene.Field(AuthorType, email=graphene.String(required=True))

    def resolve_all_authors(root, info):
        # We can easily optimize query count in the resolve method
        return Author.objects.prefetch_related("posts").all()

    def resolve_author_by_email(root, info, email):
        try:
            return Author.objects.get(email=email)
        except Author.DoesNotExist:
            return None


schema = graphene.Schema(query=Query, mutation=Mutation)
