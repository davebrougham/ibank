from django import forms
from .models import Idea

class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ['name', 'description', 'complexity', 'effort', 'upside', 'downside']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field not in ['name', 'description']:
                self.fields[field].required = False
                
    def clean(self):
        cleaned_data = super().clean()
        for field in self.fields:
            if cleaned_data.get(field) == '':
                cleaned_data[field] = None
        return cleaned_data