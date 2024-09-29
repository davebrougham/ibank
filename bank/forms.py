from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Idea, Link, Label, CustomUser

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

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ("email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email')
