from django.db import models
from django.contrib.postgres.fields import ArrayField

class VectorField(ArrayField):
    def __init__(self, *args, **kwargs):
        kwargs['base_field'] = models.FloatField()
        kwargs['size'] = kwargs.pop('dimensions', None)
        super().__init__(*args, **kwargs)

class VectorEntry(models.Model):
    content = models.TextField()
    embedding = VectorField(dimensions=1536)  # OpenAI's embedding size
    conversation_id = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['conversation_id']),
        ]
        app_label = 'vector'