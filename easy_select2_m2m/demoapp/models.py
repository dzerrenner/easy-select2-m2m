from django.db import models
import six

class Tag(models.Model):
    name = models.CharField(max_length=127)

    def __str__(self):
        return self.name

class Parent(models.Model):
    tags = models.ManyToManyField(to='Tag', null=True, blank=True, symmetrical=False)

    def __str__(self):
        return ",".join([six.u(t.name) for t in self.tags.all()])
