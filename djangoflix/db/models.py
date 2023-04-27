from django.db import models

class StateOptions(models.TextChoices):
    PUBLISH = 'PB', 'Publish'
    DRAFT = 'DR', 'Draft'