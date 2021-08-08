from typing import Any

from ariadne.asgi import GraphQL
from graphql import GraphQLResolveInfo

from main.models import Author, Post

from ariadne import QueryType, make_executable_schema, gql, ObjectType, \
    snake_case_fallback_resolvers, MutationType

type_defs = gql("""
    type Query {
        allAuthors: [AuthorType]
        authorByEmail(email: String!): AuthorType
    }
    
    type AuthorType {
        id: ID!
        firstName: String
        lastName: String
        email: String!
        posts: [PostType!]
    }
    
    type PostType{
        id: ID!
        title: String!
        contents: String!
        author: AuthorType!
    }
    
    type Mutation {
        createOrUpdateAuthor(input: AuthorInput!): AuthorType
        createOrUpdatePost(input: PostInput!): PostType
    }
    
    input AuthorInput {
        id: ID
        firstName: String
        lastName: String
        email: String
    }
    
    input PostInput {
        id: ID
        title: String
        contents: String
        author_id: ID
    }
""")

# Create ObjectType instance for Query type defined in our schema...
query = QueryType()
author_type = ObjectType("AuthorType")
post_type = ObjectType("PostType")

mutation = MutationType()


# bind resolvers to its field defined on type_defs
@query.field("allAuthors")
def resolve_all_author(obj: Any, info: GraphQLResolveInfo):
    """

    :param obj: `obj` is a value returned by a parent resolver.
    :param info: `info` defines a special context attribute that contains any value that GraphQL server provided for
        resolvers on the query execution. Its type and contents are application-specific, but it is generally expected
        to contain application-specific data such as authentication state of the user or an HTTP request.
    :return:
    """
    return Author.objects.all()


@author_type.field("posts")
def resolve_posts(obj, info):
    return obj.posts.all()


@query.field("authorByEmail")
def resolve_all_author(*_, email):
    return Author.objects.get(email=email)


@mutation.field("createOrUpdateAuthor")
def resolve_create_or_update_author(*_, input):
    id = input.pop("id", None)
    if id:
        author, _ = Author.objects.update_or_create(id=id, defaults=input)
    else:
        author, _ = Author.objects.update_or_create(**input)
    return author


@mutation.field("createOrUpdatePost")
def resolve_create_or_update_post(*_, input):
    id = input.pop("id", None)
    if id:
        post, _ = Post.objects.update_or_create(id=id, defaults=input)
    else:
        post, _ = Post.objects.update_or_create(**input)
    return post


schema = make_executable_schema(type_defs, [query, author_type, post_type, mutation, snake_case_fallback_resolvers])
