from django import forms
from .models import Idea, Link

class LinkInlineFormSet(forms.inlineformset_factory(Idea, Link, fields=['url'], extra=1, can_delete=True)):
    pass

class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ["name", "description", "complexity", "effort", "upside", "downside", "notes"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['complexity'].required = False
        self.fields['effort'].required = False
        self.fields['upside'].required = False
        self.fields['downside'].required = False
        self.fields['notes'].required = False

class IdeaCreateForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ["name", "description"]