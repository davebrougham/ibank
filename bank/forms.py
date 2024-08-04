from django import forms
from .models import Idea

class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ['name', 'description', 'complexity', 'effort', 'upside', 'downside', 'competitors']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field not in ['name', 'description']:
                self.fields[field].required = False