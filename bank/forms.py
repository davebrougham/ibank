from django import forms
from .models import Idea, Link, Label

class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name']


class IdeaForm(forms.ModelForm):
    labels = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Idea
        fields = ["name", "description", "notes", "labels"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['notes'].required = False
        if self.instance.pk:
            self.fields['labels'].initial = ','.join([label.name for label in self.instance.labels.all()])

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            labels = self.cleaned_data['labels'].split(',')
            instance.labels.clear()
            for label_name in labels:
                label_name = label_name.strip()
                if label_name:
                    label, _ = Label.objects.get_or_create(name=label_name)
                    instance.labels.add(label)
        return instance

class LinkInlineFormSet(forms.inlineformset_factory(Idea, Link, fields=['url'], extra=1, can_delete=True)):
    pass

class IdeaCreateForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ["name", "description"]