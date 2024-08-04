from django.db import models

class Idea(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    complexity = models.IntegerField(default=None, null=True)
    effort = models.IntegerField(default=None, null=True)
    upside = models.IntegerField(default=None, null=True)
    downside = models.IntegerField(default=None, null=True)
    competitors = models.TextField(default=None, null=True)
    category = models.TextField(default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'idea'
    
    def __str__(self):
        return self.name
    
    def set_category(self):
        pass