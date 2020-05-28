from django.contrib.auth.models import User
from django.db import models

class Yearbook(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    data = models.TextField()
    secretkey = models.CharField(max_length=16)
