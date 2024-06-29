from django import forms
from django.forms import CharField


class ChatForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea, label='Message')