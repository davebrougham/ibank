from django.db import models

class Idea(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True)
    order = models.IntegerField(default=0)
    labels = models.ManyToManyField('Label', related_name='ideas', blank=True)
    class Meta:
        db_table = 'idea'
        ordering = ['order']

    def __str__(self):
        return self.name


class Link(models.Model):
    idea = models.ForeignKey('Idea', related_name='links', on_delete=models.CASCADE)
    url = models.URLField()

    def __str__(self):
        return self.url


class Label(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'label'

    def __str__(self):
        return self.name
    