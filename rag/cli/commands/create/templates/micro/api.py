from rag import Application, models
from django.views.decorators.csrf import csrf_exempt


# settings
settings = {
    'SECRET_KEY': 'mysecret',
    'DEBUG': True,
}


# application
app = Application(__name__, settings)


# routes
@app.route("ping", "GET")
def ping(request):
    return {'data': 'pong!'}

@app.route("echo", 'POST', [csrf_exempt])
def pong(request):
    return request.data
