"""
ASGI config for django_graphql project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from ariadne.asgi import GraphQL
from channels.http import AsgiHandler
from channels.routing import URLRouter
from django.urls import path

from main.schemas import schema

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_graphql.settings')


application = URLRouter([
    path("graphql/", GraphQL(schema, debug=True)),
    path("", AsgiHandler),
])
