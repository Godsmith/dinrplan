from django import forms


class UploadFileForm(forms.Form):
    meals = forms.FileField()
    days = forms.FileField()
