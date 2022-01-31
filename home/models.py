from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    slug = models.SlugField()


    def __str__(self):
        return self.name

