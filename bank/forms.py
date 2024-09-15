from django import forms
from .models import Idea, Link

class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ["name", "description", "complexity", "effort", "upside", "downside", "notes", "links"]

class LinkForm(forms.ModelForm):
    id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    
    class Meta:
        model = Link
        fields = ["id", "url"]