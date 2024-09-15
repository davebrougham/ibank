from django import forms
from .models import Idea, Link

class LinkInlineFormSet(forms.inlineformset_factory(Idea, Link, fields=['url'], extra=1, can_delete=True)):
    pass

class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ["name", "description", "complexity", "effort", "upside", "downside", "notes"]