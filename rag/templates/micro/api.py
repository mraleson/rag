from rag import Application
from rag import models
from django.views.decorators.csrf import csrf_exempt


settings = {
    'SECRET_KEY': 'mysecret',
    'DEBUG': True,
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    }
}

class Question(models.Model):
    question_text = models.CharField(max_length=200)

app = Application(__name__, settings, models=[Question])

@app.route("ping", "get", [csrf_exempt])
def ping(request):
    return {'data': 'pong!'}

@app.route("pong", 'get', [csrf_exempt])
def pong(request):
    return {'data': 'bling!'}

@app.register
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
