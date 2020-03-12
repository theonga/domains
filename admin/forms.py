from django import forms
class DeleteForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
