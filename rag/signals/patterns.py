from django.urls import path
from rag.signals import SignalConsumer

patterns = [
    path(r'ws/signals', SignalConsumer),
]
