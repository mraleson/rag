import os
from functools import wraps
from importlib import import_module
from django.apps import apps
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

    def __init__(self, settings=None, urls=None):
        self.settings = settings
        if not urls: urls = []
        self.urls = import_module(urls) if isinstance(urls, str) else Urls([], urls)
        self.setup()

    def setup(self, set_prefix=True):
        # inject urls into settings
        self.settings['ROOT_URLCONF'] = self.urls

        # don't allow DJANGO_SETTINGS_MODULE because it loads settings differently than settings.configure (see dj docs)
        if "DJANGO_SETTINGS_MODULE" in os.environ:
            raise RuntimeError('DJANGO_SETTINGS_MODULE environment variable is not supported.')

        # configure settings
        if isinstance(self.settings, str):
            module = import_module(self.settings)
            self.settings = {k: getattr(module, k) for k in dir(module) if not k.startswith('_')}
        settings.configure(default, **self.settings)

        # configure logging
        configure_logging(settings.LOGGING_CONFIG, settings.LOGGING)

        # set prefix
        if set_prefix:
            set_script_prefix(
                '/' if settings.FORCE_SCRIPT_NAME is None else settings.FORCE_SCRIPT_NAME
            )

        # populate apps
        print(settings.INSTALLED_APPS)
        apps.populate(settings.INSTALLED_APPS)

    def route(self, route, method, *args, **kwargs):
        def decorator(func):
            self.urls.restpatterns.append(rest(route, method, func, *args, **kwargs))
            return func
        return decorator


    @property
    def router(self):
        # websocketpatterns = signals.patterns
        return ProtocolTypeRouter({
            "http": get_asgi_application(), # may not be needed (http->django views is added by default)
            # 'websocket': URLRouter(urls.websocketpatterns),
        })
