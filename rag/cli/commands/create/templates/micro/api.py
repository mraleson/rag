from rag import Application, models


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

@app.route("echo", 'POST')
def pong(request):
    return request.json
