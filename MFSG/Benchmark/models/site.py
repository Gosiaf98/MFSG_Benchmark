from django.db import models


class Site(models.Model):

    title = models.CharField(max_length=200)
    path = models.CharField(max_length=200)
    dom = models.IntegerField(default=0)
    first_byte = models.IntegerField(default=0)
    interactive = models.IntegerField(default=0)

    def __str__(self):
        return self.title
