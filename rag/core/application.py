import os
from functools import wraps
from importlib import import_module
from django.apps import apps
from django.apps import AppConfig
from django.conf import settings
from django.urls import set_script_prefix
from django.utils.log import configure_logging
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from rag import rest
from rag.core.settings import default


class Urls:
    def __init__(self, urlpatterns, restpatterns):
        self.urlpatterns = urlpatterns
        self.restpatterns = restpatterns

class Application:

    def __init__(self, name, settings=None, urls=None, models=None):
        self.name = name
        self.settings = settings
        self.urls = self.url_config(urls)
        self.appconfig = self.app_config(name)
        self.setup()
        self.models = self.model_config(models)

    @staticmethod
    def url_config(urls):
        if not urls: urls = []
        if isinstance(urls, str):
            return import_module(urls)
        else:
            return Urls([], urls)

    @staticmethod
    def model_config(models):
        if not models: return []
        for model in models:
            model.finalize()
        return models

    @staticmethod
    def app_config(name):
        return AppConfig(name, import_module(name))

    def route(self, route, method, *args, **kwargs):
        def decorator(func):
            self.urls.restpatterns.append(rest(route, method, func, *args, **kwargs))
            return func
        return decorator

    def register(self, model):
        self.models.append(model)
        model.finalize()
        return model

    def setup(self, set_prefix=True):
        # don't allow DJANGO_SETTINGS_MODULE because it loads settings differently than settings.configure (see dj docs)
        if "DJANGO_SETTINGS_MODULE" in os.environ:
            raise RuntimeError('DJANGO_SETTINGS_MODULE environment variable is not supported.')

        # load setttings
        if isinstance(self.settings, str):
            module = import_module(self.settings)
            self.settings = {k: getattr(module, k) for k in dir(module) if not k.startswith('_') and k.isupper()}

        # inject urls into settings
        self.settings['ROOT_URLCONF'] = self.urls

        # inject root asgi app setting
        self.settings['ASGI_APPLICATION'] = f'{self.name}:app.router'

        # configure settings
        settings.configure(default, **self.settings)

        # configure logging
        configure_logging(settings.LOGGING_CONFIG, settings.LOGGING)

        # set prefix
        if set_prefix:
            set_script_prefix('/' if settings.FORCE_SCRIPT_NAME is None else settings.FORCE_SCRIPT_NAME)

        # populate apps
        apps.populate([self.appconfig] + settings.INSTALLED_APPS)

    @property
    def router(self):
        # websocketpatterns = signals.patterns
        return ProtocolTypeRouter({
            "http": get_asgi_application(), # may not be needed (http->django views is added by default)
            # 'websocket': URLRouter(urls.websocketpatterns),
        })
