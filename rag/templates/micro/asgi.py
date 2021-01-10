from rag import Application
from rag import signals
from rag import rest
from django.views.decorators.csrf import csrf_exempt


settings = {
    'SECRET_KEY': 'mysecret',
    'DEBUG': True,
    'ASGI_APPLICATION': 'asgi.application'
}

app = Application(settings)

@app.route("ping", "get", [csrf_exempt])
def ping(request):
    return {'data': 'pong!'}

@app.route("pong", 'get', [csrf_exempt])
def pong(request):
    return {'data': 'bling!'}
