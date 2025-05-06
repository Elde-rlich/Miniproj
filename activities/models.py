from django.db import models

class ActivityCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Task(models.Model):
    category = models.ForeignKey(ActivityCategory, on_delete=models.CASCADE, related_name="tasks")
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='activities/', blank=True, null=True)

