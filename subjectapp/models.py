from django.db import models
from studentapp.models import Stream

# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=100)
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)
    semester = models.IntegerField(null=True)
    
    # get(): Search
    def __str__(self):
        return f"Subject name: {self.name} - Stream name: {self.stream.name} - Stream semester: {self.stream.semester}"