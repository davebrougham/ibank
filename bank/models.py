from django.db import models

CATEGORY_CHOICES = [
    ("easy-big-wins", "Easy Big Wins"),
    ("easy-small-wins", "Easy Small Wins"),
    ("hard-big-wins", "Hard Big Wins"),
    ("hard-small-wins", "Hard Small Wins"),
]    

class Link(models.Model):
    idea = models.ForeignKey('Idea', related_name='links', on_delete=models.CASCADE)
    url = models.URLField()

    def __str__(self):
        return self.url

class Idea(models.Model):
    """
    Complexity 1-4 Low is good. 
        Definition: How technical the product would be to get to mvp. Are there regulations, competitive markets,
        lots of up front capital etc
    Effort 1-4 Low is good
        Definition: Is there a lot of upfront work required, will it require daily or weekly hours to maintain 
        and grow or once finished will it be set and forget.
    Upside 1-4 High is good
        Definition: Mostly capital upside, but also confidence, growth, learning are important to consider. 
    Downside 1-4 Low is good
        Definition: Time intensive, capital intensive, hard to know results for a long time or slow feedback loop,
        generally an unpleasant experience or something that will take all of me for a long time. 
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    complexity = models.IntegerField(default=None, null=True)
    effort = models.IntegerField(default=None, null=True)
    upside = models.IntegerField(default=None, null=True)
    downside = models.IntegerField(default=None, null=True)
    competitors = models.TextField(default=None, null=True)
    category = models.CharField(max_length=200, default=None, null=True, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True)
    order = models.IntegerField(default=0)

    class Meta:
        db_table = 'idea'
        ordering = ['order']

    def __str__(self):
        return self.name
        
    def calculate_score(self, complexity, effort, upside, downside):
        score = -complexity - effort + upside - int(downside)
        return score

    def categorize_idea(self, complexity=None, effort=None, upside=None, downside=None):
        score = self.calculate_score(complexity, effort, upside, downside)
        difficulty = "easy" if (complexity + effort) <= 5 else "hard"
        size = "big" if score >= 0 else "small"
        category = f"{difficulty}-{size}-wins"
        return category
        
    def update_grade(self):
        if all(getattr(self, field) is not None for field in ['complexity', 'effort', 'upside', 'downside']):
            new_category = self.categorize_idea(
                self.complexity, self.effort, self.upside, self.downside
            )
            if self.category != new_category:
                self.category = new_category
                return True
        return False
    
    def save(self, *args, **kwargs):
        category_changed = self.update_grade()
        super().save(*args, **kwargs)
        return category_changed