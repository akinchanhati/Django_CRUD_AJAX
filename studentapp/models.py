from django.db import models

class Stream(models.Model):
    # id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    semester = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)