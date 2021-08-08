from typing import Any

from ariadne.asgi import GraphQL
from graphql import GraphQLResolveInfo

from main.models import Author, Post

from ariadne import QueryType, make_executable_schema, gql, ObjectType, \
    snake_case_fallback_resolvers

type_defs = gql("""
    type Query {
        allAuthors: [AuthorType]
        authorByEmail(email: String!): AuthorType
    }
    
    type AuthorType {
        id: Int!
        firstName: String
        lastName: String
        email: String!
        posts: [PostType!]!
    }
    
    type PostType{
        id: Int!
        title: String!
        contents: String!
        author: AuthorType!
    }
    
""")

# Create ObjectType instance for Query type defined in our schema...
query = QueryType()
user_type = ObjectType("AuthorType")
post_type = ObjectType("PostType")


# bind resolvers to its field
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


@query.field("authorByEmail")
def resolve_all_author(*_, email):
    return Author.objects.get(email=email)


schema = make_executable_schema(type_defs, [query, user_type, post_type, snake_case_fallback_resolvers])
