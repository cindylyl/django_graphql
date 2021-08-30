import asyncio
from typing import Any

from graphql import GraphQLResolveInfo

from main.models import Author, Post

from ariadne import QueryType, make_executable_schema, gql, ObjectType, \
    snake_case_fallback_resolvers, MutationType, SubscriptionType

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
        first_name: String
        last_name: String
        email: String
    }
    
    input PostInput {
        id: ID
        title: String
        contents: String
        author_id: ID
    }
    
    type Subscription {
        counter: Int!
    }
""")

# Create ObjectType instances for types defined in our schema...
query = QueryType()
author_type = ObjectType("AuthorType")
post_type = ObjectType("PostType")


# bind resolvers to its field defined on type_defs
@query.field("allAuthors")
def resolve_all_authors(obj: Any, info: GraphQLResolveInfo):
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
def resolve_author_by_email(*_, email):
    return Author.objects.get(email=email)

###########################################
# Mutation


mutation = MutationType()


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


#######################################
"""
Subscription requires to provide two functions for each field.

- generator is a function that yields data we're going to send to the client.
 It has to implement the AsyncGenerator protocol.
- resolver that tells the server how to send data to the client. 

After the last value is yielded the generator returns, the server tells the client that no more data will be available, 
and the subscription is complete.
"""

subscription = SubscriptionType()


@subscription.source("counter")
async def counter_generator(obj, info):
    for i in range(5):
        await asyncio.sleep(1)
        yield i


@subscription.field("counter")
def counter_resolver(count, info):
    return count + 1


schema = make_executable_schema(
    type_defs,
    [query, author_type, post_type, mutation, subscription, snake_case_fallback_resolvers]
)

