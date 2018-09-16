from django.db import models
from django.contrib.auth.models import User

class Schedule(models.Model):
    job = models.CharField(max_length=100)
    action_id = models.TextField(max_length=200)
    started = models.DateTimeField(auto_now_add=True)
    scheduled = models.CharField(max_length=50)
    author = models.ForeignKey(User, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.job
