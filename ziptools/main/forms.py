from django import forms

class FormUploadFile(forms.Form):
    file = forms.FileField()
    # title = forms.CharField(max_length=50)
    # file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))