from django.db.models import Model as DjangoModel, DateTimeField
from django.forms.models import model_to_dict
from django.utils import timezone

# import everything from the django models module
from django.db.models import *

# override base model class to add additional functionality
def lazy_model(cache={}):
    if 'Model' not in cache:
        class Model(DjangoModel):

            created_at = DateTimeField(default=timezone.now)
            updated_at = DateTimeField(default=timezone.now)

            class Meta:
                abstract = True

            @classmethod
            def create(cls, values=None, **kwargs):
                values = values or kwargs
                return cls.objects.create(**values)

            def update(self, values=None, **kwargs):
                values = values or kwargs
                for field in list(values.keys()):
                    setattr(self, field, values[field])
                return self

            def to_dict(self, *args, **kwargs):
                return model_to_dict(self, *args, **kwargs)

            def save(self, *args, **kwargs):
                self.updated_at = timezone.now()
                super().save(*args, **kwargs)
                return self
        cache['Model'] = Model
    return cache['Model']

# lazily evaluate the modified base model class otherwise importing rag.models (like in rag's __init__.py)
# raises an django.core.exceptions.ImproperlyConfigured because we are using the base models meta class
del globals()['Model']
def __getattr__(name):
    if name == "Model": return lazy_model()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
