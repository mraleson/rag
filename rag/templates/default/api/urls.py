from django.urls import path
from rag import rest, authorize
from rag import signals
from . import views


urlpatterns = [
    path('', views.index, name='index'),
]

restpatterns = [
    rest("ping", "get", views.ping),
    rest("login", "post", views.login),
    rest("logout", "post", views.logout),
    rest("message", "put", views.message, authorize.authenticated),
]

websocketpatterns = signals.patterns
